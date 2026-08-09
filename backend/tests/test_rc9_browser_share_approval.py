from __future__ import annotations

import os
from uuid import UUID, uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import select

from dtmo.intelligence.model import ConfidenceLevel, IntelligenceSeverity, IntelligenceType
from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9 browser E2E executes only in the dedicated browser workflow",
)


async def _seed_candidate() -> str:
    database = Database()
    item = IntelligenceItem(
        source_id="rc9-browser-e2e",
        external_id=f"candidate-{uuid4()}",
        item_type=IntelligenceType.ADVISORY,
        title="RC9 browser governed decision fixture",
        summary="Synthetic browser E2E fixture",
        canonical_url="https://example.invalid/rc9-browser-e2e",
        content_hash="a" * 64,
        severity=IntelligenceSeverity.MEDIUM,
        confidence_score=80,
        confidence_level=ConfidenceLevel.HIGH,
        confidence_rationale=["synthetic browser E2E fixture"],
        education_relevance=80,
        review_status="candidate",
        share_approved=False,
        metadata_json={"fixture": "synthetic", "publish_approved": False},
    )
    async for session in database.session():
        session.add(item)
        await session.flush()
        item_id = str(item.id)
        await session.commit()
        break
    await database.close()
    return item_id


async def _assert_persisted_decision(item_id: str) -> None:
    database = Database()
    async for session in database.session():
        item = await session.scalar(
            select(IntelligenceItem).where(IntelligenceItem.id == UUID(item_id))
        )
        assert item is not None
        assert item.review_status == "reviewed"
        assert item.share_approved is True
        assert item.metadata_json["reviewed_by"] == "alice-admin"
        assert item.metadata_json["share_approved_by"] == "bob-publisher"
        assert item.metadata_json["fixture"] == "synthetic"
        break
    await database.close()


@pytest.mark.asyncio
async def test_browser_enforces_permission_visibility_and_separate_share_approval() -> None:
    item_id = await _seed_candidate()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        admin_context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "alice-admin",
                "X-DTMO-Roles": "admin",
            }
        )
        admin_page = await admin_context.new_page()
        await admin_page.goto(f"{BASE_URL}/ui/share-approval")
        await expect(admin_page.get_by_test_id("principal")).to_contain_text("alice-admin")
        await expect(admin_page.get_by_test_id("review-button")).to_be_visible()
        await expect(admin_page.get_by_test_id("share-button")).to_be_visible()
        await admin_page.get_by_test_id("item-id").fill(item_id)
        await admin_page.get_by_test_id("review-button").click()
        await expect(admin_page.get_by_test_id("result")).to_contain_text('"review_status": "reviewed"')
        await expect(admin_page.get_by_test_id("result")).to_contain_text('"share_approved": false')

        await admin_page.get_by_test_id("share-button").click()
        await expect(admin_page.get_by_test_id("result")).to_contain_text('"status": 409')
        await expect(admin_page.get_by_test_id("result")).to_contain_text(
            "share approval must be performed by a different principal"
        )
        await admin_context.close()

        publisher_context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "bob-publisher",
                "X-DTMO-Roles": "publisher",
            }
        )
        publisher_page = await publisher_context.new_page()
        await publisher_page.goto(f"{BASE_URL}/ui/share-approval")
        await expect(publisher_page.get_by_test_id("principal")).to_contain_text("bob-publisher")
        await expect(publisher_page.get_by_test_id("review-button")).to_be_hidden()
        await expect(publisher_page.get_by_test_id("share-button")).to_be_visible()
        await publisher_page.get_by_test_id("item-id").fill(item_id)
        await publisher_page.get_by_test_id("share-button").click()
        await expect(publisher_page.get_by_test_id("result")).to_contain_text('"status": 200')
        await expect(publisher_page.get_by_test_id("result")).to_contain_text('"share_approved": true')
        await publisher_context.close()

        service_context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "connector-service",
                "X-DTMO-Roles": "service_account",
            }
        )
        service_page = await service_context.new_page()
        await service_page.goto(f"{BASE_URL}/ui/share-approval")
        await expect(service_page.get_by_test_id("review-button")).to_be_hidden()
        await expect(service_page.get_by_test_id("share-button")).to_be_hidden()
        await service_context.close()

        await browser.close()

    await _assert_persisted_decision(item_id)
