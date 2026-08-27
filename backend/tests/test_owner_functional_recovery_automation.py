from __future__ import annotations

import os
from uuid import UUID

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete, select

from dtmo.connectors.state import ConnectorHealthEvent, ConnectorRuntimeState
from dtmo.persistence.models import IntelligenceItem
from dtmo.persistence.session import Database
from dtmo.sources import SourceDefinition, SourceRegistry

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
CISA_FIXTURE_ID = "CVE-2026-99999"
REGISTERED_SOURCE_ID = "github-global-advisories"
pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason="Automation functional recovery executes only in the dedicated exact-head browser workflow",
)


async def _seed_registered_source() -> None:
    database = Database()
    async for session in database.session():
        registry = SourceRegistry(session)
        existing = await registry.get(REGISTERED_SOURCE_ID)
        if existing is None:
            await registry.create(
                source_id=REGISTERED_SOURCE_ID,
                name="GitHub Global Security Advisories",
                source_type="json-feed",
                endpoint_url="https://api.github.com/advisories?per_page=100",
                enabled=True,
                interval_seconds=3600,
                reliability="high",
                secret_ref=None,
                actor="functional-recovery-automation-fixture",
            )
        elif not existing.enabled:
            await registry.update(
                existing,
                name=None,
                endpoint_url=None,
                enabled=True,
                interval_seconds=None,
                reliability=None,
                secret_ref=None,
                actor="functional-recovery-automation-fixture",
            )
    await database.close()


async def _assert_cisa_ingested() -> UUID:
    database = Database()
    item_id: UUID | None = None
    async for session in database.session():
        item = await session.scalar(
            select(IntelligenceItem).where(
                IntelligenceItem.source_id == "cisa-kev",
                IntelligenceItem.external_id == CISA_FIXTURE_ID,
            )
        )
        assert item is not None
        assert item.title == "Repository-controlled KEV automation fixture"
        assert item.review_status == "candidate"
        assert item.share_approved is False
        item_id = item.id
        break
    await database.close()
    assert item_id is not None
    return item_id


async def _cleanup() -> None:
    database = Database()
    async for session in database.session():
        item = await session.scalar(
            select(IntelligenceItem).where(
                IntelligenceItem.source_id == "cisa-kev",
                IntelligenceItem.external_id == CISA_FIXTURE_ID,
            )
        )
        if item is not None:
            await session.delete(item)
        await session.execute(
            delete(ConnectorHealthEvent).where(ConnectorHealthEvent.connector_id == "cisa-kev")
        )
        await session.execute(
            delete(ConnectorRuntimeState).where(ConnectorRuntimeState.connector_id == "cisa-kev")
        )
        await session.execute(
            delete(SourceDefinition).where(SourceDefinition.id == REGISTERED_SOURCE_ID)
        )
    await database.close()


@pytest.mark.asyncio
async def test_automation_executes_real_bounded_trigger_persists_state_and_rolls_back_source_pause() -> None:
    """Prove canonical automation trigger, durable observation and scope-limited rollback."""
    await _seed_registered_source()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-automation-human",
                    "X-DTMO-Roles": "admin",
                }
            )
            page = await context.new_page()
            await page.goto(f"{BASE_URL}/workbench/automation")
            await expect(page.get_by_role("heading", name="Automation & Playbooks", exact=True)).to_be_visible()

            cisa = page.locator("button.integration-row").filter(has_text="cisa-kev")
            await expect(cisa).to_be_visible()
            await cisa.click()
            await expect(page.get_by_role("button", name="Run bounded collection playbook", exact=True)).to_be_enabled()
            await page.get_by_role("button", name="Run bounded collection playbook", exact=True).click()

            result = page.get_by_text("Observed bounded execution result", exact=True).locator("..")
            await expect(result).to_contain_text("Connector: cisa-kev · status: completed")
            await expect(result).to_contain_text("Records: 1")

            persisted = page.locator('[data-automation-section="persisted-execution-observation"]')
            await expect(persisted.get_by_text("healthy", exact=True)).to_be_visible()
            await expect(persisted.get_by_text("not recorded", exact=True)).to_have_count(2)
            item_id = await _assert_cisa_ingested()

            registered = page.locator("button.integration-row").filter(has_text="GitHub Global Security Advisories")
            await expect(registered).to_be_visible()
            await registered.click()
            await expect(page.get_by_role("button", name="Pause registered source", exact=True)).to_be_enabled()
            await page.get_by_role("button", name="Pause registered source", exact=True).click()

            await expect(page.get_by_text("This connector does not advertise manual-run availability.", exact=False)).to_be_visible()
            await expect(page.get_by_role("button", name="Rollback this pause", exact=True)).to_be_enabled()
            await page.get_by_role("button", name="Rollback this pause", exact=True).click()

            await expect(page.get_by_role("button", name="Rollback this pause", exact=True)).to_have_count(0)
            await expect(page.get_by_role("button", name="Run bounded collection playbook", exact=True)).to_be_enabled()

            await page.reload()
            registered = page.locator("button.integration-row").filter(has_text="GitHub Global Security Advisories")
            await expect(registered).to_be_visible()
            await registered.click()
            await expect(page.get_by_role("button", name="Run bounded collection playbook", exact=True)).to_be_enabled()
            await expect(page.get_by_text("Rollback restores only the source enabled state", exact=False)).to_be_visible()
            assert await page.locator('a[href^="/ui/"]').count() == 0

            # The trigger created canonical evidence but did not review or share it.
            assert isinstance(item_id, UUID)
            await context.close()
            await browser.close()
    finally:
        await _cleanup()
