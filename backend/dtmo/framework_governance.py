from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.audit.chain import AuditDecision
from dtmo.audit.store import append_persistent_audit_event
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.logging import correlation_id
from dtmo.persistence.framework_models import GovernanceFramework, IntelligenceFrameworkMapping
from dtmo.persistence.models import IntelligenceItem

router = APIRouter(prefix="/api/v1/governance", tags=["governance"])


class FrameworkMappingCreate(BaseModel):
    framework_id: str = Field(min_length=1, max_length=64)
    object_type: Literal["control", "technique", "category", "scoring_context"]
    object_id: str = Field(min_length=1, max_length=128)
    object_title: str | None = Field(default=None, max_length=500)
    intelligence_id: UUID
    provenance_reference: str = Field(min_length=3, max_length=2000)
    confidence_score: int = Field(ge=0, le=100)
    mapping_reason: str = Field(min_length=3, max_length=4000)


class FrameworkMappingReview(BaseModel):
    decision: Literal["approved", "rejected"]


def _framework_status(framework: GovernanceFramework, mappings: list[IntelligenceFrameworkMapping]) -> str:
    if framework.coverage_mode == "context_only":
        return "CONTEXT_ONLY"
    if any(mapping.review_state == "approved" for mapping in mappings):
        return "MAPPED"
    return "UNMAPPED"


def _mapping_dict(mapping: IntelligenceFrameworkMapping, title: str | None = None) -> dict[str, object]:
    return {
        "id": str(mapping.id),
        "framework_id": mapping.framework_id,
        "framework_version": mapping.framework_version,
        "object_type": mapping.object_type,
        "object_id": mapping.object_id,
        "object_title": mapping.object_title,
        "intelligence_id": str(mapping.intelligence_id),
        "intelligence_title": title,
        "mapping_status": mapping.mapping_status,
        "provenance_reference": mapping.provenance_reference,
        "confidence_score": mapping.confidence_score,
        "mapping_reason": mapping.mapping_reason,
        "review_state": mapping.review_state,
        "created_by": mapping.created_by,
        "created_at": mapping.created_at.isoformat(),
        "reviewed_by": mapping.reviewed_by,
        "reviewed_at": mapping.reviewed_at.isoformat() if mapping.reviewed_at else None,
    }


def _framework_dict(framework: GovernanceFramework, mappings: list[IntelligenceFrameworkMapping]) -> dict[str, object]:
    approved = [mapping for mapping in mappings if mapping.review_state == "approved"]
    pending = [mapping for mapping in mappings if mapping.review_state == "pending"]
    rejected = [mapping for mapping in mappings if mapping.review_state == "rejected"]
    approved_objects = {(mapping.object_type, mapping.object_id) for mapping in approved}
    expected = framework.expected_object_count
    coverage_percent = round((len(approved_objects) / expected) * 100.0, 1) if expected else None
    return {
        "id": framework.id,
        "name": framework.name,
        "version": framework.version,
        "version_label": framework.version_label,
        "kind": framework.kind,
        "authority": framework.authority,
        "source_url": framework.source_url,
        "coverage_mode": framework.coverage_mode,
        "status": _framework_status(framework, mappings),
        "expected_object_count": expected,
        "mapped_object_count": len(approved_objects),
        "approved_mapping_count": len(approved),
        "pending_mapping_count": len(pending),
        "rejected_mapping_count": len(rejected),
        "coverage_percent": coverage_percent,
        "metadata": framework.metadata_json,
        "last_verified_at": framework.last_verified_at.isoformat(),
    }


async def _audit_mapping_change(
    session: AsyncSession,
    *,
    principal: Principal,
    action: str,
    resource: str,
    provenance_reference: str,
) -> None:
    request_id = correlation_id.get()
    if request_id == "-":
        request_id = str(uuid4())

    def append(sync_session) -> None:  # type: ignore[no-untyped-def]
        append_persistent_audit_event(
            sync_session,
            principal=principal.subject,
            principal_type="service_account" if principal.is_service_account else "human",
            action=action,
            resource=resource,
            decision=AuditDecision.RECORD,
            request_id=request_id,
            provenance_reference=provenance_reference,
        )

    await session.run_sync(append)


