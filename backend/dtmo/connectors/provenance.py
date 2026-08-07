from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Iterable, Mapping, Protocol
from uuid import UUID


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _parse_source_timestamp(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    return _as_utc(parsed)


def canonical_payload_digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class ReplayRegistry(Protocol):
    def claim(
        self,
        *,
        connector_id: str,
        external_id: str,
        payload_digest: str,
        run_id: UUID,
        source_uri: str,
        observed_at: datetime | None = None,
    ) -> bool: ...


@dataclass(frozen=True, slots=True)
class SourceFreshnessPolicy:
    max_age: timedelta
    max_future_skew: timedelta = timedelta(minutes=5)
    allow_missing: bool = False

    def validate(self) -> None:
        if self.max_age <= timedelta(0):
            raise ValueError("max_age must be positive")
        if self.max_future_skew < timedelta(0):
            raise ValueError("max_future_skew cannot be negative")


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
    source_timestamp_utc: datetime | None
    freshness_status: str
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
    source_timestamp: str | None = None
    source_timestamp_utc: datetime | None = None
    freshness_status: str | None = None
    publish_approved: bool = False


@dataclass(frozen=True, slots=True)
class NormalizationResult:
    candidates: tuple[CandidateRecord, ...]
    quarantined: tuple[QuarantinedPayload, ...]
    publish_approved: bool = False

    @property
    def duplicate_count(self) -> int:
        return sum(item.reason in {"duplicate_external_id", "replayed_record"} for item in self.quarantined)


def normalize_connector_records(
    records: Iterable[Any],
    *,
    context: IngestionContext,
    external_id_field: str,
    source_timestamp_field: str | None = None,
    freshness_policy: SourceFreshnessPolicy | None = None,
    replay_registry: ReplayRegistry | None = None,
) -> NormalizationResult:
    """Normalize untrusted connector records into governed, non-publishable candidates.

    Malformed, duplicate, replayed, stale, invalid-time and excessive future-skew
    records fail closed to quarantine. Provenance is copied into immutable dataclasses
    and publication approval is always false.
    """
    context.validate()
    if freshness_policy is not None:
        freshness_policy.validate()
        if source_timestamp_field is None:
            raise ValueError("freshness_policy requires source_timestamp_field")

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
        source_timestamp_utc: datetime | None = None
        freshness_status = "not_evaluated"
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
                        freshness_status="invalid",
                    )
                )
                continue
            if isinstance(source_value, str):
                source_timestamp = source_value.strip()
                try:
                    source_timestamp_utc = _parse_source_timestamp(source_timestamp)
                except ValueError:
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
                            source_timestamp=source_timestamp,
                            freshness_status="invalid",
                        )
                    )
                    continue

        if freshness_policy is not None:
            if source_timestamp_utc is None:
                if not freshness_policy.allow_missing:
                    quarantined.append(
                        QuarantinedPayload(
                            connector_id=context.connector_id,
                            run_id=context.run_id,
                            reason="missing_source_timestamp",
                            source_uri=context.source_uri,
                            fetched_at=fetched_at,
                            payload_digest=digest,
                            raw_evidence=raw,
                            external_id=external_id,
                            freshness_status="missing",
                        )
                    )
                    continue
                freshness_status = "missing_allowed"
            elif source_timestamp_utc > fetched_at + freshness_policy.max_future_skew:
                quarantined.append(
                    QuarantinedPayload(
                        connector_id=context.connector_id,
                        run_id=context.run_id,
                        reason="future_source_timestamp",
                        source_uri=context.source_uri,
                        fetched_at=fetched_at,
                        payload_digest=digest,
                        raw_evidence=raw,
                        external_id=external_id,
                        source_timestamp=source_timestamp,
                        source_timestamp_utc=source_timestamp_utc,
                        freshness_status="future_skew",
                    )
                )
                continue
            elif fetched_at - source_timestamp_utc > freshness_policy.max_age:
                quarantined.append(
                    QuarantinedPayload(
                        connector_id=context.connector_id,
                        run_id=context.run_id,
                        reason="stale_source_timestamp",
                        source_uri=context.source_uri,
                        fetched_at=fetched_at,
                        payload_digest=digest,
                        raw_evidence=raw,
                        external_id=external_id,
                        source_timestamp=source_timestamp,
                        source_timestamp_utc=source_timestamp_utc,
                        freshness_status="stale",
                    )
                )
                continue
            else:
                freshness_status = "fresh"

        if replay_registry is not None and not replay_registry.claim(
            connector_id=context.connector_id,
            external_id=external_id,
            payload_digest=digest,
            run_id=context.run_id,
            source_uri=context.source_uri,
            observed_at=fetched_at,
        ):
            quarantined.append(
                QuarantinedPayload(
                    connector_id=context.connector_id,
                    run_id=context.run_id,
                    reason="replayed_record",
                    source_uri=context.source_uri,
                    fetched_at=fetched_at,
                    payload_digest=digest,
                    raw_evidence=raw,
                    external_id=external_id,
                    source_timestamp=source_timestamp,
                    source_timestamp_utc=source_timestamp_utc,
                    freshness_status=freshness_status,
                )
            )
            continue

        candidates.append(
            CandidateRecord(
                connector_id=context.connector_id,
                run_id=context.run_id,
                external_id=external_id,
                source_uri=context.source_uri,
                source_timestamp=source_timestamp,
                source_timestamp_utc=source_timestamp_utc,
                freshness_status=freshness_status,
                fetched_at=fetched_at,
                payload_digest=digest,
                confidence=context.confidence,
                raw_evidence=raw,
                publish_approved=False,
            )
        )

    return NormalizationResult(candidates=tuple(candidates), quarantined=tuple(quarantined), publish_approved=False)
