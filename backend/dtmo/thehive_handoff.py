from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.config import Settings, get_settings
from dtmo.integrations.thehive import (
    TLP_MAP,
    TheHiveAmbiguousDelivery,
    TheHiveCaseAdapter,
    TheHivePolicyError,
    build_case_payload,
)
from dtmo.persistence.models import IntelligenceItem, ProvenanceRecord
from dtmo.persistence.thehive import TheHiveHandoffRepository, TheHiveHandoffState

router = APIRouter(prefix="/api/v1/thehive", tags=["thehive"])


class TheHiveHandoffRequest(BaseModel):
    request_id: UUID
    summary: str = Field(min_length=1, max_length=4000)
    tlp: str = Field(min_length=1, max_length=32)
    pap: str = Field(min_length=1, max_length=32)


class TheHiveHandoffResponse(BaseModel):
    handoff_id: UUID
    request_id: UUID
    item_id: UUID
    status: str
    organization: str
    thehive_case_id: str | None
    thehive_case_number: str | None
    external_share_authorized: bool
    local_compromise_proven: bool


class TheHiveInvestigationHandoff(BaseModel):
    handoff_id: UUID
    request_id: UUID
    status: str
    requested_by: str
    organization: str
    tlp: str
    pap: str
    thehive_case_id: str | None
    thehive_case_number: str | None
    error_detail: str | None
    created_at: datetime
    updated_at: datetime
    external_share_authorized: bool
    local_compromise_proven: bool


class TheHiveInvestigationResponse(BaseModel):
    item_id: UUID
    title: str
    source_id: str
    canonical_url: str
    severity: str
    review_status: str
    provenance_count: int
    authoritative_tlp_tags: list[str]
    handoff_history: list[TheHiveInvestigationHandoff]
    handoff_blockers: list[str]
    principal_actions: dict[str, bool]
    feature_enabled: bool
    configured: bool
    runtime_health_claim: bool
    upstream_case_readback_supported: bool
    alerts_tasks_timeline_persisted: bool
    external_share_authority: bool
    local_compromise_proof: bool
    evidence_boundary: str


def _response(state: TheHiveHandoffState) -> TheHiveHandoffResponse:
    return TheHiveHandoffResponse(
        handoff_id=state.id,
        request_id=state.request_id,
        item_id=state.item_id,
        status=state.status,
        organization=state.organization,
        thehive_case_id=state.thehive_case_id,
        thehive_case_number=state.thehive_case_number,
        external_share_authorized=state.external_share_authorized,
        local_compromise_proven=state.local_compromise_proven,
    )


def _investigation_handoff(state: TheHiveHandoffState) -> TheHiveInvestigationHandoff:
    return TheHiveInvestigationHandoff(
        handoff_id=state.id,
        request_id=state.request_id,
        status=state.status,
        requested_by=state.requested_by,
        organization=state.organization,
        tlp=state.tlp,
        pap=state.pap,
        thehive_case_id=state.thehive_case_id,
        thehive_case_number=state.thehive_case_number,
        error_detail=state.error_detail,
        created_at=state.created_at,
        updated_at=state.updated_at,
        external_share_authorized=state.external_share_authorized,
        local_compromise_proven=state.local_compromise_proven,
    )


def validate_authoritative_handling(item: IntelligenceItem, requested_tlp: str) -> None:
    """Reject any handoff that would broaden or cannot represent known source restrictions."""

    requested = requested_tlp.strip().lower()
    requested_rank = TLP_MAP.get(requested)
    if requested_rank is None:
        raise TheHivePolicyError("unknown TLP mapping")

    source_ranks: list[int] = []
    for raw_tag in item.tags:
        tag = str(raw_tag).strip().lower()
        if tag.startswith("tlp:"):
            tag = tag.removeprefix("tlp:")
        if tag in TLP_MAP:
            source_ranks.append(TLP_MAP[tag])
    if source_ranks and requested_rank < max(source_ranks):
        raise TheHivePolicyError("requested TLP would broaden an authoritative source restriction")

    misp_restrictions = item.metadata_json.get("misp_restrictions")
    if isinstance(misp_restrictions, dict) and misp_restrictions.get("restriction_authoritative") is True:
        raise TheHivePolicyError(
            "authoritative MISP distribution/sharing-group restrictions require a deployment-approved TheHive access mapping"
        )


