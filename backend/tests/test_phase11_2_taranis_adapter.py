from __future__ import annotations

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
async def test_fetch_is_read_only_and_uses_bearer_token() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path.endswith("news-items"):
            return httpx.Response(200, json=[{"id": "n1", "title": "News", "tlp": "amber"}])
        return httpx.Response(200, json=[{"id": "s1", "title": "Story", "tlp": "red"}])

    connector = TaranisReadConnector(_settings())
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await connector.fetch(client)
    records = connector.parse(payload)

    assert [request.method for request in requests] == ["GET", "GET"]
    assert all(request.headers["Authorization"] == "Bearer read-token" for request in requests)
    assert not any(any(term in request.url.path for term in ("publish", "share", "delete", "update")) for request in requests)
    assert {record.external_id for record in records} == {"taranis:news-item:n1", "taranis:story:s1"}
    assert all(record.raw["_dtmo_taranis"]["external_share_authorized"] is False for record in records)


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
async def test_missing_token_and_upstream_outage_are_isolated() -> None:
    missing = TaranisReadConnector(_settings(taranis_api_token=SecretStr("")))
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(200, json=[]))) as client:
        with pytest.raises(ValueError, match="token"):
            await missing.fetch(client)

    connector = TaranisReadConnector(_settings())
    async def broken(_: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("upstream unavailable")
    # Connector.run owns the bounded retry/failure isolation path; use a malformed base to force a safe failed result.
    result = await TaranisReadConnector(_settings(taranis_api_base="http://127.0.0.1:1")).run()
    assert result.status == "failed"
    assert result.records == []


def test_production_requires_https_and_runtime_token() -> None:
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
