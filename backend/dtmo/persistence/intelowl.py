from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.integrations.intelowl import IntelOwlEnrichmentResult

from .models import IntelligenceItem, IntelOwlEnrichmentRecord


class IntelOwlEnrichmentRepository:
    """Persistence boundary for immutable governed IntelOwl enrichment history."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def persist(
        self,
        *,
        item_id: UUID,
        result: IntelOwlEnrichmentResult,
        handling: str,
        analyzers: list[str],
        requested_by: str,
    ) -> IntelOwlEnrichmentRecord:
        item = await self.session.get(IntelligenceItem, item_id)
        if item is None:
            raise KeyError(item_id)
        if str(item.id) != result.canonical_id:
            raise ValueError("IntelOwl result canonical identity mismatch")

        existing = await self.session.scalar(
            select(IntelOwlEnrichmentRecord).where(
                IntelOwlEnrichmentRecord.item_id == item_id,
                IntelOwlEnrichmentRecord.job_id == result.job_id,
            )
        )
        if existing is not None:
            return existing

        record = IntelOwlEnrichmentRecord(
            item_id=item_id,
            job_id=result.job_id,
            observable_type=result.observable_type,
            observable_value=result.observable_value,
            handling=handling.strip().lower(),
            analyzers=[name.strip() for name in analyzers if name.strip()],
            status=result.status,
            partial=result.partial,
            reports=result.reports,
            raw_result=result.raw,
            requested_by=requested_by,
            external_share_authorized=False,
            local_compromise_proven=False,
        )
        self.session.add(record)
        await self.session.flush()
        # The API returns this record as persisted and immediately supports a
        # canonical history read from a separate request/session. Commit before
        # success so that the returned durability claim cannot race that read.
        await self.session.commit()
        return record

    async def list_for_item(self, item_id: UUID) -> list[IntelOwlEnrichmentRecord]:
        statement = (
            select(IntelOwlEnrichmentRecord)
            .where(IntelOwlEnrichmentRecord.item_id == item_id)
            .order_by(IntelOwlEnrichmentRecord.created_at.desc())
        )
        return list((await self.session.scalars(statement)).all())
