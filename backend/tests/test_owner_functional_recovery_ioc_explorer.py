from __future__ import annotations

import os
from uuid import UUID, uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete

from dtmo.intelligence.model import ConfidenceLevel, IntelligenceSeverity, IntelligenceType
from dtmo.persistence.models import IntelligenceItem, IntelOwlEnrichmentRecord
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
E2E_ENABLED = bool(BASE_URL)

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="IOC Explorer functional recovery executes only in the dedicated exact-head same-origin workflow",
)


async def _seed_ioc_fixture() -> tuple[str, str, str]:
    database = Database()
    token = uuid4().hex
    observable_value = f"ioc-{token}.example.invalid"
    source_id = f"ioc-functional-recovery-{token}"
    item = IntelligenceItem(
        source_id=source_id,
        external_id=f"ioc-functional-recovery-{token}",
        item_type=IntelligenceType.ADVISORY,
        title=f"IOC functional recovery advisory {token}",
        summary="Repository-controlled fixture proving the canonical IOC inventory read/filter/pivot journey.",
        canonical_url=f"https://example.invalid/ioc-functional-recovery/{token}",
        content_hash=uuid4().hex * 2,
        severity=IntelligenceSeverity.HIGH,
        confidence_score=93,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_rationale=["repository-controlled IOC browser acceptance fixture"],
        education_relevance=90,
        review_status="candidate",
        share_approved=False,
        metadata_json={"fixture": "repository-controlled-ioc-functional-recovery"},
    )
    record = IntelOwlEnrichmentRecord(
        item=item,
        job_id=f"ioc-functional-recovery-job-{token}",
        observable_type="domain",
        observable_value=observable_value,
        handling="TLP:AMBER",
        analyzers=["repository-controlled-fixture"],
        status="completed",
        partial=False,
        reports=[],
        raw_result={"fixture": True},
        requested_by="owner-functional-recovery-ioc",
        external_share_authorized=False,
        local_compromise_proven=False,
    )
    async for session in database.session():
        session.add(item)
        session.add(record)
        await session.flush()
        item_id = str(item.id)
        await session.commit()
        break
    await database.close()
    return item_id, observable_value, source_id


async def _cleanup(item_id: str) -> None:
    database = Database()
    async for session in database.session():
        await session.execute(delete(IntelligenceItem).where(IntelligenceItem.id == UUID(item_id)))
        await session.commit()
        break
    await database.close()


@pytest.mark.asyncio
async def test_ioc_explorer_reads_real_inventory_filters_and_opens_canonical_pivot() -> None:
    """Prove the canonical IOC read/filter/pivot path without route interception.

    This is repository-controlled exact-head evidence against temporary PostgreSQL
    persistence. It is not live-source, staging, production-equivalent, pentest,
    owner-acceptance or independent-assurance evidence.
    """
    item_id, observable_value, source_id = await _seed_ioc_fixture()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "owner-functional-recovery-ioc",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await context.new_page()

            await page.goto(f"{BASE_URL}/workbench/intelligence/iocs")
            await expect(page.get_by_role("heading", name="IOC Explorer", exact=True)).to_be_visible()
            await expect(page.get_by_text(observable_value, exact=True)).to_be_visible()

            await page.get_by_label("Indicator or context").fill(observable_value)
            await page.get_by_label("Type").select_option("domain")
            await page.get_by_label("Severity").select_option("high")
            await page.get_by_label("Source").select_option(source_id)
            await page.get_by_label("Minimum confidence").fill("90")

            result = page.locator("article.intelligence-result").filter(has_text=observable_value)
            await expect(result).to_be_visible()
            await expect(page.get_by_text("1 shown", exact=True)).to_be_visible()
            await expect(result.get_by_text("confidence 93/100", exact=False)).to_be_visible()
            await expect(result.get_by_text("TLP:AMBER", exact=False)).to_be_visible()

            await expect(result.get_by_role("link", name="Open source intelligence")).to_have_attribute(
                "href", f"/workbench/intelligence?item={item_id}"
            )
            await expect(result.get_by_role("link", name="Enrich / analyze selected IOC")).to_have_attribute(
                "href",
                f"/workbench/analysis?item={item_id}&observable_type=domain&observable_value={observable_value}",
            )
            await expect(result.get_by_role("link", name="Graph")).to_have_attribute(
                "href", f"/workbench/intelligence/graph?item={item_id}"
            )
            await expect(result.get_by_role("link", name="Investigate")).to_have_attribute(
                "href", f"/workbench/investigations?item={item_id}"
            )
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await result.get_by_role("link", name="Open source intelligence").click()
            await expect(page).to_have_url(f"{BASE_URL}/workbench/intelligence?item={item_id}")
            await expect(page.get_by_text(source_id, exact=True)).to_be_visible()

            await context.close()
            await browser.close()
    finally:
        await _cleanup(item_id)
