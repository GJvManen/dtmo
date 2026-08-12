from __future__ import annotations

import json
import os

import pytest
from playwright.async_api import ConsoleMessage, Route, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
BROWSER_CHANNEL = os.environ.get("DTMO_BROWSER_CHANNEL", "chrome")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC13 owner-retest Chrome E2E executes only in the dedicated workflow",
)


@pytest.mark.asyncio
async def test_owner_reported_console_usability_in_chrome() -> None:
    calls = {"dashboard": 0, "sources": 0, "recent": 0, "rbac": 0, "governance": 0}
    page_errors: list[str] = []
    console_errors: list[str] = []

    catalog = [
        {
            "id": "cisa-kev",
            "name": "CISA Known Exploited Vulnerabilities",
            "endpoint_url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
            "reliability": "authoritative",
            "category": "exploited-vulnerabilities",
            "execution_profile": "built-in-cisa-kev",
            "execution_status": "supported-built-in",
            "provenance_note": "owner-retest Chrome fixture",
            "recommended_interval_seconds": 3600,
            "secret_ref": None,
        }
    ]
    source_status = [
        {
            "id": "cisa-kev",
            "name": "CISA Known Exploited Vulnerabilities",
            "category": "exploited-vulnerabilities",
            "source_type": "cisa-kev",
            "execution_profile": "built-in-cisa-kev",
            "execution_status": "supported-built-in",
            "registered": True,
            "enabled": False,
            "interval_seconds": 3600,
            "reliability": "authoritative",
            "health_status": "unknown",
            "last_success_at": None,
            "last_failure_at": None,
            "consecutive_failures": 0,
            "isolated_until": None,
            "manual_run_available": True,
            "provenance": {"endpoint": catalog[0]["endpoint_url"]},
        }
    ]
    zero_dashboard = {
        "generated_at": "2026-08-12T06:30:00+00:00",
        "total_intelligence": 0,
        "new_last_24h": 0,
        "average_confidence": 0.0,
        "severity": {},
        "review_status": {},
        "sources": {},
        "connector_health": {},
        "intelligence_trend_7d": {
            "2026-08-06": 0,
            "2026-08-07": 0,
            "2026-08-08": 0,
            "2026-08-09": 0,
            "2026-08-10": 0,
            "2026-08-11": 0,
            "2026-08-12": 0,
        },
        "publication_boundary": "human-review-and-separate-share-approval-required",
    }
    governance = {
        "frameworks": [],
        "mappings": [],
        "authority_boundaries": ["Technical access never grants publication/share authority."],
        "claim_boundary": "No inferred mappings.",
    }

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(channel=BROWSER_CHANNEL)
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "admin-tester",
                "X-DTMO-Roles": "admin",
            }
        )
        page = await context.new_page()
        page.on("pageerror", lambda error: page_errors.append(str(error)))

        def capture_console(message: ConsoleMessage) -> None:
            if message.type == "error":
                console_errors.append(message.text)

        page.on("console", capture_console)

        async def catalog_route(route: Route) -> None:
            calls["sources"] += 1
            await route.fulfill(status=200, content_type="application/json", body=json.dumps(catalog))

        async def status_route(route: Route) -> None:
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(source_status),
            )

        async def registered_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body="[]")

        async def recent_route(route: Route) -> None:
            calls["recent"] += 1
            await route.fulfill(status=200, content_type="application/json", body="[]")

        async def dashboard_route(route: Route) -> None:
            calls["dashboard"] += 1
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(zero_dashboard),
            )

        async def roles_route(route: Route) -> None:
            calls["rbac"] += 1
            await route.fulfill(status=200, content_type="application/json", body="[]")

        async def principals_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body="[]")

        async def governance_route(route: Route) -> None:
            calls["governance"] += 1
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(governance),
            )

        await page.route("**/api/v1/admin/sources/catalog", catalog_route)
        await page.route("**/api/v1/source-center/status", status_route)
        await page.route("**/api/v1/admin/sources", registered_route)
        await page.route("**/api/v1/console/recent-intelligence?*", recent_route)
        await page.route("**/api/v1/dashboards/summary", dashboard_route)
        await page.route("**/api/v1/admin/rbac/roles", roles_route)
        await page.route("**/api/v1/admin/rbac/principals", principals_route)
        await page.route("**/api/v1/governance/knowledge", governance_route)

        await page.goto(f"{BASE_URL}/")
        await expect(page.get_by_test_id("global-status")).to_have_text(
            "Geen intelligence data · bronstatus geladen"
        )

        # Empty datasets must be explicit empty states, not zero-height pseudo-graphs.
        await expect(page.locator("#overview-trend-chart")).to_contain_text(
            "Geen data om te visualiseren"
        )
        await expect(page.locator("#overview-severity-chart")).to_contain_text(
            "Geen data om te visualiseren"
        )
        await expect(page.locator("#overview-trend-chart .bar")).to_have_count(0)
        await expect(page.locator("#overview-severity-chart .bar")).to_have_count(0)
        await expect(page.get_by_test_id("overview-recent")).to_contain_text(
            "Nog geen intelligence ingested"
        )

        # The product navigation must not expose a release badge.
        await expect(page.locator("aside.side")).not_to_contain_text("16.0.0rc12")

        # The owner-reported refresh control must perform a real second refresh and recover its UI state.
        initial_dashboard_calls = calls["dashboard"]
        initial_source_calls = calls["sources"]
        initial_recent_calls = calls["recent"]
        refresh = page.get_by_role("button", name="Alles vernieuwen")
        await refresh.click()
        await expect(refresh).to_be_enabled()
        await expect(refresh).to_have_text("Alles vernieuwen")
        await expect(page.get_by_test_id("global-status")).to_have_text(
            "Geen intelligence data · bronstatus geladen"
        )
        assert calls["dashboard"] > initial_dashboard_calls
        assert calls["sources"] > initial_source_calls
        assert calls["recent"] > initial_recent_calls

        # Exercise the canonical navigation and the non-mutating controls in the Chrome channel.
        journeys = (
            ("Intelligence", "intelligence"),
            ("Bronnen & catalogus", "sources"),
            ("Visual analytics", "analytics"),
            ("Administration", "administration"),
            ("Governance", "governance"),
            ("Overzicht", "overview"),
        )
        for label, panel in journeys:
            await page.get_by_role("button", name=label, exact=True).click()
            await expect(page.locator(f'[data-view-panel="{panel}"]')).to_be_visible()

        await page.get_by_role("button", name="Intelligence", exact=True).click()
        await page.get_by_role("button", name="Recente intelligence vernieuwen").click()
        await expect(page.locator("#intel-recent-status")).to_contain_text(
            "Nog geen canonical intelligence beschikbaar"
        )

        await page.get_by_role("button", name="Bronnen & catalogus").click()
        await page.get_by_role("button", name="Vernieuwen", exact=True).click()
        await expect(page.get_by_test_id("source-status")).to_contain_text("1 catalogusbronnen")

        await page.get_by_role("button", name="Administration", exact=True).click()
        await expect(page.locator('[data-view-panel="administration"]')).to_contain_text(
            "Beheer governed gebruikers en rollen vanuit één centrale werkruimte"
        )
        await expect(page.locator("#rbac-administration")).to_be_visible()
        await page.locator("#rbac-refresh").click()
        await expect(page.locator("#rbac-status")).to_contain_text("0 managed principals")
        await expect(page.locator("#dev-identity-context")).not_to_have_attribute("open", "")

        await page.get_by_role("button", name="Governance", exact=True).click()
        await page.locator("#governance-refresh").click()
        await expect(page.locator("#governance-status")).to_contain_text("0 frameworks")

        assert calls["rbac"] >= 2
        assert calls["governance"] >= 2
        assert page_errors == []
        assert console_errors == []

        await context.close()
        await browser.close()
