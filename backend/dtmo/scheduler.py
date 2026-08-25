from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from functools import partial
from uuid import uuid4

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from dtmo.alerts import connector_alerts
from dtmo.audit import AuditDecision
from dtmo.audit.store import append_persistent_audit_event
from dtmo.connectors.base import ConnectorResult
from dtmo.connectors.state import ConnectorRuntimeState, ConnectorStateStore, as_utc
from dtmo.logging import get_logger
from dtmo.source_catalog import catalog_by_id
from dtmo.source_framework import SOURCE_ADAPTER_REGISTRY, execute_source
from dtmo.sources import SourceDefinition, SourceRegistry

_REGISTERED_SOURCE_RECONCILIATION_SECONDS = 60


@dataclass(slots=True)
class ScheduledJob:
    id: str
    interval_seconds: int
    handler: Callable[[], Awaitable[object]]
    run_immediately: bool = False


def _automatic_source_eligibility(source: SourceDefinition) -> tuple[bool, str]:
    """Return whether a persisted source is safe to execute automatically.

    Automatic collection is intentionally narrower than manual execution. Only
    enabled, code-reviewed catalog sources with an implemented supported adapter
    are eligible. Built-in CISA KEV remains owned by its dedicated connector path.
    Credentialed adapters additionally require a logical secret reference; the
    actual secret value remains runtime/server-side and is never exposed here.
    """
    if not source.enabled:
        return False, "disabled"
    if source.source_type == "cisa-kev" or source.id == "cisa-kev":
        return False, "built-in-execution-path"
    catalog = catalog_by_id(source.id)
    if catalog is None or catalog.execution_status != "supported":
        return False, "unsupported-or-research-only"
    spec = SOURCE_ADAPTER_REGISTRY.get(catalog.execution_profile)
    if spec is None:
        return False, "adapter-not-registered"
    if spec.requires_secret and not source.secret_ref:
        return False, "credential-reference-required"
    return True, "ready"


def _automatic_source_due(
    state: ConnectorRuntimeState | None,
    *,
    interval_seconds: int,
    now: datetime,
) -> bool:
    if state is None:
        return True
    last_observed = as_utc(state.updated_at)
    return last_observed + timedelta(seconds=interval_seconds) <= now.astimezone(UTC)


def _load_source_state(
    sync_session: Session,
    *,
    source_id: str,
    now: datetime,
) -> tuple[ConnectorRuntimeState | None, bool]:
    return (
        sync_session.get(ConnectorRuntimeState, source_id),
        ConnectorStateStore(sync_session).is_isolated(source_id, now=now),
    )


def _record_automatic_source_run(
    sync_session: Session,
    *,
    source_id: str,
    run_result: ConnectorResult,
    succeeded: bool,
    duration: float,
    inserted: int,
    indexed: int,
) -> None:
    ConnectorStateStore(sync_session).record_run(
        connector_id=source_id,
        run_id=uuid4(),
        succeeded=succeeded,
        duration_seconds=duration,
        record_count=len(run_result.records),
        quarantined=[],
        error_code=None if succeeded else "source_execution_failed",
        details={
            "trigger": "automatic-interval",
            "inserted": inserted,
            "indexed": indexed,
            "error": run_result.error,
        },
    )


def _append_automatic_source_audit(
    sync_session: Session,
    *,
    source_id: str,
    source_url: str,
) -> None:
    append_persistent_audit_event(
        sync_session,
        principal="service:source-scheduler",
        principal_type="service_account",
        action="source.auto-run",
        resource=f"source:{source_id}",
        decision=AuditDecision.ALLOW,
        request_id=f"scheduler:{uuid4()}",
        provenance_reference=source_url,
    )


