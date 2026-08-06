from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest

from dtmo.config import Settings
from dtmo.connectors.catalog import ConnectorCatalog, ConnectorDefinition
from dtmo.lake.minio_store import MinioObjectStore
from dtmo.persistence.models import ConnectorRun, IntelligenceItem, ProvenanceRecord
from dtmo.persistence.repository import ConnectorRunRepository, IntelligenceRepository
from dtmo.scheduler import ScheduledJob, SchedulerService


class FakeSession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.scalar_result: object | None = None
        self.get_result: object | None = None
        self.flush_count = 0

    async def scalar(self, _statement: object) -> object | None:
        return self.scalar_result

    async def get(self, _model: object, _item_id: object) -> object | None:
        return self.get_result

    def add(self, value: object) -> None:
        self.added.append(value)

    async def flush(self) -> None:
        self.flush_count += 1
        for value in self.added:
            if isinstance(value, (IntelligenceItem, ProvenanceRecord, ConnectorRun)):
                if getattr(value, "id", None) is None:
                    value.id = uuid4()
            if isinstance(value, ConnectorRun) and getattr(value, "started_at", None) is None:
                value.started_at = datetime.now(timezone.utc)


class FakeMinioResponse:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload
        self.closed = False
        self.released = False

    def read(self) -> bytes:
        return self.payload

    def close(self) -> None:
        self.closed = True

    def release_conn(self) -> None:
        self.released = True


class FakeMinioClient:
    def __init__(self) -> None:
        self.buckets: set[str] = set()
        self.objects: dict[tuple[str, str], bytes] = {}
        self.last_response: FakeMinioResponse | None = None

    def bucket_exists(self, bucket: str) -> bool:
        return bucket in self.buckets

    def make_bucket(self, bucket: str) -> None:
        self.buckets.add(bucket)

    def put_object(
        self,
        bucket: str,
        key: str,
        stream: object,
        *,
        length: int,
        content_type: str,
    ) -> None:
        del content_type
        self.objects[(bucket, key)] = stream.read(length)  # type: ignore[attr-defined]

    def get_object(self, bucket: str, key: str) -> FakeMinioResponse:
        self.last_response = FakeMinioResponse(self.objects[(bucket, key)])
        return self.last_response

    def list_buckets(self) -> list[object]:
        return [SimpleNamespace(name=name) for name in sorted(self.buckets)]


def definition(connector_id: str = "example", **overrides: object) -> ConnectorDefinition:
    values = {
        "connector_id": connector_id,
        "title": "Example connector",
        "source_type": "feed",
        "reliability": "trusted",
        "schedule_minutes": 15,
        "enabled_by_default": True,
        "factory": lambda: None,
    }
    values.update(overrides)
    return ConnectorDefinition(**values)  # type: ignore[arg-type]


def test_connector_catalog_validation_sorting_and_health() -> None:
    catalog = ConnectorCatalog()
    catalog.register(definition("zeta"))
    catalog.register(definition("alpha", enabled_by_default=False))
    assert [item.connector_id for item in catalog.definitions()] == ["alpha", "zeta"]

    snapshot = catalog.health_snapshot(
        {
            "alpha": {
                "enabled": True,
                "last_success": "now",
                "consecutive_failures": 3,
                "last_error": "offline",
            }
        }
    )
    assert snapshot[0]["enabled"] is True
    assert snapshot[0]["healthy"] is False
    assert snapshot[1]["healthy"] is True
    assert snapshot[0]["generated_at"]

    with pytest.raises(ValueError, match="duplicate"):
        catalog.register(definition("alpha"))
    with pytest.raises(ValueError, match="reliability"):
        ConnectorCatalog().register(definition(reliability="unknown"))
    with pytest.raises(ValueError, match="interval"):
        ConnectorCatalog().register(definition(schedule_minutes=1))


