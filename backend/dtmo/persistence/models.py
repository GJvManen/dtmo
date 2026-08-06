from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from dtmo.intelligence.model import (
    ConfidenceLevel,
    IntelligenceSeverity,
    IntelligenceType,
    SourceReliability,
)


def utc_now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class IntelligenceItem(Base):
    __tablename__ = "intelligence_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    source_id: Mapped[str] = mapped_column(String(128), index=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    item_type: Mapped[IntelligenceType] = mapped_column(
        SAEnum(
            IntelligenceType,
            name="intelligence_type",
            native_enum=False,
            validate_strings=True,
        ),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(500))
    summary: Mapped[str] = mapped_column(Text, default="")
    canonical_url: Mapped[str] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    severity: Mapped[IntelligenceSeverity] = mapped_column(
        SAEnum(
            IntelligenceSeverity,
            name="intelligence_severity",
            native_enum=False,
            validate_strings=True,
        ),
        default=IntelligenceSeverity.INFORMATIONAL,
        index=True,
    )
    confidence_score: Mapped[int] = mapped_column(Integer, default=50)
    confidence_level: Mapped[ConfidenceLevel] = mapped_column(
        SAEnum(
            ConfidenceLevel,
            name="confidence_level",
            native_enum=False,
            validate_strings=True,
        ),
        default=ConfidenceLevel.MEDIUM,
        index=True,
    )
    confidence_rationale: Mapped[list[str]] = mapped_column(JSON, default=list)
    education_relevance: Mapped[int] = mapped_column(Integer, default=0, index=True)
    review_status: Mapped[str] = mapped_column(
        String(32),
        default="candidate",
        index=True,
    )
    share_approved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    provenance: Mapped[list[ProvenanceRecord]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
    )
    revisions: Mapped[list[IntelligenceRevision]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
        order_by="IntelligenceRevision.revision_number",
    )

    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "external_id",
            name="uq_intelligence_source_external",
        ),
        CheckConstraint(
            "confidence_score >= 0 AND confidence_score <= 100",
            name="ck_intelligence_confidence_score",
        ),
        CheckConstraint(
            "education_relevance >= 0 AND education_relevance <= 100",
            name="ck_intelligence_education_relevance",
        ),
        Index(
            "ix_intelligence_priority",
            "severity",
            "education_relevance",
            "review_status",
        ),
    )


class ProvenanceRecord(Base):
    __tablename__ = "provenance_records"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    item_id: Mapped[UUID] = mapped_column(
        ForeignKey("intelligence_items.id", ondelete="CASCADE"),
        index=True,
    )
    source_url: Mapped[str] = mapped_column(Text)
    source_title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    content_hash: Mapped[str] = mapped_column(String(64))
    exact_passage: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_reliability: Mapped[SourceReliability] = mapped_column(
        SAEnum(
            SourceReliability,
            name="source_reliability",
            native_enum=False,
            validate_strings=True,
        ),
        default=SourceReliability.UNKNOWN,
        index=True,
    )
    is_primary_source: Mapped[bool] = mapped_column(Boolean, default=False)
    content_integrity_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence_score: Mapped[int] = mapped_column(Integer, default=50)

    item: Mapped[IntelligenceItem] = relationship(back_populates="provenance")

    __table_args__ = (
        CheckConstraint(
            "confidence_score >= 0 AND confidence_score <= 100",
            name="ck_provenance_confidence_score",
        ),
        UniqueConstraint(
            "item_id",
            "source_url",
            "content_hash",
            name="uq_provenance_item_source_content",
        ),
    )


class IntelligenceRevision(Base):
    """Immutable snapshot metadata for a canonical intelligence item revision."""

    __tablename__ = "intelligence_revisions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    item_id: Mapped[UUID] = mapped_column(
        ForeignKey("intelligence_items.id", ondelete="CASCADE"),
        index=True,
    )
    revision_number: Mapped[int] = mapped_column(Integer)
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    snapshot: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    created_by: Mapped[str] = mapped_column(String(255), default="system")
    change_reason: Mapped[str] = mapped_column(Text, default="ingestion")

    item: Mapped[IntelligenceItem] = relationship(back_populates="revisions")

    __table_args__ = (
        CheckConstraint(
            "revision_number >= 1",
            name="ck_intelligence_revision_number",
        ),
        UniqueConstraint(
            "item_id",
            "revision_number",
            name="uq_intelligence_item_revision",
        ),
        UniqueConstraint(
            "item_id",
            "content_hash",
            name="uq_intelligence_item_revision_hash",
        ),
    )


class ConnectorRun(Base):
    __tablename__ = "connector_runs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    connector_id: Mapped[str] = mapped_column(String(128), index=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(32), index=True)
    fetched: Mapped[int] = mapped_column(Integer, default=0)
    inserted: Mapped[int] = mapped_column(Integer, default=0)
    duplicates: Mapped[int] = mapped_column(Integer, default=0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
