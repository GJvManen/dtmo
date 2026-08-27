from __future__ import annotations

import os
from uuid import UUID, uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete

from dtmo.intelligence.model import ConfidenceLevel, IntelligenceSeverity, IntelligenceType
from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason="Sharing functional recovery executes only in the dedicated exact-head browser workflow",
)


async def _seed_item() -> str:
    database = Database()
    item = IntelligenceItem(
        source_id="functional-recovery-sharing",
        external_id=f"sharing-{uuid4()}",
        item_type=IntelligenceType.ADVISORY,
        title="Functional recovery sharing advisory",
        summary="Repository-controlled governed MISP export fixture.",
        canonical_url="https://example.invalid/sharing-recovery",
        content_hash=uuid4().hex * 2,
        severity=IntelligenceSeverity.HIGH,
        confidence_score=92,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_rationale=["repository-controlled sharing fixture"],
        education_relevance=90,
        review_status="candidate",
        share_approved=False,
        metadata_json={"fixture": "sharing-functional-recovery"},
    )
    async for session in database.session():
        session.add(item)
        await session.commit()
        item_id = str(item.id)
        break
    await database.close()
    return item_id


async def _cleanup(item_id: str) -> None:
    database = Database()
    async for session in database.session():
        await session.execute(delete(IntelligenceItem).where(IntelligenceItem.id == UUID(item_id)))
        await session.commit()
        break
    await database.close()


@pytest.mark.asyncio
async def test_sharing_requires_separate_humans_then_persists_unpublished_misp_export() -> None:
    """Prove review -> separate approval -> unpublished MISP export without browser mocks.

    The loopback MISP service is repository-controlled integration evidence only.
    Export evidence does not grant MISP publication or synchronization authority and
    does not establish live upstream health, upstream truth or production readiness.
    """
    item_id = await _seed_item()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()

            reviewer = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-sharing-reviewer",
                    "X-DTMO-Roles": "admin",
                }
            )
            reviewer_page = await reviewer.new_page()
            await reviewer_page.goto(f"{BASE_URL}/workbench/sharing?item={item_id}")
            await expect(reviewer_page.get_by_role("heading", name="Sharing & Exchange", exact=True)).to_be_visible()
            await expect(reviewer_page.get_by_role("button", name="Record review", exact=True)).to_be_enabled()
            await expect(reviewer_page.get_by_role("button", name="Approve sharing", exact=True)).to_be_disabled()

            await reviewer_page.get_by_role("button", name="Record review", exact=True).click()
            await expect(
                reviewer_page.get_by_text("Reviewed by functional-recovery-sharing-reviewer", exact=True)
            ).to_be_visible()
            await expect(
                reviewer_page.get_by_text(
                    "This principal performed the review and therefore cannot approve sharing for the same item.",
                    exact=True,
                )
            ).to_be_visible()
            await expect(reviewer_page.get_by_role("button", name="Approve sharing", exact=True)).to_be_disabled()
            await reviewer.close()

            approver = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-sharing-approver",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await approver.new_page()
            await page.goto(f"{BASE_URL}/workbench/sharing?item={item_id}")
            await expect(page.get_by_role("button", name="Approve sharing", exact=True)).to_be_enabled()
            await page.get_by_role("button", name="Approve sharing", exact=True).click()

            await expect(
                page.get_by_text("Approved by functional-recovery-sharing-approver", exact=True)
            ).to_be_visible()
            export_button = page.get_by_role("button", name="Export approved intelligence", exact=True)
            await expect(export_button).to_be_enabled()
            await export_button.click()

            history = page.locator(".surface").filter(has_text="MISP export history")
            await expect(history.get_by_text("success", exact=True)).to_be_visible()
            await expect(
                history.get_by_text("MISP event repo-misp-4242 · distribution 0 · tlp:amber", exact=True)
            ).to_be_visible()
            await expect(page.get_by_text("Publication authority: no", exact=True)).to_be_visible()
            await expect(page.get_by_text("Synchronization authority: no", exact=True)).to_be_visible()

            await page.reload()
            history = page.locator(".surface").filter(has_text="MISP export history")
            await expect(
                history.get_by_text("MISP event repo-misp-4242 · distribution 0 · tlp:amber", exact=True)
            ).to_be_visible()
            await expect(page.get_by_role("button", name="Export approved intelligence", exact=True)).to_be_disabled()
            await expect(
                page.get_by_text(
                    "Not authorized or implemented in this workspace. Exported MISP events remain unpublished.",
                    exact=True,
                )
            ).to_be_visible()
            assert await page.get_by_role("button", name="Publish", exact=True).count() == 0
            assert await page.get_by_role("button", name="Synchronize", exact=True).count() == 0
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await approver.close()
            await browser.close()
    finally:
        await _cleanup(item_id)
