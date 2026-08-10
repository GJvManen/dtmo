from __future__ import annotations

import json

import httpx
import pytest

from dtmo.config import Settings
from dtmo.search.service import OpenSearchService


@pytest.mark.asyncio
async def test_search_initializes_missing_index_and_returns_empty_results() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "HEAD":
            return httpx.Response(404, request=request)
        if request.method == "PUT" and request.url.path == "/dtmo-intelligence-v1":
            return httpx.Response(200, request=request, json={"acknowledged": True})
        if request.method == "POST" and request.url.path.endswith("/_search"):
            return httpx.Response(200, request=request, json={"hits": {"hits": []}})
        raise AssertionError(f"unexpected request: {request.method} {request.url}")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = OpenSearchService(
        Settings(opensearch_url="http://opensearch.test:9200"),
        client=client,
    )
    try:
        assert await service.search("ransomware") == []
    finally:
        await client.aclose()

    assert [request.method for request in requests] == ["HEAD", "PUT", "POST"]
    create_body = json.loads(requests[1].content)
    properties = create_body["mappings"]["properties"]
    assert "confidence_score" in properties
    assert "confidence_level" in properties
    assert "confidence_rationale" in properties
    assert "confidence" not in properties

    search_body = json.loads(requests[2].content)
    assert search_body["sort"][1] == {"confidence_score": {"order": "desc"}}


@pytest.mark.asyncio
async def test_index_document_uses_mapping_compatible_confidence_fields() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "HEAD":
            return httpx.Response(200, request=request)
        if request.method == "PUT" and "/_doc/" in request.url.path:
            return httpx.Response(201, request=request, json={"result": "created"})
        raise AssertionError(f"unexpected request: {request.method} {request.url}")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = OpenSearchService(
        Settings(opensearch_url="http://opensearch.test:9200"),
        client=client,
    )
    document = {
        "title": "Example",
        "summary": "Example intelligence",
        "item_type": "vulnerability",
        "source_id": "test-source",
        "severity": "high",
        "confidence_score": 98,
        "confidence_level": "high",
        "confidence_rationale": "authoritative source",
        "education_relevance": 90,
        "published_at": "2026-08-10T00:00:00+00:00",
        "canonical_url": "https://example.invalid/item",
        "tags": ["test"],
    }
    try:
        await service.index_document("item-1", document)
    finally:
        await client.aclose()

    indexed = json.loads(requests[-1].content)
    assert indexed["confidence_score"] == 98
    assert indexed["confidence_level"] == "high"
    assert "confidence" not in indexed
