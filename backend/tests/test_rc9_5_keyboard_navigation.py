from __future__ import annotations

import os

import pytest
from playwright.async_api import Page, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.5 keyboard E2E executes only in the dedicated browser workflow",
)


async def _assert_visible_focus(page: Page, test_id: str) -> None:
    locator = page.get_by_test_id(test_id)
    await expect(locator).to_be_focused()
    focus = await locator.evaluate(
        """element => {
          const style = getComputedStyle(element);
          return {
            outlineStyle: style.outlineStyle,
            outlineWidth: style.outlineWidth,
            boxShadow: style.boxShadow,
          };
        }"""
    )
    has_outline = focus["outlineStyle"] != "none" and focus["outlineWidth"] not in {"0", "0px"}
    has_shadow = focus["boxShadow"] not in {"none", ""}
    assert has_outline or has_shadow, f"{test_id} has no visible focus indicator: {focus}"


async def _tab_to(page: Page, test_id: str, *, limit: int = 12) -> None:
    for _ in range(limit):
        await page.keyboard.press("Tab")
        if await page.get_by_test_id(test_id).evaluate("el => el === document.activeElement"):
            await _assert_visible_focus(page, test_id)
            return
    raise AssertionError(f"keyboard focus never reached {test_id}")


@pytest.mark.asyncio
async def test_accepted_critical_journeys_are_keyboard_operable_with_visible_focus() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        share_context = await browser.new_context(
            extra_http_headers={"X-DTMO-Subject": "keyboard-admin", "X-DTMO-Roles": "admin"}
        )
        share_page = await share_context.new_page()
        share_calls: list[str] = []

        async def share_route(route):  # type: ignore[no-untyped-def]
            share_calls.append(route.request.url)
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=(
                    '{"id":"00000000-0000-0000-0000-000000000001",'
                    '"review_status":"reviewed","share_approved":false,'
                    '"audit_event_id":"00000000-0000-0000-0000-000000000002"}'
                ),
            )

        await share_page.route("**/api/v1/intelligence/**/review", share_route)
        await share_page.route("**/api/v1/intelligence/**/share-approval", share_route)
        await share_page.goto(f"{BASE_URL}/ui/share-approval")
        await expect(share_page.get_by_test_id("review-button")).to_be_visible()
        await _tab_to(share_page, "item-id")
        await share_page.keyboard.type("00000000-0000-0000-0000-000000000001")
        await _tab_to(share_page, "review-button")
        await share_page.keyboard.press("Enter")
        await expect(share_page.get_by_test_id("result")).to_contain_text('"status": 200')
        await _tab_to(share_page, "share-button")
        await share_page.keyboard.press("Space")
        await expect(share_page.get_by_test_id("result")).to_contain_text('"status": 200')
        assert len(share_calls) == 2
        await share_context.close()

        analyst_context = await browser.new_context(
            extra_http_headers={"X-DTMO-Subject": "keyboard-analyst", "X-DTMO-Roles": "analyst"}
        )
        analyst_page = await analyst_context.new_page()
        analyst_calls = 0

        async def analyst_route(route):  # type: ignore[no-untyped-def]
            nonlocal analyst_calls
            analyst_calls += 1
            await route.fulfill(
                status=200,
                content_type="application/json",
                body='{"query":"kev","count":0,"results":[]}',
            )

        await analyst_page.route("**/api/v1/intelligence/search?*", analyst_route)
        await analyst_page.goto(f"{BASE_URL}/ui/analyst-search")
        await expect(analyst_page.get_by_test_id("search-panel")).to_be_visible()
        await _tab_to(analyst_page, "search-query")
        await analyst_page.keyboard.type("kev")
        await _tab_to(analyst_page, "search-submit")
        await analyst_page.keyboard.press("Enter")
        await expect(analyst_page.get_by_test_id("search-status")).to_have_attribute("data-state", "empty")
        assert analyst_calls == 1
        await analyst_context.close()

        ciso_context = await browser.new_context(
            extra_http_headers={"X-DTMO-Subject": "keyboard-ciso", "X-DTMO-Roles": "ciso"}
        )
        ciso_page = await ciso_context.new_page()
        ciso_calls = 0

        async def ciso_route(route):  # type: ignore[no-untyped-def]
            nonlocal ciso_calls
            ciso_calls += 1
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=(
                    '{"jti":"keyboard-token","expires_at":"2030-01-01T00:00:00Z",'
                    '"audit_event_id":"00000000-0000-0000-0000-000000000003"}'
                ),
            )

        await ciso_page.route("**/api/v1/security/tokens/revoke", ciso_route)
        await ciso_page.goto(f"{BASE_URL}/ui/ciso-security")
        await expect(ciso_page.get_by_test_id("revocation-panel")).to_be_visible()
        await _tab_to(ciso_page, "token-jti")
        await ciso_page.keyboard.type("keyboard-token")
        await _tab_to(ciso_page, "token-expiry")
        await ciso_page.keyboard.type("2030-01-01T00:00:00Z")
        await _tab_to(ciso_page, "revocation-reason")
        await ciso_page.keyboard.type("Synthetic keyboard accessibility validation")
        await _tab_to(ciso_page, "revoke-submit")
        await ciso_page.keyboard.press("Enter")
        await expect(ciso_page.get_by_test_id("revocation-status")).to_have_attribute("data-state", "success")
        assert ciso_calls == 1
        await ciso_context.close()

        auditor_context = await browser.new_context(
            extra_http_headers={"X-DTMO-Subject": "keyboard-auditor", "X-DTMO-Roles": "auditor"}
        )
        auditor_page = await auditor_context.new_page()
        auditor_calls = 0

        async def auditor_route(route):  # type: ignore[no-untyped-def]
            nonlocal auditor_calls
            auditor_calls += 1
            await route.fulfill(
                status=200,
                content_type="application/json",
                body='{"count":0,"read_only":true,"events":[]}',
            )

        await auditor_page.route("**/api/v1/audit/events?*", auditor_route)
        await auditor_page.goto(f"{BASE_URL}/ui/auditor")
        await expect(auditor_page.get_by_test_id("audit-panel")).to_be_visible()
        await _tab_to(auditor_page, "load-audit")
        await auditor_page.keyboard.press("Space")
        await expect(auditor_page.get_by_test_id("audit-status")).to_have_attribute("data-state", "empty")
        assert auditor_calls == 1
        await auditor_context.close()

        await browser.close()
