from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Iterable, Mapping
from uuid import UUID


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def canonical_payload_digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class IngestionContext:
    connector_id: str
    run_id: UUID
    source_uri: str
    fetched_at: datetime
    confidence: int

    def validate(self) -> None:
        if not self.connector_id.strip():
            raise ValueError("connector_id is required")
        if not self.source_uri.startswith("https://"):
            raise ValueError("source_uri must use HTTPS")
        if not 0 <= self.confidence <= 100:
            raise ValueError("confidence must be between 0 and 100")


@dataclass(frozen=True, slots=True)
class CandidateRecord:
    connector_id: str
    run_id: UUID
    external_id: str
    source_uri: str
    source_timestamp: str | None
    fetched_at: datetime
    payload_digest: str
    confidence: int
    raw_evidence: Mapping[str, Any]
    publish_approved: bool = False


@dataclass(frozen=True, slots=True)
class QuarantinedPayload:
    connector_id: str
    run_id: UUID
    reason: str
    source_uri: str
    fetched_at: datetime
    payload_digest: str
    raw_evidence: Any
    external_id: str | None = None
    publish_approved: bool = False


@dataclass(frozen=True, slots=True)
class NormalizationResult:
    candidates: tuple[CandidateRecord, ...]
    quarantined: tuple[QuarantinedPayload, ...]
    publish_approved: bool = False

    @property
    def duplicate_count(self) -> int:
        return sum(item.reason == "duplicate_external_id" for item in self.quarantined)


def normalize_connector_records(
    records: Iterable[Any],
    *,
    context: IngestionContext,
    external_id_field: str,
    source_timestamp_field: str | None = None,
) -> NormalizationResult:
    """Normalize untrusted connector records into governed, non-publishable candidates.

    Malformed and duplicate records fail closed to quarantine. Provenance is copied
    into immutable dataclasses and publication approval is always false.
    """
    context.validate()
    fetched_at = _as_utc(context.fetched_at)
    seen: set[str] = set()
    candidates: list[CandidateRecord] = []
    quarantined: list[QuarantinedPayload] = []

    for raw in records:
        if not isinstance(raw, dict):
            digest = hashlib.sha256(repr(raw).encode("utf-8")).hexdigest()
            quarantined.append(
                QuarantinedPayload(
                    connector_id=context.connector_id,
                    run_id=context.run_id,
                    reason="malformed_record",
                    source_uri=context.source_uri,
                    fetched_at=fetched_at,
                    payload_digest=digest,
                    raw_evidence=raw,
                )
            )
            continue

        digest = canonical_payload_digest(raw)
        external_value = raw.get(external_id_field)
        if not isinstance(external_value, str) or not external_value.strip():
            quarantined.append(
                QuarantinedPayload(
                    connector_id=context.connector_id,
                    run_id=context.run_id,
                    reason="missing_external_id",
                    source_uri=context.source_uri,
                    fetched_at=fetched_at,
                    payload_digest=digest,
                    raw_evidence=raw,
                )
            )
            continue

        external_id = external_value.strip()
        if external_id in seen:
            quarantined.append(
                QuarantinedPayload(
                    connector_id=context.connector_id,
                    run_id=context.run_id,
                    reason="duplicate_external_id",
                    source_uri=context.source_uri,
                    fetched_at=fetched_at,
                    payload_digest=digest,
                    raw_evidence=raw,
                    external_id=external_id,
                )
            )
            continue
        seen.add(external_id)

        source_timestamp: str | None = None
        if source_timestamp_field is not None:
            source_value = raw.get(source_timestamp_field)
            if source_value is not None and (not isinstance(source_value, str) or not source_value.strip()):
                quarantined.append(
                    QuarantinedPayload(
                        connector_id=context.connector_id,
                        run_id=context.run_id,
                        reason="malformed_source_timestamp",
                        source_uri=context.source_uri,
                        fetched_at=fetched_at,
                        payload_digest=digest,
                        raw_evidence=raw,
                        external_id=external_id,
                    )
                )
                continue
            if isinstance(source_value, str):
                source_timestamp = source_value.strip()

        candidates.append(
            CandidateRecord(
                connector_id=context.connector_id,
                run_id=context.run_id,
                external_id=external_id,
                source_uri=context.source_uri,
                source_timestamp=source_timestamp,
                fetched_at=fetched_at,
                payload_digest=digest,
                confidence=context.confidence,
                raw_evidence=raw,
                publish_approved=False,
            )
        )

    return NormalizationResult(candidates=tuple(candidates), quarantined=tuple(quarantined), publish_approved=False)
