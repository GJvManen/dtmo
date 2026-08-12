from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.alerts import connector_alerts
from dtmo.api.routes import get_session, ingest_connector_record
from dtmo.audit import AuditDecision
from dtmo.audit.store import append_persistent_audit_event
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal, Role
from dtmo.connectors.state import ConnectorStateStore
from dtmo.source_catalog import SOURCE_CATALOG, catalog_by_id
from dtmo.source_framework import SOURCE_ADAPTER_REGISTRY, execute_source
from dtmo.source_onboarding import test_manual_source
from dtmo.sources import SourceDefinition, SourceRegistry, validate_source_url

router = APIRouter(prefix="/api/v1/admin/sources", tags=["admin-sources"])


class SourceCreateRequest(BaseModel):
    id: str = Field(min_length=2, max_length=128)
    name: str = Field(min_length=2, max_length=255)
    source_type: str
    endpoint_url: str = Field(min_length=8, max_length=2048)
    enabled: bool = False
    interval_seconds: int = Field(default=3600, ge=60, le=86400)
    reliability: str = "medium"
    secret_ref: str | None = Field(default=None, max_length=512)


class SourceUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    endpoint_url: str | None = Field(default=None, min_length=8, max_length=2048)
    enabled: bool | None = None
    interval_seconds: int | None = Field(default=None, ge=60, le=86400)
    reliability: str | None = None
    secret_ref: str | None = Field(default=None, max_length=512)


class SourceResponse(BaseModel):
    id: str
    name: str
    source_type: str
    endpoint_url: str
    enabled: bool
    interval_seconds: int
    reliability: str
    secret_ref: str | None
    authentication_mode: str
    owner: str
    created_by: str
    updated_by: str


def _human_admin(principal: Principal) -> None:
    if principal.is_service_account or Role.ADMIN not in principal.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="source registry changes require a human admin role",
        )


def _authentication_mode(source: SourceDefinition) -> str:
    return "credentialed-secret-reference" if source.secret_ref else "anonymous"


def _validate_manual_auth_contract(request: SourceCreateRequest) -> None:
    if not request.secret_ref:
        return
    entry = catalog_by_id(request.id.strip().lower())
    if entry is None or entry.execution_status != "supported":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="manual credentialed sources require a code-reviewed registered adapter profile",
        )
    spec = SOURCE_ADAPTER_REGISTRY.get(entry.execution_profile)
    if spec is None or not spec.requires_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the selected source profile does not use a credential reference",
        )


def _response(source: SourceDefinition) -> SourceResponse:
    return SourceResponse(
        id=source.id,
        name=source.name,
        source_type=source.source_type,
        endpoint_url=source.endpoint_url,
        enabled=source.enabled,
        interval_seconds=source.interval_seconds,
        reliability=source.reliability,
        secret_ref=source.secret_ref,
        authentication_mode=_authentication_mode(source),
        owner=source.created_by,
        created_by=source.created_by,
        updated_by=source.updated_by,
    )


async def _audit(
    session: AsyncSession,
    *,
    principal: Principal,
    action: str,
    resource: str,
    request_id: str,
    provenance_reference: str,
) -> None:
    await session.run_sync(
        lambda sync_session: append_persistent_audit_event(
            sync_session,
            principal=principal.subject,
            principal_type="human",
            action=action,
            resource=resource,
            decision=AuditDecision.ALLOW,
            request_id=request_id,
            provenance_reference=provenance_reference,
        )
    )


@router.get("/catalog")
async def source_catalog(
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
) -> list[dict[str, object]]:
    _human_admin(principal)
    return [entry.as_dict() for entry in SOURCE_CATALOG]


