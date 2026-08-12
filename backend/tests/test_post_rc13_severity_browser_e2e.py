from __future__ import annotations

import json
import os
from urllib.parse import parse_qs, urlparse

import pytest
from playwright.async_api import ConsoleMessage, Route, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
BROWSER_CHANNEL = os.environ.get("DTMO_BROWSER_CHANNEL", "chrome")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="Post-RC13 severity Chrome E2E executes only in the dedicated workflow",
)


def _record(severity: str, title: str) -> dict[str, object]:
    return {
        "id": f"{severity}-record",
        "source_id": "nvd-cve",
        "title": title,
        "summary": f"{severity} canonical intelligence",
        "severity": severity,
        "confidence_score": 90,
        "education_relevance": 80,
        "review_status": "pending",
        "share_approved": False,
        "canonical_url": f"https://example.invalid/{severity}",
        "published_at": "2026-08-12T12:00:00+00:00",
        "discovered_at": "2026-08-12T12:05:00+00:00",
    }


def _dashboard(severity: str | None) -> dict[str, object]:
    counts = {
        "informational": 1,
        "low": 1,
        "medium": 0,
        "high": 1,
        "critical": 1,
    }
    if severity is None:
        visible = {key: value for key, value in counts.items() if value > 0}
        total = sum(visible.values())
    else:
        value = counts.get(severity, 0)
        visible = {severity: value} if value else {}
        total = value
    return {
        "generated_at": "2026-08-12T12:30:00+00:00",
        "severity_filter": severity,
        "severity_values": ["informational", "low", "medium", "high", "critical"],
        "total_intelligence": total,
        "new_last_24h": total,
        "average_confidence": 90.0 if total else 0.0,
        "severity": visible,
        "review_status": {"pending": total} if total else {},
        "sources": {"nvd-cve": total} if total else {},
        "connector_health": {"healthy": 2},
        "connector_health_filter_scope": "operational-unfiltered",
        "intelligence_trend_7d": {
            "2026-08-06": 0,
            "2026-08-07": 0,
            "2026-08-08": 0,
            "2026-08-09": 0,
            "2026-08-10": 0,
            "2026-08-11": 0,
            "2026-08-12": total,
        },
        "publication_boundary": "human-review-and-separate-share-approval-required",
    }


