from __future__ import annotations

import json
import os

import pytest
from playwright.async_api import Route, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(not E2E_ENABLED, reason="E8.9b browser E2E runs only in the dedicated workflow")


@pytest.mark.asyncio
async def test_ail_indicator_shows_misp_vulnerability_and_investigation_context_without_raw_content() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()

        async def search_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body=json.dumps({
                "query": "login.example", "count": 1, "results": [{
                    "id": "11111111-1111-4111-8111-111111111111",
                    "title": "AIL domain indicator", "summary": "AIL extracted domain indicator: login.example",
                    "source_id": "ail", "severity": "informational", "education_relevance": 80, "confidence_score": 75,
                }],
            }))

        async def detail_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body=json.dumps({
                "id": "11111111-1111-4111-8111-111111111111", "source_id": "ail", "external_id": "domain:None:login.example",
                "item_type": "indicator", "title": "AIL domain indicator", "summary": "AIL extracted domain indicator: login.example",
                "canonical_url": "https://ail.example.test/api/v1/object?gid=domain%3ANone%3Alogin.example",
                "severity": "informational", "confidence_score": 75, "confidence_level": "high", "education_relevance": 80,
                "review_status": "candidate", "share_approved": False, "tags": [], "context": {"cve_ids": [], "known_exploited": False, "vendor": None, "product": None},
                "metadata": {}, "provenance": [], "published_at": None, "discovered_at": "2026-08-14T20:00:00+00:00", "confidence_rationale": [],
            }))

        async def correlation_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body=json.dumps({
                "status": "ok", "indicator": {"type": "domain", "value": "login.example"},
                "investigation_references": [{"id": "case-42"}], "raw_content_exposed": False, "analysis_only": True,
                "degraded_reasons": [],
                "claim_boundary": "Exact correlation is analytical context only; it does not prove exposure, compromise, attribution or share authority.",
                "correlations": [
                    {"source_id": "misp", "external_id": "event-1", "item_type": "cti_event", "title": "MISP phishing event", "relation": "misp_object_attribute", "matched_value": "login.example", "context": {"object_name": "domain-ip", "type": "domain"}},
                    {"source_id": "opencve", "external_id": "CVE-2026-12345", "item_type": "vulnerability", "title": "Affected product", "relation": "canonical_exact_match", "matched_value": "login.example", "context": {"vendor": "Example", "product": "Portal"}},
                ],
            }))

        await page.route("**/api/v1/intelligence/search?*", search_route)
        await page.route("**/api/v1/intelligence/11111111-1111-4111-8111-111111111111/workspace", detail_route)
        await page.route("**/api/v1/intelligence/11111111-1111-4111-8111-111111111111/ail-correlations", correlation_route)

        await page.goto(f"{BASE_URL}/ui/intelligence-workspace")
        await page.locator("#query").fill("login.example")
        await page.get_by_role("button", name="Zoeken").click()
        await page.locator("[data-id]").click()

        panel = page.locator("#ail-correlation-panel")
        await expect(panel).to_be_visible()
        await expect(page.locator("#ail-correlation-status")).to_contain_text("2 correlaties")
        await expect(panel).to_contain_text("case-42")
        await expect(panel).to_contain_text("MISP phishing event")
        await expect(panel).to_contain_text("Affected product")
        await expect(panel).to_contain_text("does not prove exposure")
        await expect(panel).not_to_contain_text("raw paste")
        await expect(panel).not_to_contain_text("leak body")

        await browser.close()
