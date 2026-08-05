from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class GraphStore(Protocol):
    async def upsert_node(self, node_id: str, node_type: str, label: str, properties: dict[str, Any]) -> None: ...
    async def upsert_edge(self, source_id: str, relation: str, target_id: str, properties: dict[str, Any]) -> None: ...
    async def neighbors(self, node_id: str, depth: int = 1) -> list[dict[str, Any]]: ...


@dataclass(frozen=True)
class CorrelationEvidence:
    source_url: str
    confidence: int
    rationale: str


class KnowledgeGraphService:
    def __init__(self, store: GraphStore) -> None:
        self.store = store

    async def relate(
        self,
        *,
        source_id: str,
        source_type: str,
        source_label: str,
        relation: str,
        target_id: str,
        target_type: str,
        target_label: str,
        evidence: CorrelationEvidence,
    ) -> None:
        if not 0 <= evidence.confidence <= 100:
            raise ValueError("confidence must be between 0 and 100")
        await self.store.upsert_node(source_id, source_type, source_label, {})
        await self.store.upsert_node(target_id, target_type, target_label, {})
        await self.store.upsert_edge(
            source_id,
            relation,
            target_id,
            {
                "confidence": evidence.confidence,
                "source_url": evidence.source_url,
                "rationale": evidence.rationale,
                "review_status": "candidate",
            },
        )

    async def attack_path(self, node_id: str, depth: int = 3) -> dict[str, Any]:
        if depth < 1 or depth > 5:
            raise ValueError("depth must be between 1 and 5")
        return {"root": node_id, "depth": depth, "relationships": await self.store.neighbors(node_id, depth)}
