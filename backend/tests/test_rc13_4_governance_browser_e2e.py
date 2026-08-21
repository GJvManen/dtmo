from __future__ import annotations

import json
import os

import pytest
from playwright.async_api import Route, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC13.4 browser E2E executes only in the dedicated workflow",
)


@pytest.mark.asyncio
async def test_canonical_governance_shows_framework_coverage_and_real_mappings() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "admin-tester",
                "X-DTMO-Roles": "admin",
            }
        )
        page = await context.new_page()

        async def empty_list_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body="[]")

        async def dashboard_route(route: Route) -> None:
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(
                    {
                        "total_intelligence": 0,
                        "new_last_24h": 0,
                        "average_confidence": 0,
                        "severity": {},
                        "sources": {},
                        "connector_health": {},
                        "review_status": {},
                        "intelligence_trend_7d": {},
                    }
                ),
            )

        await page.route("**/api/v1/admin/rbac/roles", empty_list_route)
        await page.route("**/api/v1/admin/rbac/principals", empty_list_route)
        await page.route("**/api/v1/admin/sources/catalog", empty_list_route)
        await page.route("**/api/v1/source-center/status", empty_list_route)
        await page.route("**/api/v1/admin/sources", empty_list_route)
        await page.route("**/api/v1/console/recent-intelligence?*", empty_list_route)
        await page.route("**/api/v1/dashboards/summary", dashboard_route)

        external_requests: list[str] = []
        page.on(
            "request",
            lambda request: external_requests.append(request.url)
            if not request.url.startswith(BASE_URL)
            else None,
        )

        await page.goto(f"{BASE_URL}/")
        await page.get_by_role("button", name="Governance").click()

        panel = page.locator("#governance-knowledge")
        await expect(panel).to_be_visible()
        await expect(panel).to_contain_text("Frameworks, mappings & authority boundaries")

        normenkader = page.locator('[data-governance-framework="normenkader-ibp"]')
        await expect(normenkader).to_contain_text("Normenkader IBP")
        await expect(normenkader).to_contain_text("Expliciete partiële crosswalk")
        await expect(normenkader).to_contain_text("partiële crosswalk en geen certificering")
        await expect(normenkader).to_contain_text("ID.02")
        await expect(normenkader).to_contain_text("SM.07")

        attack = page.locator('[data-governance-framework="mitre-attack"]')
        await expect(attack).to_contain_text("MITRE ATT&CK")
        await expect(attack).to_contain_text("Expliciete contextrelaties")
        await expect(attack).to_contain_text("T1078")
        await expect(attack).to_contain_text("T1087")

        cvss = page.locator('[data-governance-framework="cvss"]')
        await expect(cvss).to_contain_text("CVSS")
        await expect(cvss).to_contain_text("Context-only")
        await expect(cvss).to_contain_text("scoring-context")

        internal = page.locator('[data-governance-framework="dtmo-governance"]')
        await expect(internal).to_contain_text("Repository-backed")
        await expect(page.locator('[data-governance-mapping="exact-head-evidence"]')).to_contain_text(
            "Exact-head release evidence"
        )
        await expect(page.locator("#governance-boundaries")).to_contain_text(
            "publication/share authority"
        )
        await expect(page.locator("#governance-status")).to_contain_text(
            "5 frameworks · 6 repository-backed mappings"
        )
        claim_boundary = page.locator("#governance-claim-boundary")
        await expect(claim_boundary).to_contain_text("only when explicitly defined")
        await expect(claim_boundary).to_contain_text("do not constitute certification")
        assert external_requests == []

        await context.close()
        await browser.close()
