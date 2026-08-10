from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.audit import AuditDecision
from dtmo.audit.store import append_persistent_audit_event
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal, Role
from dtmo.sources import SourceDefinition, SourceRegistry, validate_source_url
from dtmo.api.routes import get_session


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
    created_by: str
    updated_by: str


def _human_admin(principal: Principal) -> None:
    if principal.is_service_account or Role.ADMIN not in principal.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="source registry changes require a human admin role",
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
        created_by=source.created_by,
        updated_by=source.updated_by,
    )


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
    registry = SourceRegistry(session)
    try:
        source = await registry.create(
            source_id=request.id,
            name=request.name,
            source_type=request.source_type,
            endpoint_url=request.endpoint_url,
            enabled=request.enabled,
            interval_seconds=request.interval_seconds,
            reliability=request.reliability,
            secret_ref=request.secret_ref,
            actor=principal.subject,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    await session.run_sync(
        lambda sync_session: append_persistent_audit_event(
            sync_session,
            principal=principal.subject,
            principal_type="human",
            action="source.create",
            resource=f"source:{source.id}",
            decision=AuditDecision.ALLOW,
            request_id=request_id,
            provenance_reference=source.endpoint_url,
        )
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
    await session.run_sync(
        lambda sync_session: append_persistent_audit_event(
            sync_session,
            principal=principal.subject,
            principal_type="human",
            action="source.update",
            resource=f"source:{source.id}",
            decision=AuditDecision.ALLOW,
            request_id=request_id,
            provenance_reference=source.endpoint_url,
        )
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
        "execution": "built-in" if source.source_type == "cisa-kev" else "registry-only",
        "note": "generic source execution requires the next connector-adapter run",
    }
