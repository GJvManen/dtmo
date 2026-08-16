from __future__ import annotations

from pathlib import Path

import httpx
import pytest
from pydantic import SecretStr

from dtmo.config import Settings
from dtmo.connectors.taranis import TaranisReadConnector


def _settings(tmp_path: Path, **overrides: object) -> Settings:
    values: dict[str, object] = {
        "environment": "test",
        "taranis_api_base": "https://taranis.example.test",
        "taranis_api_token": SecretStr("read-token"),
        "taranis_page_size": 10,
        "taranis_max_pages": 2,
        "taranis_reconcile_pages": 0,
        "taranis_detail_cti_limit": 2,
        "taranis_checkpoint_path": str(tmp_path / "taranis.json"),
        "connector_max_attempts": 1,
    }
    values.update(overrides)
    return Settings(**values)


@pytest.mark.asyncio
async def test_fetches_read_only_detail_and_cti_with_bounded_budget(tmp_path: Path) -> None:
    requests: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append((request.method, request.url.path))
        path = request.url.path
        if path.endswith("/news-items"):
            return httpx.Response(200, json=[{"id": "n1", "title": "News"}, {"id": "n2", "title": "News 2"}])
        if path.endswith("/stories"):
            return httpx.Response(200, json=[{"id": "s1", "title": "Story"}])
        if path.endswith("/news-items/n1"):
            return httpx.Response(200, json={"id": "n1", "title": "Detailed news", "tlp": "amber"})
        if path.endswith("/news-items/n1/cti"):
            return httpx.Response(200, json={"iocs": [{"type": "domain", "value": "example.test"}]})
        if path.endswith("/news-items/n2"):
            return httpx.Response(200, json={"id": "n2", "title": "Detailed news 2", "tlp": "green"})
        if path.endswith("/news-items/n2/cti"):
            return httpx.Response(200, json=[])
        raise AssertionError(f"unexpected request {path}")

    connector = TaranisReadConnector(_settings(tmp_path))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await connector.fetch(client)
    records = connector.parse(payload)

    assert all(method == "GET" for method, _ in requests)
    assert not any(any(word in path for word in ("publish", "share", "delete", "update")) for _, path in requests)
    assert records[0].title == "Detailed news"
    assert records[0].raw["_dtmo_taranis_context"]["status"] == "complete"
    assert records[0].raw["_dtmo_taranis_context"]["cti"]["iocs"][0]["value"] == "example.test"
    assert records[2].raw["_dtmo_taranis_context"]["status"] == "budget-exhausted"
    assert not any(path.endswith("/stories/s1") for _, path in requests)


@pytest.mark.asyncio
async def test_detail_404_is_reconciliation_race_not_deletion(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/news-items"):
            return httpx.Response(200, json=[{"id": "n1", "title": "News"}])
        if path.endswith("/stories"):
            return httpx.Response(200, json=[])
        if path.endswith("/news-items/n1"):
            return httpx.Response(404, json={"message": "gone during reconciliation"})
        raise AssertionError(f"unexpected request {path}")

    connector = TaranisReadConnector(_settings(tmp_path, taranis_detail_cti_limit=1))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        records = connector.parse(await connector.fetch(client))
    context = records[0].raw["_dtmo_taranis_context"]
    assert context["status"] == "reconciliation-race"
    assert context["detail"] is None
    assert context["cti"] is None


@pytest.mark.asyncio
async def test_malformed_cti_fails_before_checkpoint_commit(tmp_path: Path) -> None:
    checkpoint = tmp_path / "taranis.json"

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/news-items"):
            return httpx.Response(200, json=[{"id": "n1", "title": "News"}])
        if path.endswith("/stories"):
            return httpx.Response(200, json=[])
        if path.endswith("/news-items/n1"):
            return httpx.Response(200, json={"id": "n1", "title": "News"})
        if path.endswith("/news-items/n1/cti"):
            return httpx.Response(200, json="invalid")
        raise AssertionError(f"unexpected request {path}")

    connector = TaranisReadConnector(_settings(tmp_path, taranis_detail_cti_limit=1))

    async def run_with_transport() -> None:
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            payload = await connector.fetch(client)
            connector.parse(payload)

    with pytest.raises(ValueError, match="CTI"):
        await run_with_transport()
    assert not checkpoint.exists()


def test_main_registers_taranis_under_existing_governed_connector_permission() -> None:
    source = Path("backend/dtmo/main.py").read_text(encoding="utf-8")
    assert 'ScheduledJob(id="taranis"' in source
    assert '@app.post("/connectors/taranis/run")' in source
    route_start = source.index('@app.post("/connectors/taranis/run")')
    route_slice = source[route_start : route_start + 450]
    assert "Permission.MANAGE_CONNECTORS" in route_slice
    assert "run_taranis()" in route_slice
    assert '"external_share_authority": False' in source
