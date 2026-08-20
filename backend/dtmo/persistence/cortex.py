from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, JSON, String, Text, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from dtmo.integrations.cortex import CortexAnalysisResult

from .models import Base, IntelligenceItem, utc_now


class CortexAnalysisRecord(Base):
    """Immutable governed record of one completed Cortex analyzer execution."""

    __tablename__ = "cortex_analysis_records"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    item_id: Mapped[UUID] = mapped_column(
        ForeignKey("intelligence_items.id", ondelete="CASCADE"), index=True
    )
    job_id: Mapped[str] = mapped_column(String(255), nullable=False)
    observable_type: Mapped[str] = mapped_column(String(64), nullable=False)
    observable_value: Mapped[str] = mapped_column(Text, nullable=False)
    analyzer_id: Mapped[str] = mapped_column(String(255), nullable=False)
    tlp: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    report: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    raw_result: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)
    external_share_authorized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    local_compromise_proven: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("item_id", "job_id", name="uq_cortex_analysis_item_job"),
        CheckConstraint("tlp >= 0 AND tlp <= 3", name="ck_cortex_analysis_tlp"),
        CheckConstraint(
            "external_share_authorized = false",
            name="ck_cortex_analysis_no_share_authority",
        ),
        CheckConstraint(
            "local_compromise_proven = false",
            name="ck_cortex_analysis_no_compromise_proof",
        ),
        Index("ix_cortex_analysis_item_created", "item_id", "created_at"),
    )


class CortexAnalysisRepository:
    """Persistence boundary for immutable governed Cortex analyzer history."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def persist(
        self,
        *,
        item_id: UUID,
        result: CortexAnalysisResult,
        tlp: int,
        requested_by: str,
    ) -> CortexAnalysisRecord:
        item = await self.session.get(IntelligenceItem, item_id)
        if item is None:
            raise KeyError(item_id)
        if str(item.id) != result.canonical_id:
            raise ValueError("Cortex result canonical identity mismatch")

        existing = await self.session.scalar(
            select(CortexAnalysisRecord).where(
                CortexAnalysisRecord.item_id == item_id,
                CortexAnalysisRecord.job_id == result.job_id,
            )
        )
        if existing is not None:
            return existing

        record = CortexAnalysisRecord(
            item_id=item_id,
            job_id=result.job_id,
            observable_type=result.observable_type.strip().lower(),
            observable_value=result.observable_value,
            analyzer_id=result.analyzer_id.strip(),
            tlp=tlp,
            status=result.status,
            report=result.report,
            raw_result=result.raw,
            requested_by=requested_by,
            external_share_authorized=False,
            local_compromise_proven=False,
        )
        self.session.add(record)
        await self.session.flush()
        return record

    async def list_for_item(self, item_id: UUID) -> list[CortexAnalysisRecord]:
        statement = (
            select(CortexAnalysisRecord)
            .where(CortexAnalysisRecord.item_id == item_id)
            .order_by(CortexAnalysisRecord.created_at.desc())
        )
        return list((await self.session.scalars(statement)).all())
