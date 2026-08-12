from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, CheckConstraint, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .models import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class GovernanceFramework(Base):
    __tablename__ = "governance_frameworks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(64), nullable=False)
    version_label: Mapped[str] = mapped_column(String(255), nullable=False)
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
    authority: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    coverage_mode: Mapped[str] = mapped_column(String(32), nullable=False, default="mapping")
    expected_object_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    last_verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        CheckConstraint("coverage_mode IN ('mapping', 'context_only')", name="ck_governance_framework_coverage_mode"),
    )


class IntelligenceFrameworkMapping(Base):
    __tablename__ = "intelligence_framework_mappings"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    framework_id: Mapped[str] = mapped_column(ForeignKey("governance_frameworks.id", ondelete="RESTRICT"), index=True)
    framework_version: Mapped[str] = mapped_column(String(64), nullable=False)
    object_type: Mapped[str] = mapped_column(String(32), nullable=False)
    object_id: Mapped[str] = mapped_column(String(128), nullable=False)
    object_title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    intelligence_id: Mapped[UUID] = mapped_column(ForeignKey("intelligence_items.id", ondelete="CASCADE"), index=True)
    mapping_status: Mapped[str] = mapped_column(String(32), nullable=False, default="mapped")
    provenance_reference: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, nullable=False)
    mapping_reason: Mapped[str] = mapped_column(Text, nullable=False)
    review_state: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("object_type IN ('control', 'technique', 'category', 'scoring_context')", name="ck_framework_mapping_object_type"),
        CheckConstraint("mapping_status IN ('mapped', 'context_only')", name="ck_framework_mapping_status"),
        CheckConstraint("review_state IN ('pending', 'approved', 'rejected')", name="ck_framework_mapping_review_state"),
        CheckConstraint("confidence_score >= 0 AND confidence_score <= 100", name="ck_framework_mapping_confidence"),
        UniqueConstraint("framework_id", "framework_version", "object_type", "object_id", "intelligence_id", name="uq_framework_mapping_target_intelligence"),
        Index("ix_framework_mapping_framework_review", "framework_id", "review_state"),
        Index("ix_framework_mapping_object", "framework_id", "object_type", "object_id"),
    )
