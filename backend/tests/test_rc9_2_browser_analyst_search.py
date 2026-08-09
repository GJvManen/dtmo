from __future__ import annotations

import asyncio
import os

import pytest
from playwright.async_api import Route, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9 browser E2E executes only in a dedicated browser workflow",
)


@pytest.mark.asyncio
async def test_analyst_search_exposes_loading_empty_success_and_backend_error_states() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "alice-analyst",
                "X-DTMO-Roles": "analyst",
            }
        )
        page = await context.new_page()
        await page.goto(f"{BASE_URL}/ui/analyst-search")

        await expect(page.get_by_test_id("analyst-principal")).to_contain_text("alice-analyst")
        await expect(page.get_by_test_id("search-panel")).to_be_visible()

        async def controlled_search(route: Route) -> None:
            url = route.request.url
            if "q=empty" in url:
                await asyncio.sleep(0.35)
                await route.fulfill(
                    status=200,
                    content_type="application/json",
                    body='{"query":"empty","count":0,"results":[]}',
                )
                return
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=(
                    '{"query":"school","count":1,"results":['
                    '{"title":"Synthetic education advisory",'
                    '"summary":"Browser-only RC9.2 fixture"}]}'
                ),
            )

        await page.route("**/api/v1/intelligence/search?*", controlled_search)

        await page.get_by_test_id("search-query").fill("empty")
        await page.get_by_test_id("search-submit").click()
        await expect(page.get_by_test_id("search-status")).to_have_attribute("data-state", "loading")
        await expect(page.get_by_test_id("search-status")).to_have_attribute("data-state", "empty")
        await expect(page.get_by_test_id("search-results").locator("li")).to_have_count(0)

        await page.get_by_test_id("search-query").fill("school")
        await page.get_by_test_id("search-submit").click()
        await expect(page.get_by_test_id("search-status")).to_have_attribute("data-state", "success")
        await expect(page.get_by_test_id("search-results")).to_contain_text(
            "Synthetic education advisory"
        )

        await page.unroute("**/api/v1/intelligence/search?*")
        await page.get_by_test_id("search-query").fill("error")
        await page.get_by_test_id("search-submit").click()
        await expect(page.get_by_test_id("search-status")).to_have_attribute("data-state", "error")
        await expect(page.get_by_test_id("search-status")).to_contain_text(
            "search backend unavailable"
        )

        await context.close()
        await browser.close()
