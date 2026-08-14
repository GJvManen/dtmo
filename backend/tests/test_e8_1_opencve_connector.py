from __future__ import annotations

import json

import httpx
import pytest
from pydantic import SecretStr

from dtmo.config import Settings
from dtmo.connectors.opencve import OpenCVEConnector
from dtmo.vulnerability_intelligence import normalize_opencve_record


@pytest.fixture
def opencve_item() -> dict[str, object]:
    return {
        "cve": "CVE-2026-12345",
        "epss": 0.87,
        "opencve": {
            "title": "Example remote code execution",
            "description": "Example vulnerability description.",
            "created": "2026-08-01T10:00:00Z",
            "updated": "2026-08-14T09:00:00Z",
            "metrics": {
                "cvssV3_1": {
                    "score": 9.8,
                    "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                },
                "cvssV4_0": {"score": 9.3, "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N"},
                "kev": True,
            },
            "weaknesses": ["CWE-78"],
            "vendors": {"example_vendor": ["example_product"]},
            "cpes": ["cpe:2.3:a:example_vendor:example_product:1.0:*:*:*:*:*:*:*"],
            "references": ["https://vendor.example/advisory/12345"],
        },
    }


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "environment": "test",
        "opencve_api_token": SecretStr("opc_org.test.secret"),
        "opencve_max_pages": 2,
        "opencve_page_size": 20,
        "connector_max_attempts": 1,
    }
    values.update(overrides)
    return Settings(**values)


def test_normalizes_first_class_vulnerability_fields(opencve_item: dict[str, object]) -> None:
    normalized = normalize_opencve_record(opencve_item)

    assert normalized.cve_id == "CVE-2026-12345"
    assert normalized.cwes == ("CWE-78",)
    assert normalized.vendors == ("example_vendor",)
    assert normalized.products == ("example_product",)
    assert normalized.cvss_v31 == 9.8
    assert normalized.cvss_v40 == 9.3
    assert normalized.epss == 0.87
    assert normalized.kev is True
    assert "3.1" in normalized.cvss_vectors
    assert normalized.provenance.startswith("OpenCVE API v2")


@pytest.mark.asyncio
async def test_connector_uses_api_v2_bearer_auth_and_bounded_pagination(opencve_item: dict[str, object]) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        page = request.url.params.get("page")
        if page == "2":
            payload = {"count": 2, "next": None, "previous": "page-1", "results": [opencve_item]}
        else:
            payload = {
                "count": 2,
                "next": "https://app.opencve.io/api/v2/cves?page=2&page_size=20",
                "previous": None,
                "results": [opencve_item],
            }
        return httpx.Response(200, json=payload)

    connector = OpenCVEConnector(_settings())
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await connector.fetch(client)

    assert len(payload["pages"]) == 2
    assert len(requests) == 2
    assert requests[0].url.path == "/api/v2/cves"
    assert requests[0].headers["Authorization"] == "Bearer opc_org.test.secret"
    assert requests[0].headers["Accept"] == "application/json"


def test_connector_parse_preserves_original_and_adds_normalized_record(opencve_item: dict[str, object]) -> None:
    connector = OpenCVEConnector(_settings())
    records = connector.parse({"pages": [{"results": [opencve_item]}]})

    assert len(records) == 1
    record = records[0]
    assert record.external_id == "CVE-2026-12345"
    assert record.object_type == "vulnerability"
    assert record.source_reliability == "trusted"
    assert record.raw["cve"] == "CVE-2026-12345"
    normalized = record.raw["_dtmo_vulnerability"]
    assert isinstance(normalized, dict)
    assert normalized["epss"] == 0.87
    assert normalized["kev"] is True
    assert normalized["cvss_v31"] == 9.8


@pytest.mark.asyncio
async def test_connector_fails_closed_without_runtime_token() -> None:
    connector = OpenCVEConnector(_settings(opencve_api_token=SecretStr("")))
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(500))) as client:
        with pytest.raises(ValueError, match="token is not configured"):
            await connector.fetch(client)


def test_connector_rejects_non_paginated_api_shape() -> None:
    connector = OpenCVEConnector(_settings())
    with pytest.raises(ValueError, match="pages list"):
        connector.parse({"results": []})


def test_no_token_value_is_serialized_in_example_configuration() -> None:
    example = open(".env.example", encoding="utf-8").read()
    assert "DTMO_OPENCVE_API_TOKEN=\n" in example
    assert "opc_org.test.secret" not in example
    json.dumps(_settings().model_dump(mode="json"), default=str)
