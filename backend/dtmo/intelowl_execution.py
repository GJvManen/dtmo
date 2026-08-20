from __future__ import annotations

from typing import Annotated, Any
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.config import Settings, get_settings
from dtmo.integrations.cortex import CortexAdapter, CortexPolicyError
from dtmo.integrations.intelowl import IntelOwlAdapter, IntelOwlPolicyError
from dtmo.persistence.cortex import CortexAnalysisRecord, CortexAnalysisRepository
from dtmo.persistence.intelowl import IntelOwlEnrichmentRepository
from dtmo.persistence.models import IntelOwlEnrichmentRecord

router = APIRouter(tags=["analysis"])


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


class CortexExecutionRequest(BaseModel):
    observable_type: str = Field(min_length=1, max_length=64)
    observable_value: str = Field(min_length=1, max_length=8192)
    analyzer_id: str = Field(min_length=1, max_length=255)
    tlp: int = Field(ge=0, le=3)


class CortexExecutionResponse(BaseModel):
    record_id: UUID
    item_id: UUID
    job_id: str
    status: str
    analyzer_id: str
    tlp: int
    report: dict[str, Any]
    external_share_authorized: bool
    local_compromise_proven: bool


class CortexHistoryResponse(BaseModel):
    records: list[CortexExecutionResponse]


class AnalysisCapabilitiesResponse(BaseModel):
    intelowl_enabled: bool
    intelowl_observable_types: list[str]
    intelowl_analyzers: list[str]
    cortex_enabled: bool
    cortex_observable_types: list[str]
    cortex_analyzers: list[str]
    runtime_health_claim: bool = False
    responder_actions_allowed: bool = False
    external_share_authority: bool = False
    local_compromise_proof: bool = False


class UnifiedAnalysisHistoryResponse(BaseModel):
    item_id: UUID
    intelowl: IntelOwlHistoryResponse
    cortex: CortexHistoryResponse
    evidence_boundary: str


def _csv(value: str) -> list[str]:
    return sorted({part.strip() for part in value.split(",") if part.strip()})


def _intelowl_response(record: IntelOwlEnrichmentRecord) -> IntelOwlExecutionResponse:
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


def _cortex_response(record: CortexAnalysisRecord) -> CortexExecutionResponse:
    return CortexExecutionResponse(
        record_id=record.id,
        item_id=record.item_id,
        job_id=record.job_id,
        status=record.status,
        analyzer_id=record.analyzer_id,
        tlp=record.tlp,
        report=dict(record.report),
        external_share_authorized=record.external_share_authorized,
        local_compromise_proven=record.local_compromise_proven,
    )


@router.post(
    "/api/v1/intelowl/items/{item_id}/enrich",
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

    return _intelowl_response(record)


@router.get("/api/v1/intelowl/items/{item_id}/history", response_model=IntelOwlHistoryResponse)
async def enrichment_history(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> IntelOwlHistoryResponse:
    del principal
    records = await IntelOwlEnrichmentRepository(session).list_for_item(item_id)
    return IntelOwlHistoryResponse(records=[_intelowl_response(record) for record in records])


@router.get("/api/v1/analysis/capabilities", response_model=AnalysisCapabilitiesResponse)
async def analysis_capabilities(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AnalysisCapabilitiesResponse:
    del principal
    return AnalysisCapabilitiesResponse(
        intelowl_enabled=settings.feature_intelowl_enrichment,
        intelowl_observable_types=_csv(settings.intelowl_allowed_observable_types),
        intelowl_analyzers=_csv(settings.intelowl_allowed_analyzers),
        cortex_enabled=settings.feature_cortex_analysis,
        cortex_observable_types=_csv(settings.cortex_allowed_observable_types),
        cortex_analyzers=_csv(settings.cortex_allowed_analyzers),
    )


@router.post(
    "/api/v1/analysis/items/{item_id}/cortex",
    response_model=CortexExecutionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def execute_cortex_analysis(
    item_id: UUID,
    request: CortexExecutionRequest,
    principal: Annotated[Principal, Depends(require_permission(Permission.REVIEW_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> CortexExecutionResponse:
    """Execute one explicit analyzer-only Cortex job and persist bounded evidence."""

    if not settings.feature_cortex_analysis:
        raise HTTPException(status_code=409, detail="Cortex analysis feature flag is off")

    adapter = CortexAdapter(settings)
    timeout = httpx.Timeout(settings.connector_timeout_seconds)
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
            result = await adapter.analyze(
                client,
                canonical_id=str(item_id),
                observable_type=request.observable_type,
                observable_value=request.observable_value,
                analyzer_id=request.analyzer_id,
                tlp=request.tlp,
            )
        record = await CortexAnalysisRepository(session).persist(
            item_id=item_id,
            result=result,
            tlp=request.tlp,
            requested_by=principal.subject,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="canonical intelligence item not found") from exc
    except CortexPolicyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Cortex upstream execution failed") from exc

    return _cortex_response(record)


@router.get("/api/v1/analysis/items/{item_id}/history", response_model=UnifiedAnalysisHistoryResponse)
async def integrated_analysis_history(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UnifiedAnalysisHistoryResponse:
    del principal
    intelowl_records = await IntelOwlEnrichmentRepository(session).list_for_item(item_id)
    cortex_records = await CortexAnalysisRepository(session).list_for_item(item_id)
    return UnifiedAnalysisHistoryResponse(
        item_id=item_id,
        intelowl=IntelOwlHistoryResponse(records=[_intelowl_response(record) for record in intelowl_records]),
        cortex=CortexHistoryResponse(records=[_cortex_response(record) for record in cortex_records]),
        evidence_boundary=(
            "IntelOwl and Cortex outputs are enrichment evidence only. They do not authorize external sharing, "
            "do not prove local compromise by themselves, and do not establish live upstream health."
        ),
    )