@router.get("/frameworks")
async def framework_inventory(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    del principal
    frameworks = (await session.scalars(select(GovernanceFramework).order_by(GovernanceFramework.name))).all()
    mappings = (await session.scalars(select(IntelligenceFrameworkMapping))).all()
    by_framework: dict[str, list[IntelligenceFrameworkMapping]] = {}
    for mapping in mappings:
        by_framework.setdefault(mapping.framework_id, []).append(mapping)
    return {
        "frameworks": [_framework_dict(framework, by_framework.get(framework.id, [])) for framework in frameworks],
        "mapping_policy": "explicit-provenance-human-reviewed-no-semantic-inference",
    }


@router.get("/frameworks/{framework_id}")
async def framework_detail(
    framework_id: str,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    del principal
    framework = await session.get(GovernanceFramework, framework_id)
    if framework is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="framework not found")
    rows = (
        await session.execute(
            select(IntelligenceFrameworkMapping, IntelligenceItem.title)
            .join(IntelligenceItem, IntelligenceItem.id == IntelligenceFrameworkMapping.intelligence_id)
            .where(IntelligenceFrameworkMapping.framework_id == framework_id)
            .order_by(IntelligenceFrameworkMapping.created_at.desc())
        )
    ).all()
    mappings = [mapping for mapping, _ in rows]
    return {
        "framework": _framework_dict(framework, mappings),
        "mappings": [_mapping_dict(mapping, title) for mapping, title in rows],
        "unmapped_rule": "No approved explicit mapping means UNMAPPED; DTMO never infers equivalence from tags or free text.",
    }


@router.get("/intelligence/{intelligence_id}/framework-mappings")
async def intelligence_framework_mappings(
    intelligence_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    del principal
    item = await session.get(IntelligenceItem, intelligence_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="intelligence item not found")
    mappings = (
        await session.scalars(
            select(IntelligenceFrameworkMapping)
            .where(IntelligenceFrameworkMapping.intelligence_id == intelligence_id)
            .order_by(IntelligenceFrameworkMapping.created_at.desc())
        )
    ).all()
    return {
        "intelligence_id": str(intelligence_id),
        "title": item.title,
        "mappings": [_mapping_dict(mapping, item.title) for mapping in mappings],
    }


@router.post("/framework-mappings", status_code=status.HTTP_201_CREATED)
async def create_framework_mapping(
    payload: FrameworkMappingCreate,
    principal: Annotated[Principal, Depends(require_permission(Permission.REVIEW_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    framework = await session.get(GovernanceFramework, payload.framework_id)
    if framework is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="framework not found")
    item = await session.get(IntelligenceItem, payload.intelligence_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="intelligence item not found")
    if framework.coverage_mode == "context_only" and payload.object_type != "scoring_context":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="context-only framework requires scoring_context mapping")
    existing = await session.scalar(
        select(IntelligenceFrameworkMapping).where(
            IntelligenceFrameworkMapping.framework_id == framework.id,
            IntelligenceFrameworkMapping.framework_version == framework.version,
            IntelligenceFrameworkMapping.object_type == payload.object_type,
            IntelligenceFrameworkMapping.object_id == payload.object_id,
            IntelligenceFrameworkMapping.intelligence_id == payload.intelligence_id,
        )
    )
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="framework mapping already exists")
    mapping = IntelligenceFrameworkMapping(
        id=uuid4(),
        framework_id=framework.id,
        framework_version=framework.version,
        object_type=payload.object_type,
        object_id=payload.object_id.strip(),
        object_title=payload.object_title.strip() if payload.object_title else None,
        intelligence_id=payload.intelligence_id,
        mapping_status="context_only" if framework.coverage_mode == "context_only" else "mapped",
        provenance_reference=payload.provenance_reference.strip(),
        confidence_score=payload.confidence_score,
        mapping_reason=payload.mapping_reason.strip(),
        review_state="pending",
        created_by=principal.subject,
        created_at=datetime.now(UTC),
    )
    session.add(mapping)
    await session.flush()
    await _audit_mapping_change(
        session,
        principal=principal,
        action="framework_mapping.create",
        resource=f"framework-mapping:{mapping.id}",
        provenance_reference=mapping.provenance_reference,
    )
    return _mapping_dict(mapping, item.title)


@router.post("/framework-mappings/{mapping_id}/review")
async def review_framework_mapping(
    mapping_id: UUID,
    payload: FrameworkMappingReview,
    principal: Annotated[Principal, Depends(require_permission(Permission.REVIEW_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    mapping = await session.get(IntelligenceFrameworkMapping, mapping_id)
    if mapping is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="framework mapping not found")
    if mapping.review_state != "pending":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="framework mapping already reviewed")
    mapping.review_state = payload.decision
    mapping.reviewed_by = principal.subject
    mapping.reviewed_at = datetime.now(UTC)
    await session.flush()
    await _audit_mapping_change(
        session,
        principal=principal,
        action=f"framework_mapping.{payload.decision}",
        resource=f"framework-mapping:{mapping.id}",
        provenance_reference=mapping.provenance_reference,
    )
    item = await session.get(IntelligenceItem, mapping.intelligence_id)
    return _mapping_dict(mapping, item.title if item else None)
