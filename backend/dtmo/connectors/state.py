from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, Float, ForeignKey, Index, Integer, JSON, String, UniqueConstraint, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from dtmo.persistence.models import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


def as_utc(value: datetime) -> datetime:
    """Return an aware UTC datetime, including for drivers that drop tzinfo."""
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


class ConnectorRuntimeState(Base):
    __tablename__ = "connector_runtime_states"

    connector_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    last_run_id: Mapped[UUID | None] = mapped_column(nullable=True)
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_failure_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    consecutive_failures: Mapped[int] = mapped_column(Integer, default=0)
    circuit_open_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    health_status: Mapped[str] = mapped_column(String(32), default="unknown", index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    __table_args__ = (
        CheckConstraint("consecutive_failures >= 0", name="ck_connector_state_failures_nonnegative"),
        CheckConstraint(
            "health_status IN ('unknown', 'healthy', 'degraded', 'isolated')",
            name="ck_connector_state_health_status",
        ),
    )


class ConnectorHealthEvent(Base):
    __tablename__ = "connector_health_events"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    connector_id: Mapped[str] = mapped_column(
        ForeignKey("connector_runtime_states.connector_id", ondelete="RESTRICT"), index=True
    )
    run_id: Mapped[UUID] = mapped_column(index=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    status: Mapped[str] = mapped_column(String(32), index=True)
    duration_seconds: Mapped[float] = mapped_column(Float, default=0.0)
    record_count: Mapped[int] = mapped_column(Integer, default=0)
    quarantine_count: Mapped[int] = mapped_column(Integer, default=0)
    error_code: Mapped[str | None] = mapped_column(String(128), nullable=True)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    publish_approved: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint("connector_id", "run_id", name="uq_connector_health_run"),
        CheckConstraint("status IN ('success', 'failure')", name="ck_connector_health_status"),
        CheckConstraint("duration_seconds >= 0", name="ck_connector_health_duration"),
        CheckConstraint("record_count >= 0", name="ck_connector_health_record_count"),
        CheckConstraint("quarantine_count >= 0", name="ck_connector_health_quarantine_count"),
        CheckConstraint("publish_approved = false", name="ck_connector_health_never_publishes"),
        Index("ix_connector_health_history", "connector_id", "observed_at"),
    )


class ConnectorQuarantineRecord(Base):
    __tablename__ = "connector_quarantine_records"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    connector_id: Mapped[str] = mapped_column(String(128), index=True)
    run_id: Mapped[UUID] = mapped_column(index=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reason: Mapped[str] = mapped_column(String(128), index=True)
    raw_evidence_hash: Mapped[str] = mapped_column(String(64))
    raw_evidence: Mapped[dict[str, Any]] = mapped_column(JSON)
    quarantined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    recovery_status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    recovered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    recovered_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    review_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    publish_approved: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint(
            "connector_id", "run_id", "raw_evidence_hash", name="uq_connector_quarantine_evidence"
        ),
        CheckConstraint(
            "recovery_status IN ('pending', 'released_to_candidate', 'rejected')",
            name="ck_connector_quarantine_recovery_status",
        ),
        CheckConstraint(
            "(recovery_status = 'pending' AND recovered_at IS NULL AND recovered_by IS NULL AND review_reference IS NULL) OR "
            "(recovery_status != 'pending' AND recovered_at IS NOT NULL AND recovered_by IS NOT NULL AND review_reference IS NOT NULL)",
            name="ck_connector_quarantine_recovery_evidence",
        ),
        CheckConstraint("publish_approved = false", name="ck_connector_quarantine_never_publishes"),
        Index("ix_connector_quarantine_pending", "connector_id", "recovery_status", "quarantined_at"),
    )


@dataclass(frozen=True, slots=True)
class QuarantineInput:
    reason: str
    raw_evidence: dict[str, Any]
    external_id: str | None = None

    @property
    def evidence_hash(self) -> str:
        payload = repr(sorted(self.raw_evidence.items())).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


class ConnectorStateStore:
    def __init__(self, session: Session, *, failure_threshold: int = 3, isolation_minutes: int = 15) -> None:
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be positive")
        if isolation_minutes < 1:
            raise ValueError("isolation_minutes must be positive")
        self.session = session
        self.failure_threshold = failure_threshold
        self.isolation_minutes = isolation_minutes

    def is_isolated(self, connector_id: str, *, now: datetime | None = None) -> bool:
        state = self.session.get(ConnectorRuntimeState, connector_id)
        current = as_utc(now or utc_now())
        return bool(
            state
            and state.circuit_open_until
            and as_utc(state.circuit_open_until) > current
        )

    def record_run(
        self,
        *,
        connector_id: str,
        run_id: UUID,
        succeeded: bool,
        duration_seconds: float,
        record_count: int,
        quarantined: list[QuarantineInput],
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
        observed_at: datetime | None = None,
    ) -> ConnectorRuntimeState:
        if not connector_id.strip():
            raise ValueError("connector_id is required")
        if duration_seconds < 0 or record_count < 0:
            raise ValueError("run counters cannot be negative")
        observed = as_utc(observed_at or utc_now())
        state = self.session.get(ConnectorRuntimeState, connector_id)
        if state is None:
            state = ConnectorRuntimeState(
                connector_id=connector_id,
                consecutive_failures=0,
                health_status="unknown",
                updated_at=observed,
            )
            self.session.add(state)

        state.last_run_id = run_id
        state.updated_at = observed
        if succeeded:
            state.last_success_at = observed
            state.consecutive_failures = 0
            state.circuit_open_until = None
            state.health_status = "healthy"
        else:
            state.last_failure_at = observed
            state.consecutive_failures += 1
            if state.consecutive_failures >= self.failure_threshold:
                state.circuit_open_until = observed + timedelta(minutes=self.isolation_minutes)
                state.health_status = "isolated"
            else:
                state.health_status = "degraded"

        self.session.add(
            ConnectorHealthEvent(
                connector_id=connector_id,
                run_id=run_id,
                observed_at=observed,
                status="success" if succeeded else "failure",
                duration_seconds=duration_seconds,
                record_count=record_count,
                quarantine_count=len(quarantined),
                error_code=error_code,
                details=details or {},
                publish_approved=False,
            )
        )
        for item in quarantined:
            self.session.add(
                ConnectorQuarantineRecord(
                    connector_id=connector_id,
                    run_id=run_id,
                    external_id=item.external_id,
                    reason=item.reason,
                    raw_evidence_hash=item.evidence_hash,
                    raw_evidence=item.raw_evidence,
                    recovery_status="pending",
                    publish_approved=False,
                )
            )
        self.session.commit()
        self.session.refresh(state)
        return state

    def recover_quarantine(
        self,
        record_id: UUID,
        *,
        decision: str,
        human_reviewer: str,
        review_reference: str,
        recovered_at: datetime | None = None,
    ) -> ConnectorQuarantineRecord:
        if decision not in {"released_to_candidate", "rejected"}:
            raise ValueError("invalid quarantine recovery decision")
        if not human_reviewer.strip() or human_reviewer.startswith("service:"):
            raise ValueError("a human reviewer is required")
        if not review_reference.strip():
            raise ValueError("review_reference is required")
        record = self.session.get(ConnectorQuarantineRecord, record_id)
        if record is None:
            raise LookupError("quarantine record not found")
        if record.recovery_status != "pending":
            raise ValueError("quarantine record already decided")
        record.recovery_status = decision
        record.recovered_at = as_utc(recovered_at or utc_now())
        record.recovered_by = human_reviewer
        record.review_reference = review_reference
        record.publish_approved = False
        self.session.commit()
        self.session.refresh(record)
        return record

    def health_history(self, connector_id: str, *, limit: int = 100) -> list[ConnectorHealthEvent]:
        if not 1 <= limit <= 1000:
            raise ValueError("limit must be between 1 and 1000")
        statement = (
            select(ConnectorHealthEvent)
            .where(ConnectorHealthEvent.connector_id == connector_id)
            .order_by(ConnectorHealthEvent.observed_at.desc())
            .limit(limit)
        )
        return list(self.session.scalars(statement))
