from __future__ import annotations

import os

import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason="Governance/Operations functional recovery runs only in the dedicated exact-head browser workflow",
)


@pytest.mark.asyncio
async def test_governance_and_operations_deep_same_origin_journeys() -> None:
    """Prove repository-backed governance evidence and read-only runtime observation in the canonical shell."""
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "functional-recovery-governance-operations",
                "X-DTMO-Roles": "admin",
            }
        )
        page = await context.new_page()

        await page.goto(f"{BASE_URL}/workbench/governance")
        await expect(page.get_by_role("heading", name="Governance & Evidence", exact=True)).to_be_visible()
        for framework in ("Normenkader IBP", "MITRE ATT&CK", "NIST Cybersecurity Framework", "CVSS"):
            await expect(page.get_by_text(framework, exact=True)).to_be_visible()
        await expect(page.get_by_text("Explicit coverage state", exact=True)).to_be_visible()
        await expect(page.get_by_text("Traceable controls", exact=True)).to_be_visible()
        await expect(page.get_by_role("heading", name="Separation of duties", exact=True)).to_be_visible()
        await expect(page.get_by_text("Evidence without synthetic assurance", exact=True)).to_be_visible()
        await expect(page.get_by_text("Mapping visibility ≠ compliance approval", exact=True)).to_be_visible()
        assert await page.locator('a[href^="/ui/"]').count() == 0

        governance = await page.request.get(f"{BASE_URL}/api/v1/governance/knowledge")
        assert governance.ok
        governance_body = await governance.json()
        assert governance_body["status"] == "repository_backed"
        assert {item["id"] for item in governance_body["frameworks"]} >= {
            "normenkader-ibp",
            "mitre-attack",
            "nist-csf",
            "cvss",
            "dtmo-governance",
        }
        assert len(governance_body["authority_boundaries"]) >= 6
        assert "production authorization" in governance_body["claim_boundary"]

        await page.goto(f"{BASE_URL}/workbench/operations")
        await expect(page.get_by_role("heading", name="Operations", exact=True)).to_be_visible()
        await expect(page.get_by_role("heading", name="Operational snapshot", exact=True)).to_be_visible()
        await expect(page.get_by_role("heading", name="Platform health", exact=True)).to_be_visible()
        await expect(page.get_by_role("heading", name="Alert state", exact=True)).to_be_visible()
        await expect(page.get_by_role("heading", name="Process workload", exact=True)).to_be_visible()
        await expect(page.get_by_text("Runtime observation ≠ production assurance", exact=True)).to_be_visible()
        await expect(page.get_by_text("Missing telemetry stays unavailable", exact=False)).to_be_visible()

        health = await page.request.get(f"{BASE_URL}/health")
        assert health.ok
        health_body = await health.json()
        assert health_body["status"] == "healthy"

        summary = await page.request.get(f"{BASE_URL}/api/v1/operations/summary")
        assert summary.ok
        summary_body = await summary.json()
        for key in (
            "request_count",
            "average_latency_ms",
            "active_alerts",
            "trace_context_total",
            "in_flight",
            "queue_backlog_ratio",
            "connector_runs_total",
            "alerts",
        ):
            assert key in summary_body
        assert set(summary_body["alerts"]) == {"api_error", "connector", "storage_integrity", "search_health"}

        await page.get_by_role("button", name="Refresh runtime observation", exact=True).click()
        await expect(page.get_by_text("Canonical pivots", exact=True)).to_be_visible()
        await expect(page.get_by_role("link", name="Sources & Collection", exact=False)).to_be_visible()
        await expect(page.get_by_role("link", name="Administration", exact=False)).to_be_visible()
        await expect(page.get_by_role("link", name="Automation", exact=False)).to_be_visible()
        assert await page.locator('a[href^="/ui/"]').count() == 0

        await context.close()
        await browser.close()
