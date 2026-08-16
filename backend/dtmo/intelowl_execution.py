from __future__ import annotations

from typing import Annotated
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.config import Settings, get_settings
from dtmo.integrations.intelowl import IntelOwlAdapter, IntelOwlPolicyError
from dtmo.persistence.intelowl import IntelOwlEnrichmentRepository
from dtmo.persistence.models import IntelOwlEnrichmentRecord

router = APIRouter(prefix="/api/v1/intelowl", tags=["intelowl"])


class IntelOwlExecutionRequest(BaseModel):
    observable_type: str = Field(min_length=1, max_length=64)
    observable_value: str = Field(min_length=1, max_length=8192)
    handling: str = Field(min_length=1, max_length=64)
    analyzers: list[str] = Field(min_length=1, max_length=64)


class IntelOwlExecutionResponse(BaseModel):
    record_id: UUID
    item_id: UUID
    job_id: str
    status: str
    partial: bool
    analyzers: list[str]
    external_share_authorized: bool
    local_compromise_proven: bool


class IntelOwlHistoryResponse(BaseModel):
    records: list[IntelOwlExecutionResponse]


def _response(record: IntelOwlEnrichmentRecord) -> IntelOwlExecutionResponse:
    return IntelOwlExecutionResponse(
        record_id=record.id,
        item_id=record.item_id,
        job_id=record.job_id,
        status=record.status,
        partial=record.partial,
        analyzers=list(record.analyzers),
        external_share_authorized=record.external_share_authorized,
        local_compromise_proven=record.local_compromise_proven,
    )


@router.post(
    "/items/{item_id}/enrich",
    response_model=IntelOwlExecutionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def execute_enrichment(
    item_id: UUID,
    request: IntelOwlExecutionRequest,
    principal: Annotated[Principal, Depends(require_permission(Permission.REVIEW_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> IntelOwlExecutionResponse:
    """Execute one human-authorized, fail-closed IntelOwl enrichment and persist its result."""

    if not settings.feature_intelowl_enrichment:
        raise HTTPException(status_code=409, detail="IntelOwl enrichment feature flag is off")

    adapter = IntelOwlAdapter(settings)
    timeout = httpx.Timeout(settings.connector_timeout_seconds)
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
            result = await adapter.enrich(
                client,
                canonical_id=str(item_id),
                observable_type=request.observable_type,
                observable_value=request.observable_value,
                handling=request.handling,
                analyzers=request.analyzers,
                # IntelOwl is a separate service boundary. Treat every requested
                # analyzer as external disclosure unless a future reviewed contract
                # proves a narrower boundary.
                external_analyzers=set(request.analyzers),
            )
        record = await IntelOwlEnrichmentRepository(session).persist(
            item_id=item_id,
            result=result,
            handling=request.handling,
            analyzers=request.analyzers,
            requested_by=principal.subject,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="canonical intelligence item not found") from exc
    except IntelOwlPolicyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="IntelOwl upstream execution failed") from exc

    return _response(record)


@router.get("/items/{item_id}/history", response_model=IntelOwlHistoryResponse)
async def enrichment_history(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> IntelOwlHistoryResponse:
    del principal
    records = await IntelOwlEnrichmentRepository(session).list_for_item(item_id)
    return IntelOwlHistoryResponse(records=[_response(record) for record in records])
