from __future__ import annotations

import os
from uuid import UUID, uuid4

import httpx
import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete

from dtmo.persistence.models import IntelOwlEnrichmentRecord, IntelligenceItem
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
E2E_ENABLED = bool(BASE_URL)

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="Analysis functional recovery executes only in the dedicated exact-head same-origin workflow",
)


async def _ingest_fixture(title: str) -> str:
    payload = {
        "source_id": "functional-recovery",
        "external_id": f"analysis-{uuid4()}",
        "item_type": "indicator",
        "title": title,
        "summary": "Repository-controlled Analysis & Enrichment fixture.",
        "canonical_url": "https://example.invalid/analysis-evidence",
        "severity": "medium",
        "confidence": 91,
        "education_relevance": 88,
        "tags": ["functional-recovery", "tlp:amber"],
        "provenance": [{"source_url": "https://example.invalid/analysis-evidence", "publisher": "functional-recovery", "confidence": 91}],
        "raw_payload": {"fixture": "analysis-functional-recovery"},
    }
    async with httpx.AsyncClient(
        base_url=BASE_URL,
        headers={"X-DTMO-Subject": "functional-recovery-analysis-ingest", "X-DTMO-Roles": "admin"},
        timeout=30,
    ) as client:
        response = await client.post("/api/v1/intelligence", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["share_approved"] is False
    return str(body["id"])


async def _cleanup(item_id: str) -> None:
    database = Database()
    async for session in database.session():
        await session.execute(delete(IntelOwlEnrichmentRecord).where(IntelOwlEnrichmentRecord.item_id == UUID(item_id)))
        await session.execute(delete(IntelligenceItem).where(IntelligenceItem.id == UUID(item_id)))
        await session.commit()
        break
    await database.close()


@pytest.mark.asyncio
async def test_analysis_executes_allowlisted_intelowl_and_persists_governed_history() -> None:
    suffix = uuid4().hex[:8]
    title = f"Analysis recovery {suffix}"
    observable = f"analysis-{suffix}.example.invalid"
    item_id = await _ingest_fixture(title)

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(extra_http_headers={
                "X-DTMO-Subject": "functional-recovery-analysis-human",
                "X-DTMO-Roles": "admin",
            })
            page = await context.new_page()
            await page.goto(f"{BASE_URL}/workbench/analysis?item={item_id}&observable_type=domain&observable_value={observable}")

            await expect(page.get_by_role("heading", name="Analysis & Enrichment", exact=True)).to_be_visible()
            await expect(page.get_by_role("heading", name="IntelOwl", exact=True).first).to_be_visible()
            await expect(page.get_by_text("1 allowlisted analyzers", exact=True).first).to_be_visible()
            await expect(page.get_by_role("button", name="Run IntelOwl", exact=True)).to_be_enabled()

            await page.get_by_role("button", name="Run IntelOwl", exact=True).click()
            await expect(page.get_by_text("IntelOwl enrichment persisted as governed evidence.", exact=True)).to_be_visible()
            await expect(page.get_by_text("Job repo-intelowl-4242", exact=True)).to_be_visible()
            await expect(page.get_by_text("functional_domain", exact=True)).to_be_visible()
            await expect(page.get_by_text("External share: no · Local compromise proven: no", exact=True).first).to_be_visible()

            await page.reload()
            await expect(page.get_by_text("Job repo-intelowl-4242", exact=True)).to_be_visible()
            await expect(page.get_by_text("functional_domain", exact=True)).to_be_visible()
            await expect(page.get_by_text("Loaded canonical item:", exact=False)).to_contain_text(item_id)
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await context.close()
            await browser.close()
    finally:
        await _cleanup(item_id)