@pytest.mark.asyncio
async def test_intelligence_repository_ingest_duplicate_and_approval() -> None:
    session = FakeSession()
    repository = IntelligenceRepository(session)  # type: ignore[arg-type]
    payload = {
        "source_id": "source",
        "external_id": "item-1",
        "title": "Threat report",
        "summary": "Summary",
        "canonical_url": "https://example.invalid/report",
        "tags": ["education"],
        "metadata": {"key": "value"},
        "provenance": [
            {
                "source_url": "https://example.invalid/source",
                "source_title": "Source",
                "publisher": "Publisher",
                "exact_passage": "Evidence",
                "confidence": 90,
            }
        ],
    }

    item, inserted = await repository.ingest_candidate(payload)
    assert inserted is True
    assert item.review_status == "candidate"
    assert item.share_approved is False
    assert len(item.content_hash) == 64
    assert any(isinstance(value, ProvenanceRecord) for value in session.added)

    session.scalar_result = item
    duplicate, inserted = await repository.ingest_candidate(payload)
    assert duplicate is item
    assert inserted is False

    session.get_result = None
    with pytest.raises(KeyError):
        await repository.approve_for_sharing(uuid4(), "reviewer")

    session.get_result = item
    with pytest.raises(ValueError, match="reviewed"):
        await repository.approve_for_sharing(item.id, "reviewer")

    item.review_status = "reviewed"
    approved = await repository.approve_for_sharing(item.id, "reviewer")
    assert approved.share_approved is True
    assert approved.metadata_json["share_approved_by"] == "reviewer"


@pytest.mark.asyncio
async def test_connector_run_repository_records_success_and_degraded_runs() -> None:
    session = FakeSession()
    repository = ConnectorRunRepository(session)  # type: ignore[arg-type]
    successful = await repository.start("connector")
    finished = await repository.finish(successful, fetched=4, inserted=3, duplicates=1)
    assert finished.status == "completed"
    assert finished.error_count == 0
    assert finished.duration_seconds is not None

    degraded = await repository.start("connector")
    finished = await repository.finish(
        degraded,
        fetched=2,
        inserted=0,
        duplicates=0,
        errors=["timeout"],
    )
    assert finished.status == "degraded"
    assert finished.details == {"errors": ["timeout"]}


@pytest.mark.asyncio
async def test_minio_store_round_trip_and_ping() -> None:
    store = MinioObjectStore(Settings(environment="test", minio_secret_key="test-secret"))
    client = FakeMinioClient()
    store._client = client  # type: ignore[assignment]

    await store.put_bytes("bucket", "object", b"payload", "application/octet-stream")
    assert "bucket" in client.buckets
    assert await store.get_bytes("bucket", "object") == b"payload"
    assert client.last_response is not None
    assert client.last_response.closed is True
    assert client.last_response.released is True
    assert await store.ping() is True

    class BrokenClient(FakeMinioClient):
        def list_buckets(self) -> list[object]:
            raise OSError("offline")

    store._client = BrokenClient()  # type: ignore[assignment]
    assert await store.ping() is False


def test_scheduler_register_start_shutdown_and_status() -> None:
    service = SchedulerService()
    calls: dict[str, object] = {}

    class FakeScheduler:
        running = False

        def add_job(self, handler: object, **kwargs: object) -> None:
            calls["handler"] = handler
            calls.update(kwargs)

        def start(self) -> None:
            self.running = True

        def shutdown(self, *, wait: bool) -> None:
            calls["wait"] = wait
            self.running = False

        def get_jobs(self) -> list[object]:
            return [SimpleNamespace(id="job", next_run_time="later")]

    service.scheduler = FakeScheduler()  # type: ignore[assignment]

    async def handler() -> object:
        return {"ok": True}

    service.register(ScheduledJob(id="job", interval_seconds=60, handler=handler))
    assert calls["id"] == "job"
    service.start()
    assert service.started_at is not None
    assert service.status()["running"] is True
    assert service.status()["jobs"] == [{"id": "job", "next_run_time": "later"}]
    service.shutdown()
    assert calls["wait"] is False
