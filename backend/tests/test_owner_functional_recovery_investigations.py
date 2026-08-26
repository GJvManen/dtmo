from __future__ import annotations

import os
from uuid import UUID, uuid4

import httpx
import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete

from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
E2E_ENABLED = bool(BASE_URL)

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="Investigations functional recovery executes only in the dedicated exact-head same-origin workflow",
)


async def _ingest_fixture(title: str) -> str:
    payload = {
        "source_id": "functional-recovery",
        "external_id": f"investigation-{uuid4()}",
        "item_type": "advisory",
        "title": title,
        "summary": "Repository-controlled investigation fixture for exact-head functional browser acceptance.",
        "canonical_url": "https://example.invalid/investigation-evidence",
        "severity": "high",
        "confidence": 95,
        "education_relevance": 90,
        "tags": ["functional-recovery", "tlp:amber"],
        "provenance": [
            {
                "source_url": "https://example.invalid/investigation-evidence",
                "publisher": "functional-recovery",
                "confidence": 95,
            }
        ],
        "raw_payload": {"fixture": "investigations-functional-recovery"},
    }
    async with httpx.AsyncClient(
        base_url=BASE_URL,
        headers={
            "X-DTMO-Subject": "functional-recovery-investigations-ingest",
            "X-DTMO-Roles": "admin",
        },
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
        await session.execute(delete(IntelligenceItem).where(IntelligenceItem.id == UUID(item_id)))
        await session.commit()
        break
    await database.close()


@pytest.mark.asyncio
async def test_investigations_creates_governed_case_and_reads_durable_history() -> None:
    """Prove the canonical Investigations handoff through the real DTMO adapter.

    The upstream endpoint is a repository-controlled CI emulator, not a live TheHive
    environment. This proves DTMO browser/API/persistence behavior only and does not
    constitute staging, production-equivalent or independent-assurance evidence.
    """
    suffix = uuid4().hex[:8]
    title = f"Investigation recovery {suffix}"
    case_summary = f"Reviewed minimized case summary {suffix}"
    item_id = await _ingest_fixture(title)

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-investigations-human",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await context.new_page()
            await page.goto(f"{BASE_URL}/workbench/investigations?item={item_id}")

            await expect(page.get_by_role("heading", name="Investigations", exact=True)).to_be_visible()
            await expect(page.get_by_role("heading", name=title, exact=True)).to_be_visible()
            await expect(page.get_by_text("functional-recovery", exact=True)).to_be_visible()
            await expect(page.get_by_text("1", exact=True).first).to_be_visible()
            await expect(page.get_by_text("tlp:amber", exact=True)).to_be_visible()
            await expect(page.get_by_text("configured", exact=True)).to_be_visible()

            await page.get_by_label("Reviewed case summary").fill(case_summary)
            await page.get_by_label("TLP").select_option("amber")
            await page.get_by_label("PAP").select_option("amber")
            create = page.get_by_role("button", name="Create TheHive case handoff")
            await expect(create).to_be_enabled()
            await create.click()

            await expect(page.get_by_text("TheHive case handoff delivered as case #4242.", exact=True)).to_be_visible()
            history = page.locator(".handoff-record").filter(has_text="TheHive case #4242")
            await expect(history).to_be_visible()
            await expect(history).to_contain_text("functional-recovery-org")
            await expect(history).to_contain_text("requested by functional-recovery-investigations-human")
            await expect(history).to_contain_text("TLP amber · PAP amber")

            await expect(page.get_by_text("External sharing", exact=True)).to_be_visible()
            await expect(page.get_by_text("not authorized", exact=True)).to_be_visible()
            await expect(page.get_by_text("Local compromise", exact=True)).to_be_visible()
            await expect(page.get_by_text("not proven", exact=True)).to_be_visible()
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await context.close()
            await browser.close()
    finally:
        await _cleanup(item_id)
