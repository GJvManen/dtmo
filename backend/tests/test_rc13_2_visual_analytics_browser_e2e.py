from __future__ import annotations

import json
import os

import pytest
from playwright.async_api import Route, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC13.2 browser E2E executes only in the dedicated workflow",
)


@pytest.mark.asyncio
async def test_visual_analytics_are_single_session_and_do_not_request_grafana() -> None:
    grafana_requests: list[str] = []

    dashboard = {
        "generated_at": "2026-08-11T16:00:00+00:00",
        "total_intelligence": 7,
        "new_last_24h": 3,
        "average_confidence": 88.0,
        "severity": {"critical": 2, "high": 3, "medium": 2},
        "review_status": {"candidate": 4, "reviewed": 3},
        "sources": {"cisa-kev": 4, "nvd-cve": 3},
        "connector_health": {"healthy": 2},
        "intelligence_trend_7d": {
            "2026-08-05": 0,
            "2026-08-06": 1,
            "2026-08-07": 0,
            "2026-08-08": 1,
            "2026-08-09": 1,
            "2026-08-10": 1,
            "2026-08-11": 3,
        },
    }

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "analyst-tester",
                "X-DTMO-Roles": "analyst",
            }
        )
        page = await context.new_page()
        page.on(
            "request",
            lambda request: grafana_requests.append(request.url)
            if "/grafana/" in request.url
            else None,
        )

        async def json_response(route: Route, body: object) -> None:
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(body),
            )

        async def dashboard_route(route: Route) -> None:
            await json_response(route, dashboard)

        async def catalog_route(route: Route) -> None:
            await json_response(route, [])

        async def source_status_route(route: Route) -> None:
            await json_response(route, [])

        async def registered_sources_route(route: Route) -> None:
            await json_response(route, [])

        async def recent_route(route: Route) -> None:
            await json_response(route, [])

        await page.route("**/api/v1/dashboards/summary", dashboard_route)
        await page.route("**/api/v1/admin/sources/catalog", catalog_route)
        await page.route("**/api/v1/source-center/status", source_status_route)
        await page.route("**/api/v1/admin/sources", registered_sources_route)
        await page.route("**/api/v1/console/recent-intelligence?*", recent_route)

        await page.goto(f"{BASE_URL}/")
        await page.get_by_role("button", name="Visual analytics").click()

        await expect(page.locator("#severity-chart")).to_be_visible()
        await expect(page.locator("#source-chart")).to_be_visible()
        await expect(page.locator("#connector-chart")).to_be_visible()
        await expect(page.locator("#review-chart")).to_be_visible()
        await expect(page.locator("#severity-table")).to_contain_text("critical")
        await expect(page.locator("#source-table")).to_contain_text("cisa-kev")
        await expect(page.locator("#review-table")).to_contain_text("reviewed")

        grafana_shell = page.locator(".grafana-shell")
        await expect(grafana_shell).to_be_hidden()
        await expect(
            page.get_by_role("button", name="Open Operations in Grafana")
        ).to_be_hidden()
        await expect(
            page.get_by_role("button", name="Open Intelligence in Grafana")
        ).to_be_hidden()

        await page.wait_for_timeout(250)
        assert grafana_requests == []

        await context.close()
        await browser.close()
