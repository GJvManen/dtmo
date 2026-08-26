from __future__ import annotations

import os
from uuid import UUID, uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete

from dtmo.intelligence.model import ConfidenceLevel, IntelligenceSeverity, IntelligenceType
from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="Threat Intelligence functional recovery executes only in the dedicated same-origin browser workflow",
)


async def _seed_intelligence() -> tuple[str, str]:
    database = Database()
    external_id = f"functional-recovery-{uuid4()}"
    item = IntelligenceItem(
        source_id="functional-recovery-browser",
        external_id=external_id,
        item_type=IntelligenceType.ADVISORY,
        title="Functional recovery ransomware advisory",
        summary="Repository-controlled canonical intelligence fixture used to prove the unmocked Threat Intelligence read path.",
        canonical_url="https://example.invalid/functional-recovery-ransomware",
        content_hash=uuid4().hex * 2,
        severity=IntelligenceSeverity.HIGH,
        confidence_score=91,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_rationale=["repository-controlled exact-head browser acceptance fixture"],
        education_relevance=96,
        review_status="candidate",
        share_approved=False,
        metadata_json={
            "fixture": "repository-controlled-functional-recovery",
            "cve_ids": ["CVE-2026-4242"],
            "known_exploited": True,
            "vendor": "Example Vendor",
            "product": "Example Product",
            "tags": ["ransomware", "education"],
        },
    )
    async for session in database.session():
        session.add(item)
        await session.flush()
        item_id = str(item.id)
        await session.commit()
        break
    await database.close()
    return item_id, external_id


async def _cleanup(item_id: str) -> None:
    database = Database()
    async for session in database.session():
        await session.execute(delete(IntelligenceItem).where(IntelligenceItem.id == UUID(item_id)))
        await session.commit()
        break
    await database.close()


@pytest.mark.asyncio
async def test_threat_intelligence_reads_real_persistence_and_opens_real_detail() -> None:
    """Prove the canonical recent/detail/pivot journey without browser route interception.

    This is repository-controlled exact-head evidence against temporary PostgreSQL
    persistence. It is not live-source, staging, production-equivalent, pentest,
    owner-acceptance or independent-assurance evidence.
    """
    item_id, _ = await _seed_intelligence()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-analyst",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await context.new_page()

            await page.goto(f"{BASE_URL}/workbench/intelligence")
            await expect(page.get_by_role("heading", name="Threat Intelligence", exact=True)).to_be_visible()
            await expect(page.get_by_text("Recent canonical intelligence", exact=True)).to_be_visible()
            await expect(page.get_by_text("Functional recovery ransomware advisory", exact=True).first).to_be_visible()

            await page.get_by_role("button", name="Open Functional recovery ransomware advisory").click()
            await expect(page.get_by_role("heading", name="Functional recovery ransomware advisory", level=3)).to_be_visible()
            await expect(page.get_by_text("functional-recovery-browser", exact=True)).to_be_visible()
            await expect(page.get_by_text("96/100", exact=True)).to_be_visible()
            await expect(page.get_by_text("91/100 · high", exact=True)).to_be_visible()
            await expect(page.get_by_text("candidate", exact=True)).to_be_visible()
            await expect(page.get_by_text("Not approved for sharing", exact=True)).to_be_visible()

            await expect(page.get_by_role("link", name="Analyze & enrich")).to_have_attribute(
                "href", f"/workbench/analysis?item={item_id}"
            )
            await expect(page.get_by_role("link", name="Review & share")).to_have_attribute(
                "href", f"/workbench/sharing?item={item_id}"
            )
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await context.close()
            await browser.close()
    finally:
        await _cleanup(item_id)
