from __future__ import annotations

import os

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.10 session-status E2E executes only in the dedicated browser workflow",
)

SURFACES = (
    ("share_approval", "/ui/share-approval", "a11y-admin", "admin", "principal", "review-button"),
    ("analyst_search", "/ui/analyst-search", "a11y-analyst", "analyst", "analyst-principal", "search-submit"),
    ("ciso_token_revocation", "/ui/ciso-security", "a11y-ciso", "ciso", "ciso-principal", "revoke-submit"),
    ("auditor_read_only", "/ui/auditor", "a11y-auditor", "auditor", "auditor-principal", "load-audit"),
)


@pytest.mark.asyncio
async def test_session_resolution_is_programmatically_announced_on_all_critical_surfaces() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        for name, path, subject, roles, principal_test_id, ready_test_id in SURFACES:
            context = await browser.new_context(
                extra_http_headers={"X-DTMO-Subject": subject, "X-DTMO-Roles": roles}
            )
            page = await context.new_page()
            response = await page.goto(f"{BASE_URL}{path}")
            assert response is not None and response.ok, {
                "surface": name,
                "status": None if response is None else response.status,
            }

            principal = page.get_by_test_id(principal_test_id)
            await expect(principal).to_have_attribute("role", "status")
            await expect(principal).to_have_attribute("aria-live", "polite")
            await expect(principal).to_have_attribute("aria-atomic", "true")
            await expect(principal).to_contain_text(subject)
            await expect(principal).not_to_contain_text("Resolving authenticated principal")

            ready = page.get_by_test_id(ready_test_id)
            await expect(ready).to_be_visible()
            await context.close()
        await browser.close()
