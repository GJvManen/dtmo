from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.config import Settings, get_settings
from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.opencti import OpenCTIMappingRevision, OpenCTIObjectMapping

router = APIRouter(tags=["opencti-workspace"])


class OpenCTICapabilitiesResponse(BaseModel):
    enabled: bool
    configured: bool
    allowed_entity_types: list[str]
    runtime_health_claim: bool = False
    upstream_relationship_topology_persisted: bool = False
    external_share_authority: bool = False
    local_compromise_proof: bool = False


class OpenCTIGraphNode(BaseModel):
    id: str
    kind: str
    label: str
    entity_type: str
    stix_id: str | None = None
    confidence: int | None = None
    markings: list[dict[str, Any]] = []
    last_seen_at: datetime | None = None


class OpenCTIGraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship_type: str
    evidence_class: str


class OpenCTIGraphResponse(BaseModel):
    item_id: UUID
    title: str
    nodes: list[OpenCTIGraphNode]
    edges: list[OpenCTIGraphEdge]
    topology_scope: str
    upstream_relationship_topology_persisted: bool = False
    evidence_boundary: str


class OpenCTIRevisionResponse(BaseModel):
    id: UUID
    snapshot_hash: str
    recorded_at: datetime
    snapshot: dict[str, Any]


class OpenCTIEntityResponse(BaseModel):
    mapping_id: UUID
    item_id: UUID
    opencti_id: str
    stix_id: str
    entity_type: str
    parent_types: list[str]
    markings: list[dict[str, Any]]
    confidence: int | None
    upstream_created_at: str | None
    upstream_updated_at: str | None
    external_references: list[dict[str, Any]]
    provenance: dict[str, Any]
    snapshot_hash: str
    last_seen_at: datetime
    external_share_authorized: bool
    local_compromise_proven: bool
    revisions: list[OpenCTIRevisionResponse]
    evidence_boundary: str


def _csv(value: str) -> list[str]:
    return sorted({part.strip() for part in value.split(",") if part.strip()})


@router.get("/api/v1/opencti/capabilities", response_model=OpenCTICapabilitiesResponse)
async def opencti_capabilities(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    settings: Annotated[Settings, Depends(get_settings)],
) -> OpenCTICapabilitiesResponse:
    del principal
    configured = bool(settings.opencti_api_base.strip() and settings.opencti_api_token.get_secret_value().strip())
    return OpenCTICapabilitiesResponse(
        enabled=settings.feature_opencti_read,
        configured=configured,
        allowed_entity_types=_csv(settings.opencti_allowed_entity_types),
    )


@router.get("/api/v1/opencti/items/{item_id}/graph", response_model=OpenCTIGraphResponse)
async def opencti_graph(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OpenCTIGraphResponse:
    del principal
    item = await session.get(IntelligenceItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="canonical intelligence item not found")

    statement = (
        select(OpenCTIObjectMapping)
        .where(OpenCTIObjectMapping.item_id == item_id)
        .order_by(OpenCTIObjectMapping.entity_type, OpenCTIObjectMapping.stix_id)
    )
    mappings = list((await session.scalars(statement)).all())
    root_id = f"dtmo:{item.id}"
    nodes = [
        OpenCTIGraphNode(
            id=root_id,
            kind="canonical-intelligence",
            label=item.title,
            entity_type="DTMO Intelligence",
            confidence=item.confidence_score,
        )
    ]
    edges: list[OpenCTIGraphEdge] = []
    for mapping in mappings:
        node_id = f"opencti:{mapping.id}"
        nodes.append(
            OpenCTIGraphNode(
                id=node_id,
                kind="opencti-entity",
                label=mapping.stix_id,
                entity_type=mapping.entity_type,
                stix_id=mapping.stix_id,
                confidence=mapping.confidence,
                markings=list(mapping.markings),
                last_seen_at=mapping.last_seen_at,
            )
        )
        edges.append(
            OpenCTIGraphEdge(
                id=f"mapping:{mapping.id}",
                source=root_id,
                target=node_id,
                relationship_type="canonical-mapping",
                evidence_class="persisted-dtmo-opencti-mapping",
            )
        )

    return OpenCTIGraphResponse(
        item_id=item.id,
        title=item.title,
        nodes=nodes,
        edges=edges,
        topology_scope="persisted canonical DTMO-to-OpenCTI mappings only",
        evidence_boundary=(
            "Only persisted DTMO-to-OpenCTI identity mappings are rendered as edges. DTMO does not currently "
            "persist OpenCTI relationship topology in this boundary, so upstream entity-to-entity relationships "
            "must not be inferred. Graph presence does not prove local exposure, compromise or attribution."
        ),
    )


@router.get("/api/v1/opencti/entities/{mapping_id}", response_model=OpenCTIEntityResponse)
async def opencti_entity(
    mapping_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OpenCTIEntityResponse:
    del principal
    mapping = await session.get(OpenCTIObjectMapping, mapping_id)
    if mapping is None:
        raise HTTPException(status_code=404, detail="OpenCTI mapping not found")
    revisions_statement = (
        select(OpenCTIMappingRevision)
        .where(OpenCTIMappingRevision.mapping_id == mapping.id)
        .order_by(OpenCTIMappingRevision.recorded_at.desc())
    )
    revisions = list((await session.scalars(revisions_statement)).all())
    return OpenCTIEntityResponse(
        mapping_id=mapping.id,
        item_id=mapping.item_id,
        opencti_id=mapping.opencti_id,
        stix_id=mapping.stix_id,
        entity_type=mapping.entity_type,
        parent_types=list(mapping.parent_types),
        markings=list(mapping.markings),
        confidence=mapping.confidence,
        upstream_created_at=mapping.upstream_created_at,
        upstream_updated_at=mapping.upstream_updated_at,
        external_references=list(mapping.external_references),
        provenance=dict(mapping.provenance),
        snapshot_hash=mapping.snapshot_hash,
        last_seen_at=mapping.last_seen_at,
        external_share_authorized=mapping.external_share_authorized,
        local_compromise_proven=mapping.local_compromise_proven,
        revisions=[
            OpenCTIRevisionResponse(
                id=revision.id,
                snapshot_hash=revision.snapshot_hash,
                recorded_at=revision.recorded_at,
                snapshot=dict(revision.snapshot),
            )
            for revision in revisions
        ],
        evidence_boundary=(
            "This is persisted OpenCTI-derived context. It is read-only, grants no publication/share authority "
            "and does not prove local exposure or compromise."
        ),
    )
