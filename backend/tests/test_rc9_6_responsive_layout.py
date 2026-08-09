from __future__ import annotations

import os

import pytest
from playwright.async_api import Page, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9 responsive browser E2E executes only in the dedicated browser workflow",
)

VIEWPORTS = {
    "mobile": {"width": 360, "height": 800},
    "tablet": {"width": 768, "height": 1024},
    "desktop": {"width": 1440, "height": 900},
}

SURFACES = (
    {
        "name": "share_approval",
        "path": "/ui/share-approval",
        "subject": "responsive-admin",
        "roles": "admin",
        "ready_test_id": "review-button",
        "controls": ("item-id", "review-button", "share-button"),
    },
    {
        "name": "analyst_search",
        "path": "/ui/analyst-search",
        "subject": "responsive-analyst",
        "roles": "analyst",
        "ready_test_id": "search-panel",
        "controls": ("search-query", "search-submit"),
    },
    {
        "name": "ciso_token_revocation",
        "path": "/ui/ciso-security",
        "subject": "responsive-ciso",
        "roles": "ciso",
        "ready_test_id": "revocation-panel",
        "controls": ("token-jti", "token-expiry", "revocation-reason", "revoke-submit"),
    },
    {
        "name": "auditor_read_only",
        "path": "/ui/auditor",
        "subject": "responsive-auditor",
        "roles": "auditor",
        "ready_test_id": "audit-panel",
        "controls": ("load-audit",),
    },
)


async def _assert_no_blocking_horizontal_overflow(page: Page, viewport_width: int) -> None:
    metrics = await page.evaluate(
        """() => ({
            documentScrollWidth: document.documentElement.scrollWidth,
            documentClientWidth: document.documentElement.clientWidth,
            bodyScrollWidth: document.body.scrollWidth,
        })"""
    )
    assert metrics["documentClientWidth"] == viewport_width
    assert metrics["documentScrollWidth"] <= viewport_width + 1, metrics
    assert metrics["bodyScrollWidth"] <= viewport_width + 1, metrics


async def _assert_control_usable(page: Page, test_id: str, viewport_width: int) -> None:
    control = page.get_by_test_id(test_id)
    await expect(control).to_be_visible()
    box = await control.bounding_box()
    assert box is not None
    assert box["width"] >= 24
    assert box["height"] >= 24
    assert box["x"] >= -1
    assert box["x"] + box["width"] <= viewport_width + 1, {
        "test_id": test_id,
        "box": box,
        "viewport_width": viewport_width,
    }


@pytest.mark.asyncio
async def test_accepted_critical_surfaces_are_usable_at_representative_viewports() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        for viewport_name, viewport in VIEWPORTS.items():
            for surface in SURFACES:
                context = await browser.new_context(
                    viewport=viewport,
                    extra_http_headers={
                        "X-DTMO-Subject": surface["subject"],
                        "X-DTMO-Roles": surface["roles"],
                    },
                )
                page = await context.new_page()
                response = await page.goto(f"{BASE_URL}{surface['path']}")
                assert response is not None and response.ok, {
                    "viewport": viewport_name,
                    "surface": surface["name"],
                    "status": None if response is None else response.status,
                }

                await expect(page.get_by_test_id(surface["ready_test_id"])).to_be_visible()
                await _assert_no_blocking_horizontal_overflow(page, viewport["width"])

                for test_id in surface["controls"]:
                    await _assert_control_usable(page, test_id, viewport["width"])

                main_box = await page.locator("main").bounding_box()
                assert main_box is not None
                assert main_box["x"] >= -1
                assert main_box["x"] + main_box["width"] <= viewport["width"] + 1

                await context.close()

        await browser.close()
