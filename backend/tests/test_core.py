from __future__ import annotations

import asyncio

import httpx
from fastapi.testclient import TestClient

from dtmo.config import Settings
from dtmo.connectors.cisa_kev import CisaKevConnector
from dtmo.lake.minio_store import MinioObjectStore
from dtmo.main import app


FIXTURE = {
    "vulnerabilities": [
        {
            "cveID": "CVE-2026-0001",
            "vendorProject": "Example",
            "product": "Education Platform",
            "vulnerabilityName": "Example vulnerability",
            "dateAdded": "2026-08-05",
            "shortDescription": "Example actively exploited vulnerability.",
        }
    ]
}


def test_application_import_does_not_initialize_object_storage() -> None:
    store = MinioObjectStore(Settings(environment="test", minio_secret_key=""))
    assert store._client is None
    assert app.title == "DTMO API"


def test_health_and_security_headers() -> None:
    client = TestClient(app)
    response = client.get("/health", headers={"x-correlation-id": "test-correlation"})
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["publication_gate"] == "human-approval-required"
    assert response.headers["x-correlation-id"] == "test-correlation"
    assert response.headers["x-frame-options"] == "DENY"


def test_connector_parser() -> None:
    connector = CisaKevConnector(Settings(environment="test"))
    records = connector.parse(FIXTURE)
    assert len(records) == 1
    assert records[0].external_id == "CVE-2026-0001"
    assert records[0].source_reliability == "authoritative"
    assert len(records[0].content_hash) == 64


def test_connector_retry_failure(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    connector = CisaKevConnector(
        Settings(environment="test", connector_max_attempts=2, connector_timeout_seconds=1)
    )

    async def fail_fetch(self, client):  # type: ignore[no-untyped-def]
        raise httpx.ConnectError("offline")

    monkeypatch.setattr(CisaKevConnector, "fetch", fail_fetch)
    result = asyncio.run(connector.run())
    assert result.status == "failed"
    assert result.attempts == 2
    assert result.records == []
