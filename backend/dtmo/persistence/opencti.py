from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, Boolean, CheckConstraint, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from dtmo.integrations.opencti import OpenCTIItem, OpenCTIPage, OpenCTIReadAdapter

from .models import Base, IntelligenceItem


def utc_now() -> datetime:
    return datetime.now(UTC)


class OpenCTIObjectMapping(Base):
    """Current canonical mapping of one OpenCTI/STIX object to a DTMO item."""

    __tablename__ = "opencti_object_mappings"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("intelligence_items.id", ondelete="CASCADE"), index=True)
    opencti_id: Mapped[str] = mapped_column(String(255), nullable=False)
    stix_id: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    parent_types: Mapped[list[str]] = mapped_column(JSON, default=list)
    markings: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    confidence: Mapped[int | None] = mapped_column(Integer, nullable=True)
    upstream_created_at: Mapped[str | None] = mapped_column(String(64), nullable=True)
    upstream_updated_at: Mapped[str | None] = mapped_column(String(64), nullable=True)
    external_references: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    provenance: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    snapshot_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)
    external_share_authorized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    local_compromise_proven: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("item_id", "opencti_id", name="uq_opencti_mapping_item_opencti"),
        UniqueConstraint("item_id", "stix_id", name="uq_opencti_mapping_item_stix"),
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 100)", name="ck_opencti_mapping_confidence"),
        CheckConstraint("external_share_authorized = false", name="ck_opencti_mapping_no_share_authority"),
        CheckConstraint("local_compromise_proven = false", name="ck_opencti_mapping_no_compromise_proof"),
        Index("ix_opencti_mapping_item_seen", "item_id", "last_seen_at"),
    )


class OpenCTIMappingRevision(Base):
    """Immutable snapshot history for an OpenCTI mapping reconciliation."""

    __tablename__ = "opencti_mapping_revisions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    mapping_id: Mapped[UUID] = mapped_column(ForeignKey("opencti_object_mappings.id", ondelete="CASCADE"), index=True)
    snapshot_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    snapshot: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    __table_args__ = (
        UniqueConstraint("mapping_id", "snapshot_hash", name="uq_opencti_mapping_revision_hash"),
    )


def mapping_snapshot(item: OpenCTIItem) -> dict[str, Any]:
    return {
        "opencti_id": item.opencti_id,
        "stix_id": item.stix_id,
        "entity_type": item.entity_type,
        "parent_types": list(item.parent_types),
        "markings": list(item.markings),
        "confidence": item.confidence,
        "upstream_created_at": item.created_at,
        "upstream_updated_at": item.updated_at,
        "external_references": list(item.external_references),
        "provenance": dict(item.provenance),
        "external_share_authorized": False,
        "local_compromise_proven": False,
    }


def snapshot_hash(snapshot: dict[str, Any]) -> str:
    encoded = json.dumps(snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class OpenCTIMappingRepository:
    """Idempotent persistence boundary for read-only OpenCTI graph context."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def persist_item(self, *, item_id: UUID, item: OpenCTIItem) -> OpenCTIObjectMapping:
        if await self.session.get(IntelligenceItem, item_id) is None:
            raise KeyError(item_id)

        by_opencti = await self.session.scalar(
            select(OpenCTIObjectMapping).where(
                OpenCTIObjectMapping.item_id == item_id,
                OpenCTIObjectMapping.opencti_id == item.opencti_id,
            )
        )
        by_stix = await self.session.scalar(
            select(OpenCTIObjectMapping).where(
                OpenCTIObjectMapping.item_id == item_id,
                OpenCTIObjectMapping.stix_id == item.stix_id,
            )
        )
        if by_opencti is not None and by_opencti.stix_id != item.stix_id:
            raise ValueError("OpenCTI internal identity changed STIX identity")
        if by_stix is not None and by_stix.opencti_id != item.opencti_id:
            raise ValueError("OpenCTI STIX identity changed internal identity")
        if by_opencti is not None and by_stix is not None and by_opencti.id != by_stix.id:
            raise ValueError("OpenCTI identity mapping is ambiguous")

        snapshot = mapping_snapshot(item)
        digest = snapshot_hash(snapshot)
        mapping = by_opencti or by_stix
        if mapping is None:
            mapping = OpenCTIObjectMapping(
                item_id=item_id,
                opencti_id=item.opencti_id,
                stix_id=item.stix_id,
                entity_type=item.entity_type,
                parent_types=list(item.parent_types),
                markings=list(item.markings),
                confidence=item.confidence,
                upstream_created_at=item.created_at,
                upstream_updated_at=item.updated_at,
                external_references=list(item.external_references),
                provenance=dict(item.provenance),
                snapshot_hash=digest,
                external_share_authorized=False,
                local_compromise_proven=False,
            )
            self.session.add(mapping)
            await self.session.flush()
        elif mapping.snapshot_hash != digest:
            mapping.entity_type = item.entity_type
            mapping.parent_types = list(item.parent_types)
            mapping.markings = list(item.markings)
            mapping.confidence = item.confidence
            mapping.upstream_created_at = item.created_at
            mapping.upstream_updated_at = item.updated_at
            mapping.external_references = list(item.external_references)
            mapping.provenance = dict(item.provenance)
            mapping.snapshot_hash = digest
            mapping.last_seen_at = utc_now()

        existing_revision = await self.session.scalar(
            select(OpenCTIMappingRevision).where(
                OpenCTIMappingRevision.mapping_id == mapping.id,
                OpenCTIMappingRevision.snapshot_hash == digest,
            )
        )
        if existing_revision is None:
            self.session.add(OpenCTIMappingRevision(mapping_id=mapping.id, snapshot_hash=digest, snapshot=snapshot))
        mapping.last_seen_at = utc_now()
        await self.session.flush()
        return mapping

    async def persist_page(self, *, item_id: UUID, page: OpenCTIPage) -> list[OpenCTIObjectMapping]:
        return [await self.persist_item(item_id=item_id, item=item) for item in page.items]


class OpenCTIPersistenceCoordinator:
    """Commit DB state before advancing the adapter checkpoint.

    If checkpoint replacement fails after the database commit, replay is safe because
    repository writes are idempotent by stable OpenCTI/STIX identity and snapshot hash.
    """

    def __init__(self, session: AsyncSession, adapter: OpenCTIReadAdapter) -> None:
        self.session = session
        self.adapter = adapter
        self.repository = OpenCTIMappingRepository(session)

    async def persist_and_checkpoint(self, *, item_id: UUID, page: OpenCTIPage) -> list[OpenCTIObjectMapping]:
        mappings = await self.repository.persist_page(item_id=item_id, page=page)
        await self.session.commit()
        self.adapter.commit_page(page)
        return mappings