async def reconcile_registered_sources() -> dict[str, object]:
    """Execute due enabled source-registry entries through canonical ingestion.

    The reconciliation job is a service execution path. It never grants review,
    external-share or publication authority and it respects connector isolation.
    One source failure is recorded and contained so other due sources can proceed.
    """
    # Imported lazily to avoid a module import cycle: api.routes imports the
    # scheduler service during application composition.
    from dtmo.api.routes import database, ingest_connector_record

    now = datetime.now(UTC)
    eligible_count = 0
    executed_count = 0
    failed_count = 0
    skipped: dict[str, int] = {}

    async for session in database.session():
        sources = await SourceRegistry(session).list()
        for source in sources:
            eligible, reason = _automatic_source_eligibility(source)
            if not eligible:
                skipped[reason] = skipped.get(reason, 0) + 1
                continue
            eligible_count += 1

            state, isolated = await session.run_sync(
                partial(_load_source_state, source_id=source.id, now=now)
            )
            if isolated:
                skipped["isolated"] = skipped.get("isolated", 0) + 1
                continue
            if not _automatic_source_due(state, interval_seconds=source.interval_seconds, now=now):
                skipped["interval-not-due"] = skipped.get("interval-not-due", 0) + 1
                continue

            started = datetime.now(UTC)
            result: ConnectorResult
            inserted = 0
            indexed = 0
            try:
                result = await execute_source(source)
                if result.status == "completed":
                    for record in result.records:
                        receipt = await ingest_connector_record(source.id, record)
                        inserted += int(receipt.inserted)
                        indexed += int(receipt.indexed)
            except Exception as exc:
                result = ConnectorResult(
                    connector_id=source.id,
                    started_at=started.isoformat(),
                    finished_at=datetime.now(UTC).isoformat(),
                    records=[],
                    attempts=1,
                    status="failed",
                    error=f"{type(exc).__name__}: {exc}",
                )

            duration = max((datetime.now(UTC) - started).total_seconds(), 0.0)
            succeeded = result.status == "completed"
            await session.run_sync(
                partial(
                    _record_automatic_source_run,
                    source_id=source.id,
                    run_result=result,
                    succeeded=succeeded,
                    duration=duration,
                    inserted=inserted,
                    indexed=indexed,
                )
            )
            alert = connector_alerts.record(result)
            await session.run_sync(
                partial(
                    _append_automatic_source_audit,
                    source_id=source.id,
                    source_url=source.endpoint_url,
                )
            )
            executed_count += 1
            if not succeeded:
                failed_count += 1
            get_logger("scheduler").info(
                "registered_source_auto_run",
                source_id=source.id,
                status=result.status,
                records=len(result.records),
                inserted=inserted,
                indexed=indexed,
                alert_state=alert.state,
                correlation_id=alert.correlation_id,
            )

    return {
        "status": "completed",
        "eligible": eligible_count,
        "executed": executed_count,
        "failed": failed_count,
        "skipped": skipped,
        "publication_gate": "human-review-and-separate-share-approval-required",
    }


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler(timezone="UTC")
        self.log = get_logger("scheduler")
        self.started_at: str | None = None

    def register(self, job: ScheduledJob) -> None:
        async def guarded_handler() -> None:
            started = datetime.now(timezone.utc).isoformat()
            self.log.info("job_started", job_id=job.id, started_at=started)
            try:
                result = await job.handler()
                self.log.info("job_completed", job_id=job.id, result=str(result))
            except Exception:
                self.log.exception("job_failed", job_id=job.id)
                raise

        options: dict[str, object] = {}
        if job.run_immediately:
            options["next_run_time"] = datetime.now(timezone.utc)
        self.scheduler.add_job(
            guarded_handler,
            trigger=IntervalTrigger(seconds=job.interval_seconds),
            id=job.id,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=max(job.interval_seconds, 60),
            replace_existing=True,
            **options,
        )

    def _ensure_registered_source_reconciliation(self) -> None:
        if any(job.id == "registered-source-reconciliation" for job in self.scheduler.get_jobs()):
            return
        self.register(
            ScheduledJob(
                id="registered-source-reconciliation",
                interval_seconds=_REGISTERED_SOURCE_RECONCILIATION_SECONDS,
                handler=reconcile_registered_sources,
                run_immediately=True,
            )
        )

    def start(self) -> None:
        if not self.scheduler.running:
            self._ensure_registered_source_reconciliation()
            self.scheduler.start()
            self.started_at = datetime.now(timezone.utc).isoformat()
            self.log.info("scheduler_started", started_at=self.started_at)

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            self.log.info("scheduler_stopped")

    def status(self) -> dict[str, object]:
        return {
            "running": self.scheduler.running,
            "started_at": self.started_at,
            "jobs": [
                {"id": job.id, "next_run_time": str(job.next_run_time)}
                for job in self.scheduler.get_jobs()
            ],
        }
