from __future__ import annotations

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
        repository = TheHiveHandoffRepository(session)
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
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/items/{item_id}/handoffs", response_model=list[TheHiveHandoffResponse])
async def handoff_history(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[TheHiveHandoffResponse]:
    del principal
    records = await TheHiveHandoffRepository(session).list_for_item(item_id)
    return [_response(record) for record in records]
