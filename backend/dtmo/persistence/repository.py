from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ConnectorRun, IntelligenceItem, ProvenanceRecord


class IntelligenceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def ingest_candidate(self, payload: dict[str, Any]) -> tuple[IntelligenceItem, bool]:
        source_id = str(payload["source_id"])
        external_id = payload.get("external_id")
        existing = None
        if external_id:
            existing = await self.session.scalar(
                select(IntelligenceItem).where(
                    IntelligenceItem.source_id == source_id,
                    IntelligenceItem.external_id == str(external_id),
                )
            )
        content_hash = payload.get("content_hash") or sha256(
            f"{payload.get('title', '')}\n{payload.get('summary', '')}".encode()
        ).hexdigest()
        if existing is not None:
            return existing, False

        item = IntelligenceItem(
            source_id=source_id,
            external_id=str(external_id) if external_id is not None else None,
            item_type=str(payload.get("item_type", "article")),
            title=str(payload["title"]),
            summary=str(payload.get("summary", "")),
            canonical_url=str(payload["canonical_url"]),
            published_at=payload.get("published_at"),
            content_hash=content_hash,
            severity=str(payload.get("severity", "informational")),
            confidence=int(payload.get("confidence", 50)),
            education_relevance=int(payload.get("education_relevance", 0)),
            review_status="candidate",
            share_approved=False,
            tags=list(payload.get("tags", [])),
            metadata_json=dict(payload.get("metadata", {})),
        )
        self.session.add(item)
        await self.session.flush()
        for source in payload.get("provenance", []):
            self.session.add(
                ProvenanceRecord(
                    item_id=item.id,
                    source_url=str(source["source_url"]),
                    source_title=source.get("source_title"),
                    publisher=source.get("publisher"),
                    content_hash=str(source.get("content_hash", content_hash)),
                    exact_passage=source.get("exact_passage"),
                    confidence=int(source.get("confidence", item.confidence)),
                )
            )
        return item, True

    async def approve_for_sharing(self, item_id: object, reviewer: str) -> IntelligenceItem:
        item = await self.session.get(IntelligenceItem, item_id)
        if item is None:
            raise KeyError(item_id)
        if item.review_status != "reviewed":
            raise ValueError("share approval requires reviewed intelligence")
        item.share_approved = True
        item.metadata_json = {**item.metadata_json, "share_approved_by": reviewer}
        await self.session.flush()
        return item


class ConnectorRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def start(self, connector_id: str) -> ConnectorRun:
        run = ConnectorRun(connector_id=connector_id, status="running")
        self.session.add(run)
        await self.session.flush()
        return run

    async def finish(
        self,
        run: ConnectorRun,
        *,
        fetched: int,
        inserted: int,
        duplicates: int,
        errors: Iterable[str] = (),
    ) -> ConnectorRun:
        error_list = list(errors)
        now = datetime.now(UTC)
        run.finished_at = now
        run.status = "completed" if not error_list else "degraded"
        run.fetched = fetched
        run.inserted = inserted
        run.duplicates = duplicates
        run.error_count = len(error_list)
        run.details = {"errors": error_list}
        run.duration_seconds = max(0.0, (now - run.started_at).total_seconds())
        await self.session.flush()
        return run
