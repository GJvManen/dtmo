from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .models import Base


class AuditEventRecord(Base):
    """Persisted immutable audit-chain event."""

    __tablename__ = "audit_event_records"

    sequence_number: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    event_id: Mapped[UUID] = mapped_column(unique=True, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    principal: Mapped[str] = mapped_column(String(255), nullable=False)
    principal_type: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    resource: Mapped[str] = mapped_column(Text, nullable=False)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    request_id: Mapped[str] = mapped_column(String(255), nullable=False)
    provenance_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    event_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __table_args__ = (
        UniqueConstraint("sequence_number", "previous_hash", name="uq_audit_sequence_previous_hash"),
        Index("ix_audit_event_occurred_at", "occurred_at"),
        Index("ix_audit_event_principal_action", "principal", "action"),
    )
