from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class IntelligenceItem(Base):
    __tablename__ = "intelligence_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    source_id: Mapped[str] = mapped_column(String(128), index=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    item_type: Mapped[str] = mapped_column(String(64), index=True)
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
    severity: Mapped[str] = mapped_column(
        String(32),
        default="informational",
        index=True,
    )
    confidence: Mapped[int] = mapped_column(Integer, default=50)
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

    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "external_id",
            name="uq_intelligence_source_external",
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
    confidence: Mapped[int] = mapped_column(Integer, default=50)

    item: Mapped[IntelligenceItem] = relationship(back_populates="provenance")


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
