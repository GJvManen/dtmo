from __future__ import annotations

import httpx
import pytest
from pydantic import SecretStr, ValidationError

from dtmo.api.schemas import IntelligenceIngestRequest
from dtmo.config import Settings
from dtmo.connectors.ail import AilReadConnector, normalize_ail_object
from dtmo.intelligence import IntelligenceType


DOMAIN_GID = "domain:None:login-example.test"
IP_GID = "ip:None:203.0.113.10"


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "environment": "test",
        "ail_api_base": "https://ail.example.test",
        "ail_api_key": SecretStr("read-only-key"),
        "ail_object_global_ids": f"{DOMAIN_GID},{IP_GID}",
        "ail_object_limit": 25,
        "connector_max_attempts": 1,
    }
    values.update(overrides)
    return Settings(**values)


@pytest.mark.asyncio
async def test_fetch_only_reads_explicit_objects_and_never_calls_crawler_routes() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        gid = request.url.params["gid"]
        obj_type, _, obj_id = gid.split(":", 2)
        return httpx.Response(
            200,
            json={
                "type": obj_type,
                "id": obj_id,
                "content": "sensitive raw paste content must not be persisted",
                "investigations": [{"uuid": "investigation-1", "name": "Sensitive case title"}],
            },
        )

    connector = AilReadConnector(_settings())
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await connector.fetch(client)

    assert len(payload) == 2
    assert all(request.method == "GET" for request in requests)
    assert all(request.url.path == "/api/v1/object" for request in requests)
    assert [request.url.params["gid"] for request in requests] == [DOMAIN_GID, IP_GID]
    assert all(request.headers["Authorization"] == "read-only-key" for request in requests)
    assert not any("crawler" in request.url.path.lower() for request in requests)
    assert not any(request.method in {"POST", "PUT", "PATCH", "DELETE"} for request in requests)


def test_normalization_is_data_minimized_and_retains_only_investigation_identifier() -> None:
    projection = normalize_ail_object(
        DOMAIN_GID,
        {
            "type": "domain",
            "id": "login-example.test",
            "content": "raw content",
            "info": "potentially sensitive description",
            "investigations": [{"uuid": "investigation-1", "name": "Sensitive case title", "note": "private"}],
        },
    )
    assert projection == {
        "global_id": DOMAIN_GID,
        "indicator_type": "domain",
        "indicator_subtype": None,
        "indicator_value": "login-example.test",
        "investigation_references": [{"id": "investigation-1"}],
        "read_only_import": True,
        "data_minimized": True,
        "raw_content_imported": False,
        "external_share_authorized": False,
    }


def test_parse_emits_canonical_indicator_without_raw_ail_content() -> None:
    connector = AilReadConnector(_settings())
    record = connector.parse(
        [
            {
                "gid": DOMAIN_GID,
                "object": {
                    "type": "domain",
                    "id": "login-example.test",
                    "content": "must disappear",
                    "investigations": ["investigation-1"],
                },
            }
        ]
    )[0]

    assert record.external_id == DOMAIN_GID
    assert record.object_type == IntelligenceType.INDICATOR.value
    assert record.url.endswith("gid=domain%3ANone%3Alogin-example.test")
    assert record.raw == {
        "_dtmo_ail": {
            "global_id": DOMAIN_GID,
            "indicator_type": "domain",
            "indicator_subtype": None,
            "indicator_value": "login-example.test",
            "investigation_references": [{"id": "investigation-1"}],
            "read_only_import": True,
            "data_minimized": True,
            "raw_content_imported": False,
            "external_share_authorized": False,
        }
    }
    assert "must disappear" not in str(record.raw)


def test_indicator_record_is_valid_for_canonical_ingest_schema() -> None:
    record = AilReadConnector(_settings()).parse(
        [{"gid": DOMAIN_GID, "object": {"type": "domain", "id": "login-example.test"}}]
    )[0]
    request = IntelligenceIngestRequest.model_validate(
        {
            "source_id": "ail",
            "external_id": record.external_id,
            "item_type": record.object_type,
            "title": record.title,
            "summary": record.summary,
            "canonical_url": record.url,
            "provenance": [{"source_url": record.url, "confidence": record.confidence}],
            "raw_payload": record.raw,
        }
    )
    assert request.item_type == IntelligenceType.INDICATOR.value


def test_rejects_non_indicator_types_mismatches_and_missing_configuration() -> None:
    with pytest.raises(ValueError, match="outside the DTMO indicator allowlist"):
        normalize_ail_object("item:None:secret-paste", {"type": "item", "id": "secret-paste"})
    with pytest.raises(ValueError, match="type does not match"):
        normalize_ail_object(DOMAIN_GID, {"type": "ip", "id": "login-example.test"})
    with pytest.raises(ValueError, match="id does not match"):
        normalize_ail_object(DOMAIN_GID, {"type": "domain", "id": "other.test"})

    connector = AilReadConnector(_settings(ail_object_global_ids=""))
    with pytest.raises(ValueError, match="explicit object global ids"):
        connector._targets()


@pytest.mark.asyncio
async def test_rejects_missing_runtime_key() -> None:
    connector = AilReadConnector(_settings(ail_api_key=SecretStr("")))
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(200, json={}))) as client:
        with pytest.raises(ValueError, match="API key"):
            await connector.fetch(client)


def test_production_ail_requires_https_runtime_key_and_explicit_targets() -> None:
    base: dict[str, object] = {
        "environment": "production",
        "minio_secure": True,
        "minio_secret_key": SecretStr("object-secret"),
        "jwt_jwks_json": SecretStr('{"keys":[{"kty":"RSA","kid":"test"}]}'),
        "privacy_pseudonymization_secret": SecretStr("x" * 32),
        "feature_ail_connector": True,
        "ail_object_global_ids": DOMAIN_GID,
    }
    with pytest.raises(ValidationError, match="HTTPS"):
        Settings(**base, ail_api_base="http://ail.internal", ail_api_key=SecretStr("key"))
    with pytest.raises(ValidationError, match="runtime API key"):
        Settings(**base, ail_api_base="https://ail.internal", ail_api_key=SecretStr(""))
    without_targets = {**base, "ail_object_global_ids": ""}
    with pytest.raises(ValidationError, match="explicit object global ids"):
        Settings(**without_targets, ail_api_base="https://ail.internal", ail_api_key=SecretStr("key"))
