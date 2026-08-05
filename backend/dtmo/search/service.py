from __future__ import annotations

from typing import Any

import httpx

from dtmo.config import Settings, get_settings


class OpenSearchService:
    def __init__(
        self,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
        index_name: str = "dtmo-intelligence-v1",
    ) -> None:
        cfg = settings or get_settings()
        self.base_url = cfg.opensearch_url.rstrip("/")
        self.index_name = index_name
        self.client = client or httpx.AsyncClient(timeout=30.0)
        self._owns_client = client is None

    async def ensure_index(self) -> None:
        response = await self.client.head(f"{self.base_url}/{self.index_name}")
        if response.status_code == 200:
            return
        if response.status_code != 404:
            response.raise_for_status()
        create = await self.client.put(
            f"{self.base_url}/{self.index_name}",
            json={
                "settings": {
                    "index": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                    }
                },
                "mappings": {
                    "dynamic": "strict",
                    "properties": {
                        "title": {"type": "text"},
                        "summary": {"type": "text"},
                        "item_type": {"type": "keyword"},
                        "source_id": {"type": "keyword"},
                        "severity": {"type": "keyword"},
                        "confidence": {"type": "integer"},
                        "education_relevance": {"type": "integer"},
                        "published_at": {"type": "date"},
                        "canonical_url": {"type": "keyword"},
                        "tags": {"type": "keyword"},
                    },
                },
            },
        )
        create.raise_for_status()

    async def index_document(self, document_id: str, document: dict[str, Any]) -> None:
        await self.ensure_index()
        response = await self.client.put(
            f"{self.base_url}/{self.index_name}/_doc/{document_id}",
            params={"refresh": "wait_for"},
            json=document,
        )
        response.raise_for_status()

    async def search(
        self,
        query: str,
        *,
        severity: str | None = None,
        minimum_relevance: int = 0,
        size: int = 50,
    ) -> list[dict[str, Any]]:
        filters: list[dict[str, Any]] = [
            {"range": {"education_relevance": {"gte": minimum_relevance}}}
        ]
        if severity is not None:
            filters.append({"term": {"severity": severity}})
        response = await self.client.post(
            f"{self.base_url}/{self.index_name}/_search",
            json={
                "size": min(max(size, 1), 200),
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["title^3", "summary", "tags"],
                                }
                            }
                        ],
                        "filter": filters,
                    }
                },
                "sort": [
                    {"education_relevance": {"order": "desc"}},
                    {"confidence": {"order": "desc"}},
                ],
            },
        )
        response.raise_for_status()
        payload = response.json()
        return [
            {"id": hit["_id"], "score": hit.get("_score"), **hit["_source"]}
            for hit in payload.get("hits", {}).get("hits", [])
        ]

    async def ping(self) -> bool:
        try:
            response = await self.client.get(f"{self.base_url}/_cluster/health")
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    async def close(self) -> None:
        if self._owns_client:
            await self.client.aclose()