@pytest.mark.asyncio
async def test_shared_severity_filtering_in_chrome() -> None:
    calls: list[tuple[str, str | None]] = []
    page_errors: list[str] = []
    console_errors: list[str] = []

    records = {
        "informational": _record("informational", "Informational item"),
        "low": _record("low", "Low item"),
        "high": _record("high", "High item"),
        "critical": _record("critical", "Critical item"),
    }

    catalog = [
        {
            "id": "nvd-cve",
            "name": "NIST NVD CVE API 2.0",
            "endpoint_url": "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=100",
            "reliability": "authoritative",
            "category": "vulnerabilities",
            "execution_profile": "nvd-cve-v2",
            "execution_status": "supported",
            "provenance_note": "severity E2E fixture",
            "recommended_interval_seconds": 7200,
            "secret_ref": None,
        }
    ]
    source_status = [
        {
            "id": "nvd-cve",
            "name": "NIST NVD CVE API 2.0",
            "category": "vulnerabilities",
            "source_type": "json-feed",
            "execution_profile": "nvd-cve-v2",
            "execution_status": "supported",
            "registered": True,
            "enabled": True,
            "interval_seconds": 7200,
            "reliability": "authoritative",
            "health_status": "healthy",
            "last_success_at": "2026-08-12T12:00:00+00:00",
            "last_failure_at": None,
            "consecutive_failures": 0,
            "isolated_until": None,
            "manual_run_available": True,
            "provenance": {"endpoint": catalog[0]["endpoint_url"]},
        }
    ]
    registered = [
        {
            "id": "nvd-cve",
            "name": "NIST NVD CVE API 2.0",
            "source_type": "json-feed",
            "endpoint_url": catalog[0]["endpoint_url"],
            "enabled": True,
            "interval_seconds": 7200,
            "reliability": "authoritative",
            "secret_ref": None,
            "created_by": "admin-tester",
            "updated_by": "admin-tester",
        }
    ]
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

        async def dashboard_route(route: Route) -> None:
            query = parse_qs(urlparse(route.request.url).query)
            severity = query.get("severity", [None])[0]
            calls.append(("dashboard", severity))
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(_dashboard(severity)),
            )

        async def recent_route(route: Route) -> None:
            query = parse_qs(urlparse(route.request.url).query)
            severity = query.get("severity", [None])[0]
            calls.append(("recent", severity))
            rows = list(records.values()) if severity is None else ([records[severity]] if severity in records else [])
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(rows),
            )

        async def search_route(route: Route) -> None:
            query = parse_qs(urlparse(route.request.url).query)
            severity = query.get("severity", [None])[0]
            calls.append(("search", severity))
            rows = list(records.values()) if severity is None else ([records[severity]] if severity in records else [])
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"query": query.get("q", [""])[0], "count": len(rows), "results": rows}),
            )

        await page.route("**/api/v1/dashboards/summary*", dashboard_route)
        await page.route("**/api/v1/console/recent-intelligence?*", recent_route)
        await page.route("**/api/v1/intelligence/search?*", search_route)
        await page.route(
            "**/api/v1/admin/sources/catalog",
            lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps(catalog)),
        )
        await page.route(
            "**/api/v1/source-center/status",
            lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps(source_status)),
        )
        await page.route(
            "**/api/v1/admin/sources",
            lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps(registered)),
        )
        await page.route(
            "**/api/v1/admin/rbac/roles",
            lambda route: route.fulfill(status=200, content_type="application/json", body="[]"),
        )
        await page.route(
            "**/api/v1/admin/rbac/principals",
            lambda route: route.fulfill(status=200, content_type="application/json", body="[]"),
        )
        await page.route(
            "**/api/v1/governance/knowledge",
            lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps(governance)),
        )

        await page.goto(f"{BASE_URL}/")
        await expect(page.locator("#overview-severity-filter")).to_have_value("all")
        await expect(page.locator("#intelligence-severity-filter")).to_have_value("all")
        await expect(page.get_by_test_id("global-status")).to_contain_text("Bijgewerkt")

        # High filters Overview KPI/graph and recent canonical intelligence through one value.
        await page.locator("#overview-severity-filter").select_option("high")
        await expect(page.locator("#intelligence-severity-filter")).to_have_value("high")
        await expect(page.locator("#kpi-intel")).to_have_text("1")
        await expect(page.locator("#overview-severity-chart .severity-high")).to_have_count(2)
        await expect(page.get_by_test_id("overview-recent")).to_contain_text("High item")
        await expect(page.get_by_test_id("overview-recent")).not_to_contain_text("Low item")
        await expect(page.get_by_test_id("overview-recent").locator(".severity-high")).to_contain_text("High")
        assert ("dashboard", "high") in calls
        assert ("recent", "high") in calls

        # The Intelligence view keeps the same filter and composes with the existing search API.
        await page.get_by_role("button", name="Intelligence", exact=True).click()
        await expect(page.locator("#intelligence-severity-filter")).to_have_value("high")
        await page.locator("#intel-query").fill("school")
        await page.locator("#intel-search").get_by_role("button", name="Zoeken").click()
        await expect(page.locator("#intel-results")).to_contain_text("High item")
        await expect(page.locator("#intel-results .severity-high")).to_contain_text("High")
        assert ("search", "high") in calls

        # A filtered zero-result state is explicit rather than reporting unrelated records.
        await page.locator("#intelligence-severity-filter").select_option("medium")
        await expect(page.locator("#overview-severity-filter")).to_have_value("medium")
        await expect(page.locator("#kpi-intel")).to_have_text("0")
        await expect(page.locator("#intel-recent-status")).to_contain_text(
            "Geen recente records met severity Medium"
        )
        await expect(page.locator("#intel-results .empty-state")).to_contain_text(
            "Geen zoekresultaten met severity Medium"
        )

        # Critical remains a distinct canonical severity; it is never collapsed into High.
        await page.locator("#intelligence-severity-filter").select_option("critical")
        await expect(page.locator("#kpi-intel")).to_have_text("1")
        await expect(page.get_by_test_id("overview-recent")).to_contain_text("Critical item")
        await expect(page.get_by_test_id("overview-recent").locator(".severity-critical")).to_contain_text(
            "Critical"
        )
        assert ("dashboard", "critical") in calls
        assert ("recent", "critical") in calls

        # Meaning is carried by visible text/classes as well as colour, with no browser errors.
        await expect(page.locator(".severity-legend")).to_contain_text("Informational")
        await expect(page.locator(".severity-legend")).to_contain_text("Low")
        await expect(page.locator(".severity-legend")).to_contain_text("Medium")
        await expect(page.locator(".severity-legend")).to_contain_text("High")
        await expect(page.locator(".severity-legend")).to_contain_text("Critical")
        assert page_errors == []
        assert console_errors == []

        await context.close()
        await browser.close()
