from __future__ import annotations

import asyncio

import pytest

from dtmo.auth.policy import Permission, Principal, Role, require
from dtmo.graph.service import CorrelationEvidence, KnowledgeGraphService
from dtmo.lake.service import IntelligenceLake
from dtmo.reporting.service import ReportingService


class MemoryStore:
    def __init__(self) -> None:
        self.objects: dict[tuple[str, str], bytes] = {}

    async def put_bytes(self, bucket: str, key: str, data: bytes, content_type: str) -> None:
        self.objects[(bucket, key)] = data

    async def get_bytes(self, bucket: str, key: str) -> bytes:
        return self.objects[(bucket, key)]


class MemoryGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {}
        self.edges: list[dict] = []

    async def upsert_node(self, node_id: str, node_type: str, label: str, properties: dict) -> None:
        self.nodes[node_id] = {"type": node_type, "label": label, **properties}

    async def upsert_edge(self, source_id: str, relation: str, target_id: str, properties: dict) -> None:
        self.edges.append({"source": source_id, "relation": relation, "target": target_id, **properties})

    async def neighbors(self, node_id: str, depth: int = 1) -> list[dict]:
        return [edge for edge in self.edges if edge["source"] == node_id or edge["target"] == node_id]


@pytest.mark.asyncio
async def test_intelligence_lake_preserves_and_verifies_raw_payload() -> None:
    store = MemoryStore()
    lake = IntelligenceLake(store)
    receipt = await lake.land("cisa-kev", "CVE-2026-0001", b'{"cve":"CVE-2026-0001"}', "application/json")
    assert await lake.verify(receipt)
    assert receipt.sha256 and receipt.size > 0


@pytest.mark.asyncio
async def test_graph_relationship_requires_evidence_and_confidence() -> None:
    store = MemoryGraph()
    graph = KnowledgeGraphService(store)
    await graph.relate(
        source_id="cve:CVE-2026-0001",
        source_type="vulnerability",
        source_label="CVE-2026-0001",
        relation="affects",
        target_id="product:test",
        target_type="product",
        target_label="Test Product",
        evidence=CorrelationEvidence("https://example.invalid/advisory", 90, "Vendor advisory"),
    )
    result = await graph.attack_path("cve:CVE-2026-0001")
    assert result["relationships"][0]["confidence"] == 90


def test_rbac_separates_review_and_share_approval() -> None:
    analyst = Principal("analyst", frozenset({Role.SOC}))
    admin = Principal("admin", frozenset({Role.ADMIN}))
    assert analyst.can(Permission.REVIEW_INTELLIGENCE)
    assert not analyst.can(Permission.SHARE_APPROVE)
    require(admin, Permission.SHARE_APPROVE)
    with pytest.raises(PermissionError):
        require(analyst, Permission.SHARE_APPROVE)


def test_reporting_refuses_evidence_free_claims() -> None:
    service = ReportingService()
    with pytest.raises(ValueError):
        service.build(title="Report", audience="board", findings=[], recommendations=[], evidence=[])
    report = service.build(
        title="Report",
        audience="board",
        findings=[{"title": "Finding", "severity": "high", "confidence": 90}],
        recommendations=["Validate exposure"],
        evidence=[{"source_url": "https://example.invalid/source"}],
    )
    assert report.human_review_required
    assert service.to_json(report)
