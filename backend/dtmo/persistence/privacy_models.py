from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from .models import Base


class MinimizedAuditProjectionRecord(Base):
    """Privacy-minimized, purgeable projection of immutable audit evidence."""

    __tablename__ = "minimized_audit_projection_records"

    event_id: Mapped[UUID] = mapped_column(primary_key=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    principal_reference: Mapped[str] = mapped_column(String(96), nullable=False)
    principal_type: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_reference: Mapped[str] = mapped_column(String(96), nullable=False)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    request_reference: Mapped[str] = mapped_column(String(96), nullable=False)
    source_event_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    legal_hold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_minimized_projection_expires_hold", "expires_at", "legal_hold"),
    )
