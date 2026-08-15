from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from pydantic import SecretStr, ValidationError

from dtmo.config import Settings
from dtmo.connectors.taranis import TaranisReadConnector, normalize_taranis_item


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "environment": "test",
        "taranis_api_base": "https://taranis.example.test",
        "taranis_api_token": SecretStr("read-token"),
        "taranis_page_size": 50,
        "taranis_max_pages": 10,
        "taranis_reconcile_pages": 1,
        "connector_max_attempts": 1,
    }
    values.update(overrides)
    return Settings(**values)


def test_normalization_namespaces_identity_and_fails_closed_on_unknown_marking() -> None:
    projection = normalize_taranis_item(
        {"id": 42, "source": {"id": 7}, "tlp": "TLP:UNKNOWN"},
        object_type="news-item",
        instance="https://taranis.example.test",
    )
    assert projection["canonical_external_id"] == "taranis:news-item:42"
    assert projection["upstream_source_id"] == "7"
    assert projection["handling"]["dtmo"] == "review-required"
    assert projection["handling"]["mapped"] is False
    assert projection["read_only_import"] is True
    assert projection["external_share_authorized"] is False


@pytest.mark.asyncio
async def test_fetch_is_read_only_and_uses_bearer_token(tmp_path: Path) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path.endswith("news-items"):
            return httpx.Response(200, json=[{"id": "n1", "title": "News", "tlp": "amber"}])
        return httpx.Response(200, json=[{"id": "s1", "title": "Story", "tlp": "red"}])

    connector = TaranisReadConnector(_settings(taranis_checkpoint_path=str(tmp_path / "checkpoint.json")))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await connector.fetch(client)
    records = connector.parse(payload)

    assert [request.method for request in requests] == ["GET", "GET"]
    assert all(request.headers["Authorization"] == "Bearer read-token" for request in requests)
    assert not any(any(term in request.url.path for term in ("publish", "share", "delete", "update")) for request in requests)
    assert {record.external_id for record in records} == {"taranis:news-item:n1", "taranis:story:s1"}
    assert all(record.raw["_dtmo_taranis"]["external_share_authorized"] is False for record in records)


