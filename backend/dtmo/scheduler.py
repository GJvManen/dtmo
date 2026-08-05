from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from dtmo.logging import get_logger


@dataclass(slots=True)
class ScheduledJob:
    id: str
    interval_seconds: int
    handler: Callable[[], Awaitable[object]]


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

        self.scheduler.add_job(
            guarded_handler,
            trigger=IntervalTrigger(seconds=job.interval_seconds),
            id=job.id,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=max(job.interval_seconds, 60),
            replace_existing=True,
        )

    def start(self) -> None:
        if not self.scheduler.running:
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
