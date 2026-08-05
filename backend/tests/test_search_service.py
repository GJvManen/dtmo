from __future__ import annotations

import json

import httpx
import pytest

from dtmo.config import Settings
from dtmo.search.service import OpenSearchService


@pytest.mark.asyncio
async def test_search_service_creates_indexes_and_returns_hits() -> None:
    requests: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append((request.method, request.url.path))
        if request.method == "HEAD":
            return httpx.Response(404)
        if request.method == "PUT" and request.url.path.endswith("dtmo-intelligence-v1"):
            return httpx.Response(200, json={"acknowledged": True})
        if request.method == "PUT" and "/_doc/" in request.url.path:
            return httpx.Response(201, json={"result": "created"})
        if request.method == "POST" and request.url.path.endswith("/_search"):
            return httpx.Response(
                200,
                json={
                    "hits": {
                        "hits": [
                            {
                                "_id": "item-1",
                                "_score": 2.5,
                                "_source": {
                                    "title": "PaperCut vulnerability",
                                    "summary": "Relevant to education",
                                    "severity": "critical",
                                    "confidence": 90,
                                    "education_relevance": 95,
                                },
                            }
                        ]
                    }
                },
            )
        return httpx.Response(500, text=json.dumps({"unexpected": request.url.path}))

    client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="http://opensearch:9200",
    )
    service = OpenSearchService(
        Settings(environment="test"),
        client=client,
    )
    await service.index_document(
        "item-1",
        {
            "title": "PaperCut vulnerability",
            "summary": "Relevant to education",
            "item_type": "vulnerability",
            "source_id": "test",
            "severity": "critical",
            "confidence": 90,
            "education_relevance": 95,
            "published_at": "2026-08-05T00:00:00Z",
            "canonical_url": "https://example.invalid/advisory",
            "tags": ["papercut"],
        },
    )
    results = await service.search(
        "PaperCut",
        severity="critical",
        minimum_relevance=80,
    )
    await client.aclose()

    assert results[0]["id"] == "item-1"
    assert ("HEAD", "/dtmo-intelligence-v1") in requests
    assert ("POST", "/dtmo-intelligence-v1/_search") in requests