@pytest.mark.asyncio
async def test_pagination_is_bounded_and_checkpoint_commits_only_after_success(tmp_path: Path) -> None:
    checkpoint = tmp_path / "checkpoint.json"
    offsets: list[tuple[str, int]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        offset = int(request.url.params["offset"])
        offsets.append((request.url.path, offset))
        prefix = "n" if request.url.path.endswith("news-items") else "s"
        if offset == 0:
            return httpx.Response(200, json=[{"id": f"{prefix}{i}"} for i in range(2)])
        return httpx.Response(200, json=[{"id": f"{prefix}2"}])

    settings = _settings(
        taranis_page_size=2,
        taranis_max_pages=3,
        taranis_reconcile_pages=0,
        taranis_checkpoint_path=str(checkpoint),
    )
    connector = TaranisReadConnector(settings)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await connector.fetch(client)
    assert not checkpoint.exists()
    assert payload["_checkpoint"] == {"news_items": 3, "stories": 3}
    assert offsets == [
        ("/api/assess/news-items", 0),
        ("/api/assess/news-items", 2),
        ("/api/assess/stories", 0),
        ("/api/assess/stories", 2),
    ]

    async def successful_fetch(client: httpx.AsyncClient) -> object:
        return payload

    connector.fetch = successful_fetch  # type: ignore[method-assign]
    result = await connector.run()
    assert result.status == "completed"
    assert json.loads(checkpoint.read_text()) == {"news_items": 3, "stories": 3}


@pytest.mark.asyncio
async def test_reconciliation_backtracks_checkpoint_and_replays_stable_ids(tmp_path: Path) -> None:
    checkpoint = tmp_path / "checkpoint.json"
    checkpoint.write_text('{"news_items": 100, "stories": 50}\n', encoding="utf-8")
    seen_offsets: dict[str, int] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen_offsets[request.url.path] = int(request.url.params["offset"])
        return httpx.Response(200, json=[{"id": "same", "title": "changed upstream title"}])

    connector = TaranisReadConnector(
        _settings(taranis_page_size=10, taranis_reconcile_pages=2, taranis_checkpoint_path=str(checkpoint))
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await connector.fetch(client)
    records = connector.parse(payload)

    assert seen_offsets["/api/assess/news-items"] == 80
    assert seen_offsets["/api/assess/stories"] == 30
    assert {record.external_id for record in records} == {"taranis:news-item:same", "taranis:story:same"}
    assert payload["_checkpoint"] == {"news_items": 100, "stories": 50}


@pytest.mark.asyncio
async def test_failed_parse_does_not_advance_existing_checkpoint(tmp_path: Path) -> None:
    checkpoint = tmp_path / "checkpoint.json"
    checkpoint.write_text('{"news_items": 7, "stories": 9}\n', encoding="utf-8")
    connector = TaranisReadConnector(_settings(taranis_checkpoint_path=str(checkpoint)))

    async def malformed_fetch(client: httpx.AsyncClient) -> object:
        return {
            "news_items": [{"title": "missing stable id"}],
            "stories": [],
            "_checkpoint": {"news_items": 10, "stories": 9},
        }

    connector.fetch = malformed_fetch  # type: ignore[method-assign]
    result = await connector.run()
    assert result.status == "failed"
    assert json.loads(checkpoint.read_text()) == {"news_items": 7, "stories": 9}


def test_replay_is_deterministic_and_malformed_payload_fails_closed() -> None:
    connector = TaranisReadConnector(_settings())
    payload = {"news_items": [{"id": "n1", "title": "News"}], "stories": []}
    first = connector.parse(payload)[0]
    second = connector.parse(payload)[0]
    assert first.external_id == second.external_id
    assert first.content_hash == second.content_hash
    with pytest.raises(ValueError, match="stable id"):
        connector.parse({"news_items": [{"title": "missing id"}], "stories": []})
    with pytest.raises(ValueError, match="must contain a list"):
        connector.parse({"news_items": {"id": "bad"}, "stories": []})


@pytest.mark.asyncio
async def test_missing_token_and_upstream_outage_are_isolated(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    missing = TaranisReadConnector(_settings(taranis_api_token=SecretStr(""), taranis_checkpoint_path=str(tmp_path / "a.json")))
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(200, json=[]))) as client:
        with pytest.raises(ValueError, match="token"):
            await missing.fetch(client)

    async def fail_fetch(self: TaranisReadConnector, client: httpx.AsyncClient) -> object:
        raise httpx.ConnectError("upstream unavailable")

    monkeypatch.setattr(TaranisReadConnector, "fetch", fail_fetch)
    result = await TaranisReadConnector(_settings(taranis_checkpoint_path=str(tmp_path / "b.json"))).run()
    assert result.status == "failed"
    assert result.records == []
    assert "upstream unavailable" in (result.error or "")


def test_production_requires_https_runtime_token_and_absolute_checkpoint_path() -> None:
    base: dict[str, object] = {
        "environment": "production",
        "minio_secure": True,
        "minio_secret_key": SecretStr("object-secret"),
        "jwt_jwks_json": SecretStr('{"keys":[{"kty":"RSA","kid":"test"}]}'),
        "privacy_pseudonymization_secret": SecretStr("x" * 32),
        "feature_taranis_connector": True,
    }
    with pytest.raises(ValidationError, match="HTTPS"):
        Settings(**base, taranis_api_base="http://taranis.internal", taranis_api_token=SecretStr("token"))
    with pytest.raises(ValidationError, match="runtime API token"):
        Settings(**base, taranis_api_base="https://taranis.internal", taranis_api_token=SecretStr(""))
    with pytest.raises(ValidationError, match="absolute durable checkpoint path"):
        Settings(
            **base,
            taranis_api_base="https://taranis.internal",
            taranis_api_token=SecretStr("token"),
            taranis_checkpoint_path="relative/checkpoint.json",
        )
