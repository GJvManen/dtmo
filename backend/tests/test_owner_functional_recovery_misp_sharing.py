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
    reason="MISP sharing functional recovery executes only in the dedicated exact-head browser workflow",
)


async def _seed_item() -> str:
    database = Database()
    item = IntelligenceItem(
        source_id="functional-recovery-sharing",
        external_id=f"sharing-{uuid4()}",
        item_type=IntelligenceType.ADVISORY,
        title="Functional recovery governed sharing advisory",
        summary="Repository-controlled MISP sharing fixture with separate human review and approval.",
        canonical_url="https://example.invalid/sharing-recovery",
        content_hash=uuid4().hex * 2,
        severity=IntelligenceSeverity.MEDIUM,
        confidence_score=90,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_rationale=["repository-controlled sharing fixture"],
        education_relevance=87,
        review_status="candidate",
        share_approved=False,
        metadata_json={"fixture": "misp-sharing-functional-recovery"},
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
async def test_sharing_requires_separate_human_review_and_approval_then_exports_unpublished_misp_event() -> None:
    """Prove the canonical human-governed sharing chain and real server-side MISP delivery adapter."""
    item_id = await _seed_item()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()

            reviewer_context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-sharing-reviewer",
                    "X-DTMO-Roles": "admin",
                }
            )
            reviewer_page = await reviewer_context.new_page()
            await reviewer_page.goto(f"{BASE_URL}/workbench/sharing?item={item_id}")
            await expect(reviewer_page.get_by_role("heading", name="Sharing & Exchange", exact=True)).to_be_visible()
            await expect(reviewer_page.get_by_text("Human review required before sharing approval", exact=True)).to_be_visible()
            await expect(reviewer_page.get_by_role("button", name="Record review", exact=True)).to_be_enabled()
            await expect(reviewer_page.get_by_role("button", name="Approve sharing", exact=True)).to_be_disabled()
            await expect(reviewer_page.get_by_role("button", name="Export approved intelligence", exact=True)).to_be_disabled()

            await reviewer_page.get_by_role("button", name="Record review", exact=True).click()
            await expect(
                reviewer_page.get_by_text("Review recorded in canonical DTMO governance state.", exact=True)
            ).to_be_visible()
            await expect(
                reviewer_page.get_by_text("This principal performed the review and therefore cannot approve sharing for the same item.", exact=True)
            ).to_be_visible()
            await expect(reviewer_page.get_by_role("button", name="Approve sharing", exact=True)).to_be_disabled()
            await reviewer_context.close()

            approver_context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-sharing-approver",
                    "X-DTMO-Roles": "admin",
                }
            )
            approver_page = await approver_context.new_page()
            await approver_page.goto(f"{BASE_URL}/workbench/sharing?item={item_id}")
            await expect(approver_page.get_by_role("button", name="Approve sharing", exact=True)).to_be_enabled()
            await expect(approver_page.get_by_role("button", name="Export approved intelligence", exact=True)).to_be_disabled()

            await approver_page.get_by_role("button", name="Approve sharing", exact=True).click()
            await expect(
                approver_page.get_by_text("Share approval recorded in canonical DTMO governance state.", exact=True)
            ).to_be_visible()
            await expect(approver_page.get_by_role("button", name="Export approved intelligence", exact=True)).to_be_enabled()
            await expect(approver_page.get_by_text("configured", exact=True)).to_be_visible()

            await approver_page.get_by_role("button", name="Export approved intelligence", exact=True).click()
            await expect(
                approver_page.get_by_text("MISP export recorded in canonical DTMO governance state.", exact=True)
            ).to_be_visible()
            export_history = approver_page.locator(".export-history")
            await expect(export_history.get_by_text("success", exact=True)).to_be_visible()
            await expect(export_history.get_by_text("MISP event repo-misp-4242", exact=False)).to_be_visible()
            await expect(approver_page.get_by_text("Publication authority: no", exact=True)).to_be_visible()
            await expect(approver_page.get_by_text("Synchronization authority: no", exact=True)).to_be_visible()
            await expect(approver_page.get_by_role("button", name="Export approved intelligence", exact=True)).to_be_disabled()

            await approver_page.reload()
            export_history = approver_page.locator(".export-history")
            await expect(export_history.get_by_text("success", exact=True)).to_be_visible()
            await expect(export_history.get_by_text("MISP event repo-misp-4242", exact=False)).to_be_visible()
            assert await approver_page.locator('a[href^="/ui/"]').count() == 0

            await approver_context.close()
            await browser.close()
    finally:
        await _cleanup(item_id)
