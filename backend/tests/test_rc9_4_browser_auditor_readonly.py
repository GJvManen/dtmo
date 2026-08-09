from __future__ import annotations

import os
from uuid import uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import func, select

from dtmo.audit.chain import AuditDecision
from dtmo.audit.store import append_persistent_audit_event, verify_persistent_audit_chain
from dtmo.persistence.audit_models import AuditEventRecord
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.4 browser E2E executes only in the dedicated auditor workflow",
)


async def _seed_audit_event() -> tuple[str, int]:
    database = Database()
    request_id = f"rc9-4-{uuid4()}"
    event_id = ""
    count = 0
    async for session in database.session():
        event = await session.run_sync(
            lambda sync_session: append_persistent_audit_event(
                sync_session,
                principal="synthetic-rc9-audit-seed",
                principal_type="human",
                action="rc9.audit.fixture",
                resource="synthetic:rc9-4",
                decision=AuditDecision.ALLOW,
                request_id=request_id,
                provenance_reference="synthetic://rc9-4/audit-fixture",
            )
        )
        event_id = str(event.event_id)
        await session.commit()
        count = int(await session.scalar(select(func.count()).select_from(AuditEventRecord)) or 0)
        break
    await database.close()
    return event_id, count


async def _audit_count_and_chain() -> tuple[int, bool]:
    database = Database()
    count = 0
    valid = False
    async for session in database.session():
        count = int(await session.scalar(select(func.count()).select_from(AuditEventRecord)) or 0)
        valid, _ = await session.run_sync(verify_persistent_audit_chain)
        break
    await database.close()
    return count, valid


@pytest.mark.asyncio
async def test_auditor_browser_is_backend_authorized_and_read_only() -> None:
    event_id, before_count = await _seed_audit_event()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        analyst_context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "alice-analyst",
                "X-DTMO-Roles": "analyst",
            }
        )
        analyst_page = await analyst_context.new_page()
        await analyst_page.goto(f"{BASE_URL}/ui/auditor")
        await expect(analyst_page.get_by_test_id("auditor-principal")).to_contain_text("alice-analyst")
        await expect(analyst_page.get_by_test_id("audit-panel")).to_be_hidden()
        denied = await analyst_page.evaluate(
            """async () => {
              const response = await fetch('/api/v1/audit/events');
              return {status: response.status, body: await response.json()};
            }"""
        )
        assert denied["status"] == 403
        await analyst_context.close()

        auditor_context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "erin-auditor",
                "X-DTMO-Roles": "auditor",
            }
        )
        auditor_page = await auditor_context.new_page()
        await auditor_page.goto(f"{BASE_URL}/ui/auditor")
        await expect(auditor_page.get_by_test_id("auditor-principal")).to_contain_text("erin-auditor")
        await expect(auditor_page.get_by_test_id("audit-panel")).to_be_visible()
        await auditor_page.get_by_test_id("load-audit").click()
        await expect(auditor_page.get_by_test_id("audit-status")).to_have_attribute(
            "data-state", "success"
        )
        await expect(auditor_page.get_by_test_id("audit-events")).to_contain_text(
            "rc9.audit.fixture"
        )
        assert await auditor_page.locator(f'[data-event-id="{event_id}"]').count() == 1
        await auditor_context.close()
        await browser.close()

    after_count, chain_valid = await _audit_count_and_chain()
    assert after_count == before_count
    assert chain_valid is True