@router.post("/catalog/bootstrap", response_model=list[SourceResponse])
async def bootstrap_supported_sources(
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> list[SourceResponse]:
    """Idempotently register code-reviewed executable catalog sources, disabled by default."""
    _human_admin(principal)
    registry = SourceRegistry(session)
    created: list[SourceResponse] = []
    for entry in SOURCE_CATALOG:
        if entry.execution_status != "supported":
            continue
        existing = await registry.get(entry.id)
        if existing is not None:
            created.append(_response(existing))
            continue
        source = await registry.create(
            source_id=entry.id,
            name=entry.name,
            source_type="json-feed",
            endpoint_url=entry.endpoint_url,
            enabled=False,
            interval_seconds=entry.recommended_interval_seconds,
            reliability=entry.reliability,
            secret_ref=entry.secret_ref,
            actor=principal.subject,
        )
        await _audit(
            session,
            principal=principal,
            action="source.bootstrap",
            resource=f"source:{source.id}",
            request_id=request_id,
            provenance_reference=source.endpoint_url,
        )
        created.append(_response(source))
    return created


@router.get("", response_model=list[SourceResponse])
async def list_sources(
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[SourceResponse]:
    _human_admin(principal)
    return [_response(source) for source in await SourceRegistry(session).list()]


@router.post("", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def create_source(
    request: SourceCreateRequest,
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> SourceResponse:
    _human_admin(principal)
    if request.enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="new manual sources must be created disabled; validate/test before activation",
        )
    _validate_manual_auth_contract(request)
    registry = SourceRegistry(session)
    try:
        source = await registry.create(
            source_id=request.id,
            name=request.name,
            source_type=request.source_type,
            endpoint_url=request.endpoint_url,
            enabled=False,
            interval_seconds=request.interval_seconds,
            reliability=request.reliability,
            secret_ref=request.secret_ref,
            actor=principal.subject,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    await _audit(
        session,
        principal=principal,
        action="source.create",
        resource=f"source:{source.id}",
        request_id=request_id,
        provenance_reference=source.endpoint_url,
    )
    return _response(source)


@router.patch("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: str,
    request: SourceUpdateRequest,
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> SourceResponse:
    _human_admin(principal)
    registry = SourceRegistry(session)
    source = await registry.get(source_id)
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="source not found")
    try:
        source = await registry.update(
            source,
            name=request.name,
            endpoint_url=request.endpoint_url,
            enabled=request.enabled,
            interval_seconds=request.interval_seconds,
            reliability=request.reliability,
            secret_ref=request.secret_ref,
            actor=principal.subject,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    await _audit(
        session,
        principal=principal,
        action="source.update",
        resource=f"source:{source.id}",
        request_id=request_id,
        provenance_reference=source.endpoint_url,
    )
    return _response(source)


@router.post("/{source_id}/validate")
async def validate_source(
    source_id: str,
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    _human_admin(principal)
    source = await SourceRegistry(session).get(source_id)
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="source not found")
    try:
        validate_source_url(source.endpoint_url)
    except ValueError as exc:
        return {"id": source.id, "valid": False, "reason": str(exc)}
    return {
        "id": source.id,
        "valid": True,
        "source_type": source.source_type,
        "enabled": source.enabled,
        "owner": source.created_by,
        "authentication_mode": _authentication_mode(source),
        "execution": "built-in" if source.source_type == "cisa-kev" else "governed-adapter",
        "note": "runtime re-resolves DNS, rejects non-global destinations and redirects, pins TLS to the validated address, enforces response bounds, and resolves credential references without storing secret values in the registry",
    }


@router.post("/{source_id}/test")
async def test_registered_source(
    source_id: str,
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> dict[str, object]:
    """Execute a bounded non-ingesting pre-activation test for a manual JSON source."""
    _human_admin(principal)
    source = await SourceRegistry(session).get(source_id)
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="source not found")
    result = await test_manual_source(source)
    await _audit(
        session,
        principal=principal,
        action="source.test",
        resource=f"source:{source.id}",
        request_id=request_id,
        provenance_reference=source.endpoint_url,
    )
    return {
        "id": source.id,
        "status": result.status,
        "records": len(result.records),
        "error": result.error,
        "enabled": source.enabled,
        "ingested": False,
        "publication_gate": "human-review-and-separate-share-approval-required",
    }


@router.post("/{source_id}/run")
async def run_registered_source(
    source_id: str,
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> dict[str, object]:
    _human_admin(principal)
    source = await SourceRegistry(session).get(source_id)
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="source not found")
    if source.source_type == "cisa-kev":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="use the built-in CISA KEV execution path")
    isolated = await session.run_sync(
        lambda sync_session: ConnectorStateStore(sync_session).is_isolated(source.id)
    )
    if isolated:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="source is temporarily isolated after repeated failures")

    started = datetime.now(UTC)
    result = await execute_source(source)
    inserted = 0
    indexed = 0
    if result.status == "completed":
        for record in result.records:
            receipt = await ingest_connector_record(source.id, record)
            inserted += int(receipt.inserted)
            indexed += int(receipt.indexed)
    duration = max((datetime.now(UTC) - started).total_seconds(), 0.0)
    await session.run_sync(
        lambda sync_session: ConnectorStateStore(sync_session).record_run(
            connector_id=source.id,
            run_id=uuid4(),
            succeeded=result.status == "completed",
            duration_seconds=duration,
            record_count=len(result.records),
            quarantined=[],
            error_code=None if result.status == "completed" else "source_execution_failed",
            details={"inserted": inserted, "indexed": indexed, "error": result.error},
        )
    )
    alert = connector_alerts.record(result)
    await _audit(
        session,
        principal=principal,
        action="source.run",
        resource=f"source:{source.id}",
        request_id=request_id,
        provenance_reference=source.endpoint_url,
    )
    return {
        "id": source.id,
        "status": result.status,
        "records": len(result.records),
        "inserted": inserted,
        "indexed": indexed,
        "error": result.error,
        "alert_state": alert.state,
        "correlation_id": alert.correlation_id,
        "publication_gate": "human-review-and-separate-share-approval-required",
    }
