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


def test_normalizes_alternate_shapes_and_semantic_boundaries() -> None:
    item = {
        "id": "cve-2026-54321",
        "summary": "Fallback summary",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "epss": {"score": 87},
        "kev": "known_exploited",
        "metrics": {
            "cvssV2_0": {"baseScore": 7.5, "vectorString": "AV:N/AC:L/Au:N/C:P/I:P/A:P"},
            "cvssV3_0": {"score": 8.8, "vectorString": "CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H"},
            "cvssV3_1": {"score": True},
            "cvssV4_0": {"score": 11.0},
        },
        "cwe": [{"id": "CWE-79"}, {"name": "CWE-89"}],
        "vendors": [
            "vendor-a",
            {"vendor": "vendor-b", "product": "product-b", "products": ["product-c"]},
            {"name": "vendor-c"},
        ],
        "cpes": [{"criteria": "cpe:2.3:a:vendor-a:product-a:*:*:*:*:*:*:*:*"}],
        "references": [{"url": "https://example.test/a"}, {"href": "https://example.test/b"}],
    }

    normalized = normalize_opencve_record(item)
    assert normalized.cve_id == "CVE-2026-54321"
    assert normalized.description == "Fallback summary"
    assert normalized.title is None
    assert normalized.created_at == "2026-01-01T00:00:00Z"
    assert normalized.updated_at == "2026-01-02T00:00:00Z"
    assert normalized.cvss_v2 == 7.5
    assert normalized.cvss_v30 == 8.8
    assert normalized.cvss_v31 is None
    assert normalized.cvss_v40 is None
    assert normalized.epss == 0.87
    assert normalized.kev is True
    assert normalized.vendors == ("vendor-a", "vendor-b", "vendor-c")
    assert normalized.products == ("product-b", "product-c")
    assert normalized.cwes == ("CWE-79", "CWE-89")
    assert len(normalized.references) == 2
    assert "2.0" in normalized.cvss_vectors
    assert "3.0" in normalized.cvss_vectors


def test_products_fallback_and_invalid_probability_values() -> None:
    item = {
        "cve_id": "CVE-2026-22222",
        "description": "fallback",
        "epss": 150,
        "opencve": {
            "vendors": [],
            "products": [{"name": "alpha"}, {"product": "beta"}, "gamma"],
            "weaknesses": "CWE-20",
            "metrics": {"kev": None},
            "references": "https://example.test/ref",
            "cpes": "cpe:2.3:a:alpha:beta:*:*:*:*:*:*:*:*",
        },
    }
    normalized = normalize_opencve_record(item)
    assert normalized.products == ("alpha", "beta", "gamma")
    assert normalized.cwes == ("CWE-20",)
    assert normalized.epss is None
    assert normalized.kev is None
    assert normalized.references == ("https://example.test/ref",)


def test_kev_dict_and_false_string_are_preserved() -> None:
    positive = normalize_opencve_record(
        {
            "cve": "CVE-2026-33333",
            "opencve": {"metrics": {}, "kev": {"status": "yes"}},
        }
    )
    negative = normalize_opencve_record(
        {
            "cve": "CVE-2026-33334",
            "opencve": {"metrics": {}, "kev": "no"},
        }
    )
    assert positive.kev is True
    assert negative.kev is False


@pytest.mark.parametrize("bad_id", [None, "", "GHSA-1234", 123])
def test_invalid_cve_identifier_fails_closed(bad_id: object) -> None:
    with pytest.raises(ValueError, match="valid CVE identifier"):
        normalize_opencve_record({"cve": bad_id})


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


@pytest.mark.asyncio
async def test_connector_stops_when_next_is_blank(opencve_item: dict[str, object]) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json={"results": [opencve_item], "next": "  "})

    connector = OpenCVEConnector(_settings(opencve_max_pages=4))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await connector.fetch(client)
    assert calls == 1
    assert len(payload["pages"]) == 1


@pytest.mark.asyncio
async def test_connector_fetch_rejects_invalid_api_shape() -> None:
    connector = OpenCVEConnector(_settings())
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"results": "not-a-list"}))
    ) as client:
        with pytest.raises(ValueError, match="results list"):
            await connector.fetch(client)


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


def test_connector_uses_cve_as_title_when_title_missing() -> None:
    connector = OpenCVEConnector(_settings())
    records = connector.parse({"pages": [{"results": [{"cve": "CVE-2026-44444", "description": "x"}]}]})
    assert records[0].title == "CVE-2026-44444"


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"results": []}, "pages list"),
        ({"pages": ["bad-page"]}, "page has no results list"),
        ({"pages": [{"results": ["bad-item"]}]}, "result is not an object"),
    ],
)
def test_connector_parse_rejects_malformed_shapes(payload: object, message: str) -> None:
    connector = OpenCVEConnector(_settings())
    with pytest.raises(ValueError, match=message):
        connector.parse(payload)


@pytest.mark.asyncio
async def test_connector_fails_closed_without_runtime_token() -> None:
    connector = OpenCVEConnector(_settings(opencve_api_token=SecretStr("")))
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(500))) as client:
        with pytest.raises(ValueError, match="token is not configured"):
            await connector.fetch(client)


def test_no_token_value_is_serialized_in_example_configuration() -> None:
    with open(".env.example", encoding="utf-8") as handle:
        example = handle.read()
    assert "DTMO_OPENCVE_API_TOKEN=\n" in example
    assert "opc_org.test.secret" not in example
    serialized = json.dumps(_settings().model_dump(mode="json"), default=str)
    assert "opc_org.test.secret" not in serialized
