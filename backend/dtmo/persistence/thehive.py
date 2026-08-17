from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, Boolean, CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from dtmo.integrations.thehive import TheHiveCaseResult
from dtmo.persistence.models import Base, IntelligenceItem


def utc_now() -> datetime:
    return datetime.now(UTC)


class TheHiveHandoffState(Base):
    """Durable reservation and reconciliation state for one human-approved case handoff."""

    __tablename__ = "thehive_handoff_state"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(nullable=False)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("intelligence_items.id", ondelete="CASCADE"), nullable=False, index=True)
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False)
    organization: Mapped[str] = mapped_column(String(255), nullable=False)
    tlp: Mapped[str] = mapped_column(String(32), nullable=False)
    pap: Mapped[str] = mapped_column(String(32), nullable=False)
    authority_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="reserved", index=True)
    thehive_case_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    thehive_case_number: Mapped[str | None] = mapped_column(String(64), nullable=True)
    outcome: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    error_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    external_share_authorized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    local_compromise_proven: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("request_id", name="uq_thehive_handoff_request"),
        UniqueConstraint("thehive_case_id", name="uq_thehive_handoff_case"),
        CheckConstraint("status IN ('reserved','delivered','ambiguous','failed')", name="ck_thehive_handoff_status"),
        CheckConstraint("external_share_authorized = false", name="ck_thehive_handoff_no_share_authority"),
        CheckConstraint("local_compromise_proven = false", name="ck_thehive_handoff_no_compromise_proof"),
        Index("ix_thehive_handoff_item_created", "item_id", "created_at"),
    )


class TheHiveHandoffRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def reserve(
        self,
        *,
        request_id: UUID,
        item_id: UUID,
        requested_by: str,
        organization: str,
        tlp: str,
        pap: str,
        authority_snapshot: dict[str, Any],
    ) -> TheHiveHandoffState:
        if await self.session.get(IntelligenceItem, item_id) is None:
            raise KeyError(item_id)
        existing = await self.session.scalar(select(TheHiveHandoffState).where(TheHiveHandoffState.request_id == request_id))
        if existing is not None:
            if existing.item_id != item_id or existing.requested_by != requested_by or existing.organization != organization:
                raise ValueError("TheHive handoff request identity conflicts with existing reservation")
            if existing.status in {"delivered", "ambiguous"}:
                raise ValueError(f"TheHive handoff request is already {existing.status}; reconciliation required")
            return existing
        state = TheHiveHandoffState(
            request_id=request_id,
            item_id=item_id,
            requested_by=requested_by,
            organization=organization,
            tlp=tlp,
            pap=pap,
            authority_snapshot=authority_snapshot,
            status="reserved",
            external_share_authorized=False,
            local_compromise_proven=False,
        )
        self.session.add(state)
        await self.session.commit()
        await self.session.refresh(state)
        return state

    async def mark_delivered(self, state: TheHiveHandoffState, result: TheHiveCaseResult) -> TheHiveHandoffState:
        state.status = "delivered"
        state.thehive_case_id = result.case_id
        state.thehive_case_number = str(result.case_number) if result.case_number is not None else None
        state.outcome = {
            "case_id": result.case_id,
            "case_number": result.case_number,
            "organization": result.organization,
        }
        state.error_detail = None
        state.updated_at = utc_now()
        await self.session.commit()
        await self.session.refresh(state)
        return state

    async def mark_ambiguous(self, state: TheHiveHandoffState, detail: str) -> TheHiveHandoffState:
        state.status = "ambiguous"
        state.error_detail = detail[:2000]
        state.updated_at = utc_now()
        await self.session.commit()
        await self.session.refresh(state)
        return state

    async def mark_failed(self, state: TheHiveHandoffState, detail: str) -> TheHiveHandoffState:
        state.status = "failed"
        state.error_detail = detail[:2000]
        state.updated_at = utc_now()
        await self.session.commit()
        await self.session.refresh(state)
        return state

    async def list_for_item(self, item_id: UUID) -> list[TheHiveHandoffState]:
        rows = await self.session.scalars(
            select(TheHiveHandoffState).where(TheHiveHandoffState.item_id == item_id).order_by(TheHiveHandoffState.created_at.desc())
        )
        return list(rows)
