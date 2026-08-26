from __future__ import annotations

import os
from uuid import UUID, uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete

from dtmo.intelligence.model import ConfidenceLevel, IntelligenceSeverity, IntelligenceType
from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.opencti import OpenCTIMappingRevision, OpenCTIObjectMapping
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason="Knowledge Graph functional recovery executes only in the dedicated same-origin browser workflow",
)


async def _seed_graph() -> tuple[str, str, str]:
    database = Database()
    stix_id = f"indicator--{uuid4()}"
    opencti_id = f"opencti-{uuid4()}"
    item = IntelligenceItem(
        source_id="functional-recovery-graph",
        external_id=f"graph-{uuid4()}",
        item_type=IntelligenceType.ADVISORY,
        title="Functional recovery graph advisory",
        summary="Repository-controlled graph fixture.",
        canonical_url="https://example.invalid/graph-recovery",
        content_hash=uuid4().hex * 2,
        severity=IntelligenceSeverity.HIGH,
        confidence_score=88,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_rationale=["repository-controlled graph fixture"],
        education_relevance=93,
        review_status="candidate",
        share_approved=False,
        metadata_json={"fixture": "knowledge-graph-functional-recovery"},
    )
    async for session in database.session():
        session.add(item)
        await session.flush()
        mapping = OpenCTIObjectMapping(
            item_id=item.id,
            opencti_id=opencti_id,
            stix_id=stix_id,
            entity_type="Indicator",
            parent_types=["Stix-Cyber-Observable"],
            markings=[{"definition": "TLP:CLEAR"}],
            confidence=87,
            upstream_created_at="2026-08-26T00:00:00Z",
            upstream_updated_at="2026-08-26T00:00:00Z",
            external_references=[{"source_name": "functional-recovery", "external_id": "GRAPH-1"}],
            provenance={"fixture": "repository-controlled", "read_only": True},
            snapshot_hash="a" * 64,
            external_share_authorized=False,
            local_compromise_proven=False,
        )
        session.add(mapping)
        await session.flush()
        session.add(
            OpenCTIMappingRevision(
                mapping_id=mapping.id,
                snapshot_hash="a" * 64,
                snapshot={"stix_id": stix_id, "entity_type": "Indicator"},
            )
        )
        await session.commit()
        item_id = str(item.id)
        break
    await database.close()
    return item_id, stix_id, opencti_id


async def _cleanup(item_id: str) -> None:
    database = Database()
    async for session in database.session():
        await session.execute(delete(IntelligenceItem).where(IntelligenceItem.id == UUID(item_id)))
        await session.commit()
        break
    await database.close()


@pytest.mark.asyncio
async def test_knowledge_graph_reads_persisted_mapping_and_entity_detail_without_upstream_call() -> None:
    """Prove persisted graph and entity-detail reads without browser mocks or OpenCTI execution."""
    item_id, stix_id, opencti_id = await _seed_graph()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-graph-analyst",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await context.new_page()
            await page.goto(f"{BASE_URL}/workbench/intelligence/graph?item={item_id}")

            await expect(page.get_by_role("heading", name="Knowledge Graph", exact=True)).to_be_visible()
            await expect(page.get_by_role("heading", name="Functional recovery graph advisory", exact=True)).to_be_visible()
            await expect(page.get_by_text("1 OpenCTI mappings", exact=True)).to_be_visible()
            await expect(page.get_by_text(stix_id, exact=True)).to_be_visible()

            await page.get_by_role("button", name=f"Open Indicator {stix_id}", exact=True).click()
            await expect(page.get_by_role("heading", name="Indicator", exact=True)).to_be_visible()
            await expect(page.get_by_text(opencti_id, exact=True)).to_be_visible()
            await expect(page.get_by_text("not authorized", exact=True)).to_be_visible()
            await expect(page.get_by_text("not proven", exact=True)).to_be_visible()
            await expect(page.get_by_text("1 revisions", exact=True)).to_be_visible()
            await expect(page.get_by_text("TLP:CLEAR", exact=True)).to_be_visible()
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await context.close()
            await browser.close()
    finally:
        await _cleanup(item_id)
