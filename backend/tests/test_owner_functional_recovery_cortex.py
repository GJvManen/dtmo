from __future__ import annotations

import os
from uuid import UUID, uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete

from dtmo.intelligence.model import ConfidenceLevel, IntelligenceSeverity, IntelligenceType
from dtmo.persistence.cortex import CortexAnalysisRecord
from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason="Cortex functional recovery executes only in the dedicated exact-head browser workflow",
)


async def _seed_item() -> tuple[str, str]:
    database = Database()
    observable = f"cortex-{uuid4().hex[:10]}.example.invalid"
    item = IntelligenceItem(
        source_id="functional-recovery-cortex",
        external_id=f"cortex-{uuid4()}",
        item_type=IntelligenceType.INDICATOR,
        title="Functional recovery Cortex indicator",
        summary="Repository-controlled analyzer-only Cortex fixture.",
        canonical_url="https://example.invalid/cortex-recovery",
        content_hash=uuid4().hex * 2,
        severity=IntelligenceSeverity.MEDIUM,
        confidence_score=90,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_rationale=["repository-controlled Cortex fixture"],
        education_relevance=88,
        review_status="candidate",
        share_approved=False,
        metadata_json={"fixture": "cortex-functional-recovery"},
    )
    async for session in database.session():
        session.add(item)
        await session.commit()
        item_id = str(item.id)
        break
    await database.close()
    return item_id, observable


async def _cleanup(item_id: str) -> None:
    database = Database()
    async for session in database.session():
        await session.execute(
            delete(CortexAnalysisRecord).where(CortexAnalysisRecord.item_id == UUID(item_id))
        )
        await session.execute(delete(IntelligenceItem).where(IntelligenceItem.id == UUID(item_id)))
        await session.commit()
        break
    await database.close()


@pytest.mark.asyncio
async def test_cortex_executes_allowlisted_analyzer_and_persists_history_without_responder_authority() -> None:
    """Prove real server-side Cortex adapter execution against a bounded emulator.

    The emulator is repository-controlled integration evidence only. Analyzer output
    remains enrichment evidence and does not prove local compromise, authorize
    sharing, or grant responder/automation side-effect authority.
    """
    item_id, observable = await _seed_item()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-cortex-human",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await context.new_page()
            await page.goto(
                f"{BASE_URL}/workbench/analysis?item={item_id}"
                f"&observable_type=domain&observable_value={observable}"
            )

            await expect(page.get_by_role("heading", name="Analysis & Enrichment", exact=True)).to_be_visible()
            cortex_capability = page.locator(".capability-card").filter(has_text="Cortex")
            await expect(cortex_capability.get_by_role("heading", name="Enabled", exact=True)).to_be_visible()
            await expect(cortex_capability.get_by_text("1 allowlisted analyzers", exact=True)).to_be_visible()
            await expect(page.get_by_role("button", name="Run Cortex", exact=True)).to_be_enabled()

            await page.get_by_role("button", name="Run Cortex", exact=True).click()
            await expect(
                page.get_by_text("Cortex analyzer result persisted as governed evidence.", exact=True)
            ).to_be_visible()
            cortex_history = page.locator(".analysis-history-panel").filter(has_text="Cortex history")
            await expect(cortex_history.get_by_text("Job repo-cortex-4242", exact=True)).to_be_visible()
            await expect(cortex_history.get_by_text("functional_domain · TLP 2", exact=True)).to_be_visible()
            await expect(
                cortex_history.get_by_text("External share: no · Local compromise proven: no", exact=True)
            ).to_be_visible()
            await cortex_history.get_by_text("Persisted result", exact=True).click()
            persisted_result = cortex_history.locator("pre")
            await expect(persisted_result).to_contain_text('"classification": "repository-controlled"')
            await expect(persisted_result).to_contain_text('"analyzer_only": true')
            await expect(persisted_result).to_contain_text('"responder_action": false')

            await page.reload()
            cortex_history = page.locator(".analysis-history-panel").filter(has_text="Cortex history")
            await expect(cortex_history.get_by_text("Job repo-cortex-4242", exact=True)).to_be_visible()
            await expect(cortex_history.get_by_text("functional_domain · TLP 2", exact=True)).to_be_visible()
            await expect(page.get_by_role("heading", name="No responder authority", exact=True)).to_be_visible()
            await expect(page.get_by_text("Loaded canonical item:", exact=False)).to_contain_text(item_id)
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await context.close()
            await browser.close()
    finally:
        await _cleanup(item_id)
