from __future__ import annotations

import asyncio
import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Awaitable, Callable

import httpx


@dataclass(frozen=True, slots=True)
class CanaryPolicy:
    connector_id: str
    source_url: str
    licence: str
    terms_url: str
    source_reliability: str = "authoritative"
    timeout_seconds: float = 10.0
    max_attempts: int = 3
    minimum_interval_seconds: float = 1.0
    maximum_records: int = 500

    def __post_init__(self) -> None:
        if not self.connector_id.strip():
            raise ValueError("connector_id is required")
        if not self.source_url.startswith("https://"):
            raise ValueError("source_url must use HTTPS")
        if not self.terms_url.startswith("https://"):
            raise ValueError("terms_url must use HTTPS")
        if not self.licence.strip():
            raise ValueError("licence is required")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if not 1 <= self.max_attempts <= 5:
            raise ValueError("max_attempts must be between 1 and 5")
        if self.minimum_interval_seconds < 0:
            raise ValueError("minimum_interval_seconds cannot be negative")
        if not 1 <= self.maximum_records <= 5000:
            raise ValueError("maximum_records must be between 1 and 5000")


@dataclass(frozen=True, slots=True)
class CanaryRecord:
    external_id: str
    title: str
    published_at: str
    source_url: str
    source_reliability: str
    confidence: int
    raw_evidence: dict[str, Any]

    @property
    def evidence_hash(self) -> str:
        payload = repr(sorted(self.raw_evidence.items())).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class QuarantinedRecord:
    reason: str
    raw_evidence: Any


@dataclass(slots=True)
class CanaryEvidence:
    connector_id: str
    source_url: str
    licence: str
    terms_url: str
    started_at: str
    finished_at: str
    attempts: int
    status: str
    records: list[CanaryRecord] = field(default_factory=list)
    quarantined: list[QuarantinedRecord] = field(default_factory=list)
    duplicate_count: int = 0
    publish_approved: bool = False
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "connector_id": self.connector_id,
            "source_url": self.source_url,
            "licence": self.licence,
            "terms_url": self.terms_url,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "attempts": self.attempts,
            "status": self.status,
            "record_count": len(self.records),
            "quarantine_count": len(self.quarantined),
            "duplicate_count": self.duplicate_count,
            "publish_approved": self.publish_approved,
            "records": [
                {
                    "external_id": record.external_id,
                    "title": record.title,
                    "published_at": record.published_at,
                    "source_url": record.source_url,
                    "source_reliability": record.source_reliability,
                    "confidence": record.confidence,
                    "evidence_hash": record.evidence_hash,
                }
                for record in self.records
            ],
            "quarantined": [
                {"reason": item.reason, "raw_evidence": item.raw_evidence}
                for item in self.quarantined
            ],
            "error": self.error,
        }


Parser = Callable[[Any, CanaryPolicy], tuple[list[CanaryRecord], list[QuarantinedRecord], int]]
Sleep = Callable[[float], Awaitable[None]]


async def run_live_canary(
    policy: CanaryPolicy,
    parser: Parser,
    *,
    transport: httpx.AsyncBaseTransport | None = None,
    sleep: Sleep = asyncio.sleep,
) -> CanaryEvidence:
    started = datetime.now(UTC).isoformat()
    last_error: Exception | None = None

    for attempt in range(1, policy.max_attempts + 1):
        if attempt > 1:
            delay = min(policy.minimum_interval_seconds * (2 ** (attempt - 2)), 30.0)
            await sleep(delay)
        try:
            async with httpx.AsyncClient(
                timeout=policy.timeout_seconds,
                follow_redirects=False,
                transport=transport,
                headers={"User-Agent": "DTMO-connector-canary/1.0"},
            ) as client:
                response = await client.get(policy.source_url)
                response.raise_for_status()
                payload = response.json()
            records, quarantined, duplicate_count = parser(payload, policy)
            if len(records) > policy.maximum_records:
                overflow = records[policy.maximum_records :]
                quarantined.extend(
                    QuarantinedRecord(reason="record_limit_exceeded", raw_evidence=item.raw_evidence)
                    for item in overflow
                )
                records = records[: policy.maximum_records]
            return CanaryEvidence(
                connector_id=policy.connector_id,
                source_url=policy.source_url,
                licence=policy.licence,
                terms_url=policy.terms_url,
                started_at=started,
                finished_at=datetime.now(UTC).isoformat(),
                attempts=attempt,
                status="completed",
                records=records,
                quarantined=quarantined,
                duplicate_count=duplicate_count,
                publish_approved=False,
            )
        except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
            last_error = exc

    return CanaryEvidence(
        connector_id=policy.connector_id,
        source_url=policy.source_url,
        licence=policy.licence,
        terms_url=policy.terms_url,
        started_at=started,
        finished_at=datetime.now(UTC).isoformat(),
        attempts=policy.max_attempts,
        status="failed",
        publish_approved=False,
        error=str(last_error),
    )


def parse_cisa_kev(payload: Any, policy: CanaryPolicy) -> tuple[list[CanaryRecord], list[QuarantinedRecord], int]:
    if not isinstance(payload, dict):
        raise ValueError("CISA KEV payload must be an object")
    vulnerabilities = payload.get("vulnerabilities")
    if not isinstance(vulnerabilities, list):
        raise ValueError("CISA KEV vulnerabilities must be a list")

    accepted: list[CanaryRecord] = []
    quarantined: list[QuarantinedRecord] = []
    seen: set[str] = set()
    duplicate_count = 0

    for raw in vulnerabilities:
        if not isinstance(raw, dict):
            quarantined.append(QuarantinedRecord("malformed_record", raw))
            continue
        cve_value = raw.get("cveID")
        title_value = raw.get("vulnerabilityName")
        published_at_value = raw.get("dateAdded")
        if (
            not isinstance(cve_value, str)
            or not cve_value.strip()
            or not isinstance(title_value, str)
            or not title_value.strip()
            or not isinstance(published_at_value, str)
            or not published_at_value.strip()
        ):
            quarantined.append(QuarantinedRecord("missing_required_provenance", raw))
            continue

        cve = cve_value
        title = title_value
        published_at = published_at_value
        if cve in seen:
            duplicate_count += 1
            quarantined.append(QuarantinedRecord("duplicate_external_id", raw))
            continue
        seen.add(cve)
        accepted.append(
            CanaryRecord(
                external_id=cve,
                title=title,
                published_at=published_at,
                source_url=policy.source_url,
                source_reliability=policy.source_reliability,
                confidence=95,
                raw_evidence=raw,
            )
        )

    return accepted, quarantined, duplicate_count
