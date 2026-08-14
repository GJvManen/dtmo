from __future__ import annotations

import json

import httpx
import pytest
from pydantic import SecretStr, ValidationError

from dtmo.api.schemas import IntelligenceIngestRequest
from dtmo.config import Settings
from dtmo.connectors.misp import MispReadConnector, normalize_misp_event
from dtmo.intelligence import IntelligenceType


EVENT_UUID = "11111111-2222-4333-8444-555555555555"
ATTRIBUTE_UUID = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
OBJECT_UUID = "12345678-1234-4234-8234-123456789abc"


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "environment": "test",
        "misp_api_base": "https://misp.example.test",
        "misp_api_key": SecretStr("read-only-key"),
        "misp_event_limit": 25,
        "connector_max_attempts": 1,
    }
    values.update(overrides)
    return Settings(**values)


def _event() -> dict[str, object]:
    return {
        "id": "42",
        "uuid": EVENT_UUID,
        "info": "Credential phishing campaign",
        "date": "2026-08-14",
        "timestamp": "1786737600",
        "published": True,
        "publish_timestamp": "1786737600",
        "distribution": "4",
        "sharing_group_id": "7",
        "Orgc": {"uuid": "99999999-aaaa-4bbb-8ccc-dddddddddddd", "name": "Example CSIRT"},
        "Tag": [
            {"name": "tlp:amber+strict"},
            {"name": "misp-galaxy:threat-actor=\"Example Actor\""},
        ],
        "Galaxy": [
            {
                "uuid": "galaxy-uuid",
                "type": "threat-actor",
                "name": "Threat Actor",
                "GalaxyCluster": [
                    {
                        "uuid": "cluster-uuid",
                        "type": "threat-actor",
                        "value": "Example Actor",
                        "tag_name": "misp-galaxy:threat-actor=\"Example Actor\"",
                    }
                ],
            }
        ],
        "Attribute": [
            {
                "uuid": ATTRIBUTE_UUID,
                "type": "domain",
                "category": "Network activity",
                "value": "login-example.test",
                "to_ids": True,
                "timestamp": "1786737600",
                "distribution": "5",
                "sharing_group_id": "0",
                "Tag": [{"name": "tlp:amber+strict"}],
            }
        ],
        "Object": [
            {
                "uuid": OBJECT_UUID,
                "name": "file",
                "meta-category": "file",
                "description": "Observed payload",
                "timestamp": "1786737600",
                "distribution": "4",
                "sharing_group_id": "7",
                "Attribute": [
                    {
                        "uuid": "bbbbbbbb-cccc-4ddd-8eee-ffffffffffff",
                        "type": "sha256",
                        "category": "Payload delivery",
                        "value": "a" * 64,
                        "object_relation": "sha256",
                        "to_ids": True,
                        "distribution": "5",
                    }
                ],
                "ObjectReference": [
                    {
                        "uuid": "cccccccc-dddd-4eee-8fff-aaaaaaaaaaaa",
                        "referenced_uuid": ATTRIBUTE_UUID,
                        "relationship_type": "delivers",
                        "comment": "Payload relationship",
                    }
                ],
            }
        ],
    }


@pytest.mark.asyncio
async def test_fetch_uses_read_only_event_restsearch_and_runtime_key() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"response": [{"Event": _event()}]})

    connector = MispReadConnector(_settings())
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await connector.fetch(client)

    assert isinstance(payload, dict)
    request = requests[0]
    assert request.method == "POST"
    assert request.url.path == "/events/restSearch"
    assert request.headers["Authorization"] == "read-only-key"
    body = json.loads(request.content)
    assert body == {"returnFormat": "json", "limit": 25, "page": 1, "order": "timestamp desc"}
    assert not any(part in request.url.path.lower() for part in ("add", "edit", "publish", "push", "sync"))


def test_normalization_preserves_distribution_tlp_attributes_objects_and_relationships() -> None:
    projection = normalize_misp_event(_event())
    assert projection["event_uuid"] == EVENT_UUID
    assert projection["distribution"] == {"value": "4", "label": "sharing-group"}
    assert projection["sharing_group_id"] == "7"
    assert projection["tlp_tags"] == ["tlp:amber+strict"]
    assert projection["restriction_authoritative"] is True
    assert projection["read_only_import"] is True
    assert projection["external_share_authorized"] is False
    assert projection["attributes"][0]["uuid"] == ATTRIBUTE_UUID
    assert projection["attributes"][0]["distribution"]["label"] == "inherit"
    assert projection["objects"][0]["uuid"] == OBJECT_UUID
    assert projection["objects"][0]["attributes"][0]["type"] == "sha256"
    assert projection["objects"][0]["references"][0]["relationship_type"] == "delivers"
    assert projection["galaxies"][0]["clusters"][0]["value"] == "Example Actor"


def test_parse_retains_raw_event_and_uses_canonical_cti_event_type() -> None:
    connector = MispReadConnector(_settings())
    records = connector.parse({"response": [{"Event": _event()}]})
    assert len(records) == 1
    record = records[0]
    assert record.external_id == EVENT_UUID
    assert record.object_type == IntelligenceType.CTI_EVENT.value
    assert record.url == f"https://misp.example.test/events/view/{EVENT_UUID}"
    assert record.raw["uuid"] == EVENT_UUID
    assert record.raw["_dtmo_misp"]["external_share_authorized"] is False


def test_cti_event_record_is_valid_for_canonical_ingest_schema() -> None:
    record = MispReadConnector(_settings()).parse([{"Event": _event()}])[0]
    request = IntelligenceIngestRequest.model_validate(
        {
            "source_id": "misp",
            "external_id": record.external_id,
            "item_type": record.object_type,
            "title": record.title,
            "summary": record.summary,
            "canonical_url": record.url,
            "published_at": "2026-08-14T00:00:00Z",
            "provenance": [{"source_url": record.url, "confidence": record.confidence}],
            "raw_payload": record.raw,
        }
    )
    assert request.item_type == IntelligenceType.CTI_EVENT.value


def test_rejects_missing_credentials_and_malformed_event_shapes() -> None:
    connector = MispReadConnector(_settings(misp_api_key=SecretStr("")))
    with pytest.raises(ValueError, match="API key"):
        connector.parse({"metadata": {}})

    normal = MispReadConnector(_settings())
    with pytest.raises(ValueError, match="no event list"):
        normal.parse({"metadata": {"count": 1}})
    with pytest.raises(ValueError, match="not an object"):
        normal.parse(["event"])
    with pytest.raises(ValueError, match="no UUID"):
        normal.parse([{"Event": {"info": "missing uuid"}}])
    with pytest.raises(ValueError, match="Attribute must be a list"):
        normalize_misp_event({"uuid": EVENT_UUID, "Attribute": {"type": "domain"}})


def test_production_misp_requires_https_and_runtime_key() -> None:
    base: dict[str, object] = {
        "environment": "production",
        "minio_secure": True,
        "minio_secret_key": SecretStr("object-secret"),
        "jwt_jwks_json": SecretStr('{"keys":[{"kty":"RSA","kid":"test"}]}'),
        "privacy_pseudonymization_secret": SecretStr("x" * 32),
        "feature_misp_connector": True,
    }
    with pytest.raises(ValidationError, match="HTTPS"):
        Settings(**base, misp_api_base="http://misp.internal", misp_api_key=SecretStr("key"))
    with pytest.raises(ValidationError, match="runtime API key"):
        Settings(**base, misp_api_base="https://misp.internal", misp_api_key=SecretStr(""))
