from __future__ import annotations

import json
import os

import pytest
from playwright.async_api import Route, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))
ITEM_ID = "11111111-1111-4111-8111-111111111111"

pytestmark = pytest.mark.skipif(not E2E_ENABLED, reason="canonical AIL browser E2E runs only in the dedicated workflow")


@pytest.mark.asyncio
async def test_canonical_ioc_explorer_exposes_read_only_ail_correlation_context() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()

        async def inventory_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body=json.dumps({
                "records": [{
                    "record_id": "ioc-docs-1", "item_id": ITEM_ID, "item_title": "AIL domain indicator",
                    "source_id": "ail", "severity": "informational", "confidence_score": 75,
                    "observable_type": "domain", "observable_value": "login.example", "handling": "TLP:AMBER",
                    "status": "persisted", "analyzers": ["ail"], "created_at": "2026-08-27T12:00:00+00:00",
                    "external_share_authorized": False, "local_compromise_proven": False,
                }],
                "evidence_boundary": "Persisted IOC evidence only; no verdict or sharing authority is inferred.",
            }))

        async def correlation_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body=json.dumps({
                "status": "ok", "indicator": {"type": "domain", "value": "login.example"},
                "investigation_references": [{"id": "case-42"}], "raw_content_exposed": False, "analysis_only": True,
                "degraded_reasons": [],
                "claim_boundary": "Exact correlation is analytical context only; it does not prove exposure, compromise, attribution or share authority.",
                "correlations": [
                    {"source_id": "misp", "external_id": "event-1", "item_type": "cti_event", "title": "MISP phishing event", "relation": "misp_object_attribute", "matched_value": "login.example", "context": {}},
                    {"source_id": "opencve", "external_id": "CVE-2026-12345", "item_type": "vulnerability", "title": "Affected product context", "relation": "canonical_exact_match", "matched_value": "login.example", "context": {}},
                ],
            }))

        await page.route("**/api/v1/iocs?*", inventory_route)
        await page.route(f"**/api/v1/intelligence/{ITEM_ID}/ail-correlations", correlation_route)
        await page.goto(f"{BASE_URL}/workbench/intelligence/iocs", wait_until="networkidle")

        await expect(page.get_by_role("heading", name="IOC Explorer")).to_be_visible()
        await expect(page.get_by_text("login.example", exact=True)).to_be_visible()
        await page.get_by_role("button", name="Inspect AIL correlation").click()

        panel = page.get_by_role("article", name="AIL correlation context")
        await expect(panel).to_be_visible()
        await expect(panel).to_contain_text("MISP phishing event")
        await expect(panel).to_contain_text("Affected product context")
        await expect(panel).to_contain_text("case-42")
        await expect(panel).to_contain_text("Raw content exposed")
        await expect(panel).to_contain_text("no")
        await expect(panel).to_contain_text("does not prove exposure")
        await expect(panel).to_contain_text("never exposes the AIL API key")
        await expect(panel).not_to_contain_text("raw paste")
        await expect(panel).not_to_contain_text("leak body")

        await browser.close()
