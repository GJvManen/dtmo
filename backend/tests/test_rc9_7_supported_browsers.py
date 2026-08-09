from __future__ import annotations

import os

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))
BROWSERS = ("chromium", "firefox", "webkit")

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.7 supported-browser E2E executes only in the dedicated browser workflow",
)


@pytest.mark.asyncio
@pytest.mark.parametrize("browser_name", BROWSERS)
async def test_accepted_critical_journeys_are_consistent_across_supported_browsers(browser_name: str) -> None:
    async with async_playwright() as playwright:
        browser_type = getattr(playwright, browser_name)
        browser = await browser_type.launch()

        share_context = await browser.new_context(
            extra_http_headers={"X-DTMO-Subject": f"{browser_name}-admin", "X-DTMO-Roles": "admin"}
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
        response = await share_page.goto(f"{BASE_URL}/ui/share-approval")
        assert response is not None and response.ok
        await expect(share_page.get_by_test_id("review-button")).to_be_visible()
        await share_page.get_by_test_id("item-id").fill("00000000-0000-0000-0000-000000000001")
        await share_page.get_by_test_id("review-button").click()
        await expect(share_page.get_by_test_id("result")).to_contain_text('"status": 200')
        await share_page.get_by_test_id("share-button").click()
        await expect(share_page.get_by_test_id("result")).to_contain_text('"status": 200')
        assert len(share_calls) == 2
        await share_context.close()

        analyst_context = await browser.new_context(
            extra_http_headers={"X-DTMO-Subject": f"{browser_name}-analyst", "X-DTMO-Roles": "analyst"}
        )
        analyst_page = await analyst_context.new_page()
        analyst_calls = 0

        async def analyst_route(route):  # type: ignore[no-untyped-def]
            nonlocal analyst_calls
            analyst_calls += 1
            await route.fulfill(status=200, content_type="application/json", body='{"query":"kev","count":0,"results":[]}')

        await analyst_page.route("**/api/v1/intelligence/search?*", analyst_route)
        response = await analyst_page.goto(f"{BASE_URL}/ui/analyst-search")
        assert response is not None and response.ok
        await expect(analyst_page.get_by_test_id("search-panel")).to_be_visible()
        await analyst_page.get_by_test_id("search-query").fill("kev")
        await analyst_page.get_by_test_id("search-submit").click()
        await expect(analyst_page.get_by_test_id("search-status")).to_have_attribute("data-state", "empty")
        assert analyst_calls == 1
        await analyst_context.close()

        ciso_context = await browser.new_context(
            extra_http_headers={"X-DTMO-Subject": f"{browser_name}-ciso", "X-DTMO-Roles": "ciso"}
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
                    f'{{"jti":"{browser_name}-token","expires_at":"2030-01-01T00:00:00Z",'
                    '"audit_event_id":"00000000-0000-0000-0000-000000000003"}'
                ),
            )

        await ciso_page.route("**/api/v1/security/tokens/revoke", ciso_route)
        response = await ciso_page.goto(f"{BASE_URL}/ui/ciso-security")
        assert response is not None and response.ok
        await expect(ciso_page.get_by_test_id("revocation-panel")).to_be_visible()
        await ciso_page.get_by_test_id("token-jti").fill(f"{browser_name}-token")
        await ciso_page.get_by_test_id("token-expiry").fill("2030-01-01T00:00:00Z")
        await ciso_page.get_by_test_id("revocation-reason").fill("Synthetic supported-browser validation")
        await ciso_page.get_by_test_id("revoke-submit").click()
        await expect(ciso_page.get_by_test_id("revocation-status")).to_have_attribute("data-state", "success")
        assert ciso_calls == 1
        await ciso_context.close()

        auditor_context = await browser.new_context(
            extra_http_headers={"X-DTMO-Subject": f"{browser_name}-auditor", "X-DTMO-Roles": "auditor"}
        )
        auditor_page = await auditor_context.new_page()
        auditor_calls = 0

        async def auditor_route(route):  # type: ignore[no-untyped-def]
            nonlocal auditor_calls
            auditor_calls += 1
            await route.fulfill(status=200, content_type="application/json", body='{"count":0,"read_only":true,"events":[]}')

        await auditor_page.route("**/api/v1/audit/events?*", auditor_route)
        response = await auditor_page.goto(f"{BASE_URL}/ui/auditor")
        assert response is not None and response.ok
        await expect(auditor_page.get_by_test_id("audit-panel")).to_be_visible()
        await auditor_page.get_by_test_id("load-audit").click()
        await expect(auditor_page.get_by_test_id("audit-status")).to_have_attribute("data-state", "empty")
        assert auditor_calls == 1
        await auditor_context.close()

        await browser.close()
