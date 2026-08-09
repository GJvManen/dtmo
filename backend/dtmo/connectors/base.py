from __future__ import annotations

import asyncio
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx

from dtmo.config import Settings
from dtmo.logging import get_logger
from dtmo.trace_context import outbound_traceparent


@dataclass(slots=True)
class ConnectorRecord:
    external_id: str
    object_type: str
    title: str
    url: str
    summary: str
    published_at: str | None
    source_reliability: str
    confidence: int
    raw: dict[str, Any]

    @property
    def content_hash(self) -> str:
        value = f"{self.external_id}\n{self.title}\n{self.summary}\n{self.url}"
        return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class ConnectorResult:
    connector_id: str
    started_at: str
    finished_at: str
    records: list[ConnectorRecord]
    attempts: int
    status: str
    error: str | None = None


class Connector(ABC):
    id = "base"
    reliability = "candidate"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.log = get_logger(f"connector.{self.id}")

    @abstractmethod
    async def fetch(self, client: httpx.AsyncClient) -> Any:
        raise NotImplementedError

    @abstractmethod
    def parse(self, payload: Any) -> list[ConnectorRecord]:
        raise NotImplementedError

    async def run(self) -> ConnectorResult:
        started = datetime.now(timezone.utc).isoformat()
        last_error: Exception | None = None
        for attempt in range(1, self.settings.connector_max_attempts + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=self.settings.connector_timeout_seconds,
                    follow_redirects=True,
                    headers={
                        "User-Agent": "DTMO-RC4/1.0",
                        "traceparent": outbound_traceparent(),
                    },
                ) as client:
                    payload = await self.fetch(client)
                records = self.parse(payload)
                return ConnectorResult(
                    connector_id=self.id,
                    started_at=started,
                    finished_at=datetime.now(timezone.utc).isoformat(),
                    records=records,
                    attempts=attempt,
                    status="completed",
                )
            except (httpx.HTTPError, ValueError, KeyError) as exc:
                last_error = exc
                self.log.warning("connector_attempt_failed", attempt=attempt, error=str(exc))
                if attempt < self.settings.connector_max_attempts:
                    await asyncio.sleep(min(2 ** (attempt - 1), 30))
        return ConnectorResult(
            connector_id=self.id,
            started_at=started,
            finished_at=datetime.now(timezone.utc).isoformat(),
            records=[],
            attempts=self.settings.connector_max_attempts,
            status="failed",
            error=str(last_error),
        )