@router.get(
    "/items/{item_id}/investigation",
    response_model=TheHiveInvestigationResponse,
)
async def investigation_state(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> TheHiveInvestigationResponse:
    """Project canonical DTMO investigation and TheHive handoff evidence without inferring upstream state."""

    item = await session.get(IntelligenceItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="canonical intelligence item not found")

    provenance_count = int(
        await session.scalar(
            select(func.count()).select_from(ProvenanceRecord).where(ProvenanceRecord.item_id == item_id)
        )
        or 0
    )
    handoffs = await TheHiveHandoffRepository(session).list_for_item(item_id)
    configured = bool(
        settings.thehive_api_base.rstrip("/")
        and settings.thehive_api_token.get_secret_value().strip()
        and settings.thehive_organization.strip()
    )
    can_handoff = principal.can(Permission.CASE_HANDOFF) and not principal.is_service_account

    blockers: list[str] = []
    if provenance_count == 0:
        blockers.append("canonical provenance required before TheHive case handoff")
    if not settings.feature_thehive_handoff:
        blockers.append("TheHive case handoff feature is disabled")
    if not configured:
        blockers.append("TheHive case handoff runtime configuration is incomplete")
    if not can_handoff:
        blockers.append("current principal lacks human case-handoff authority")
    misp_restrictions = item.metadata_json.get("misp_restrictions")
    if isinstance(misp_restrictions, dict) and misp_restrictions.get("restriction_authoritative") is True:
        blockers.append(
            "authoritative MISP distribution/sharing-group restrictions require deployment-approved TheHive access mapping"
        )

    authoritative_tlp_tags = sorted(
        {
            str(raw_tag).strip().lower()
            for raw_tag in item.tags
            if str(raw_tag).strip().lower().startswith("tlp:")
        }
    )

    return TheHiveInvestigationResponse(
        item_id=item.id,
        title=item.title,
        source_id=item.source_id,
        canonical_url=item.canonical_url,
        severity=item.severity.value,
        review_status=item.review_status,
        provenance_count=provenance_count,
        authoritative_tlp_tags=authoritative_tlp_tags,
        handoff_history=[_investigation_handoff(record) for record in handoffs],
        handoff_blockers=blockers,
        principal_actions={"can_handoff": can_handoff},
        feature_enabled=bool(settings.feature_thehive_handoff),
        configured=configured,
        runtime_health_claim=False,
        upstream_case_readback_supported=False,
        alerts_tasks_timeline_persisted=False,
        external_share_authority=False,
        local_compromise_proof=False,
        evidence_boundary=(
            "Investigation state is derived from canonical DTMO intelligence, provenance and durable TheHive handoff records only. "
            "Configuration does not prove live TheHive health. Handoff history does not prove upstream case completeness, local compromise, "
            "external-share authority, responder execution, downstream action, or production authorization. Alerts, tasks and case timeline "
            "are not persisted by the accepted Phase 11.6 boundary and are therefore not inferred in Phase 11.10h."
        ),
    )


@router.post(
    "/items/{item_id}/cases",
    response_model=TheHiveHandoffResponse,
    status_code=status.HTTP_201_CREATED,
)
async def handoff_case(
    item_id: UUID,
    request: TheHiveHandoffRequest,
    principal: Annotated[Principal, Depends(require_permission(Permission.CASE_HANDOFF))],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> TheHiveHandoffResponse:
    """Create exactly one explicitly human-authorized TheHive case handoff."""

    if principal.is_service_account:
        raise HTTPException(status_code=403, detail="service accounts cannot authorize TheHive case handoff")
    if not settings.feature_thehive_handoff:
        raise HTTPException(status_code=409, detail="TheHive handoff feature flag is off")

    item = await session.get(IntelligenceItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="canonical intelligence item not found")
    provenance_count = await session.scalar(
        select(func.count()).select_from(ProvenanceRecord).where(ProvenanceRecord.item_id == item_id)
    )
    if not provenance_count:
        raise HTTPException(status_code=422, detail="TheHive handoff requires canonical provenance")

    try:
        validate_authoritative_handling(item, request.tlp)
        payload = build_case_payload(
            canonical_id=str(item.id),
            title=item.title,
            summary=request.summary,
            severity=item.severity.value,
            tlp=request.tlp,
            pap=request.pap,
            tags=list(item.tags),
        )
        adapter = TheHiveCaseAdapter(
            api_base=settings.thehive_api_base,
            api_token=settings.thehive_api_token.get_secret_value(),
            organization=settings.thehive_organization,
        )
    except TheHivePolicyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    repository = TheHiveHandoffRepository(session)
    try:
        state = await repository.reserve(
            request_id=request.request_id,
            item_id=item_id,
            requested_by=principal.subject,
            organization=settings.thehive_organization,
            tlp=request.tlp.strip().lower(),
            pap=request.pap.strip().lower(),
            authority_snapshot={
                "human_authorized": True,
                "permission": Permission.CASE_HANDOFF.value,
                "requested_by": principal.subject,
                "external_share_authorized": False,
                "local_compromise_proven": False,
            },
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    timeout = httpx.Timeout(settings.connector_timeout_seconds)
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
            result = await adapter.create_case(client, payload)
    except TheHiveAmbiguousDelivery as exc:
        await repository.mark_ambiguous(state, str(exc))
        raise HTTPException(status_code=502, detail="TheHive delivery ambiguous; manual reconciliation required") from exc
    except TheHivePolicyError as exc:
        await repository.mark_failed(state, str(exc))
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except httpx.HTTPError as exc:
        await repository.mark_failed(state, "TheHive upstream request failed before confirmed delivery")
        raise HTTPException(status_code=502, detail="TheHive upstream request failed") from exc

    state = await repository.mark_delivered(state, result)
    return _response(state)


@router.get("/items/{item_id}/handoffs", response_model=list[TheHiveHandoffResponse])
async def handoff_history(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[TheHiveHandoffResponse]:
    del principal
    records = await TheHiveHandoffRepository(session).list_for_item(item_id)
    return [_response(record) for record in records]
