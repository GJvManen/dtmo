from __future__ import annotations

import json
import os

import pytest
from playwright.async_api import Route, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC13 browser E2E executes only in the dedicated workflow",
)


@pytest.mark.asyncio
async def test_source_register_enable_run_updates_intelligence_and_overview() -> None:
    state = {"registered": False, "enabled": False, "ingested": False}

    catalog = [
        {
            "id": "cisa-kev",
            "name": "CISA Known Exploited Vulnerabilities",
            "endpoint_url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
            "reliability": "authoritative",
            "category": "exploited-vulnerabilities",
            "execution_profile": "built-in-cisa-kev",
            "execution_status": "supported-built-in",
            "provenance_note": "fixture",
            "recommended_interval_seconds": 3600,
            "secret_ref": None,
        },
        {
            "id": "nvd-cve",
            "name": "NIST NVD CVE API 2.0",
            "endpoint_url": "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=100",
            "reliability": "authoritative",
            "category": "vulnerabilities",
            "execution_profile": "nvd-cve-v2",
            "execution_status": "supported",
            "provenance_note": "fixture",
            "recommended_interval_seconds": 7200,
            "secret_ref": None,
        },
        {
            "id": "enisa-threat-landscape",
            "name": "ENISA Threat Landscape",
            "endpoint_url": "https://www.enisa.europa.eu/topics/cyber-threats/threats-and-trends",
            "reliability": "authoritative",
            "category": "strategic-threat-intelligence",
            "execution_profile": "research-publication",
            "execution_status": "research-reference",
            "provenance_note": "fixture",
            "recommended_interval_seconds": 86400,
            "secret_ref": None,
        },
    ]

    def registered_sources() -> list[dict[str, object]]:
        if not state["registered"]:
            return []
        return [
            {
                "id": "nvd-cve",
                "name": "NIST NVD CVE API 2.0",
                "source_type": "json-feed",
                "endpoint_url": catalog[1]["endpoint_url"],
                "enabled": state["enabled"],
                "interval_seconds": 7200,
                "reliability": "authoritative",
                "secret_ref": None,
                "created_by": "admin-tester",
                "updated_by": "admin-tester",
            }
        ]

    def source_status() -> list[dict[str, object]]:
        return [
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
                "health_status": "healthy" if state["ingested"] else "unknown",
                "last_success_at": "2026-08-11T14:00:00+00:00" if state["ingested"] else None,
                "last_failure_at": None,
                "consecutive_failures": 0,
                "isolated_until": None,
                "manual_run_available": True,
                "provenance": {"endpoint": catalog[0]["endpoint_url"]},
            },
            {
                "id": "nvd-cve",
                "name": "NIST NVD CVE API 2.0",
                "category": "vulnerabilities",
                "source_type": "json-feed",
                "execution_profile": "nvd-cve-v2",
                "execution_status": "supported",
                "registered": state["registered"],
                "enabled": state["enabled"],
                "interval_seconds": 7200,
                "reliability": "authoritative",
                "health_status": "healthy" if state["ingested"] else "unknown",
                "last_success_at": "2026-08-11T14:01:00+00:00" if state["ingested"] else None,
                "last_failure_at": None,
                "consecutive_failures": 0,
                "isolated_until": None,
                "manual_run_available": state["registered"] and state["enabled"],
                "provenance": {"endpoint": catalog[1]["endpoint_url"]},
            },
        ]

    def recent_items() -> list[dict[str, object]]:
        if not state["ingested"]:
            return []
        return [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "source_id": "nvd-cve",
                "title": "Synthetic NVD advisory",
                "summary": "Inserted by the RC13.1 browser fixture",
                "severity": "high",
                "confidence_score": 90,
                "education_relevance": 85,
                "review_status": "candidate",
                "share_approved": False,
                "canonical_url": "https://example.invalid/CVE-TEST",
                "published_at": None,
                "discovered_at": "2026-08-11T14:01:00+00:00",
            }
        ]

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "admin-tester",
                "X-DTMO-Roles": "admin",
            }
        )
        page = await context.new_page()

        async def catalog_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body=json.dumps(catalog))

        async def status_route(route: Route) -> None:
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(source_status()),
            )

        async def registered_route(route: Route) -> None:
            if route.request.method == "GET":
                await route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(registered_sources()),
                )
                return
            await route.fallback()

        async def bootstrap_route(route: Route) -> None:
            state["registered"] = True
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(registered_sources()),
            )

        async def nvd_route(route: Route) -> None:
            if route.request.method == "PATCH":
                payload = json.loads(route.request.post_data or "{}")
                state["enabled"] = bool(payload.get("enabled"))
                await route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(registered_sources()[0]),
                )
                return
            await route.fallback()

        async def nvd_run_route(route: Route) -> None:
            state["ingested"] = True
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(
                    {
                        "id": "nvd-cve",
                        "status": "completed",
                        "records": 1,
                        "inserted": 1,
                        "indexed": 1,
                        "error": None,
                        "publication_gate": "human-review-and-separate-share-approval-required",
                    }
                ),
            )

        async def recent_route(route: Route) -> None:
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(recent_items()),
            )

        async def dashboard_route(route: Route) -> None:
            total = 1 if state["ingested"] else 0
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(
                    {
                        "generated_at": "2026-08-11T14:01:00+00:00",
                        "total_intelligence": total,
                        "new_last_24h": total,
                        "average_confidence": 90.0 if total else 0.0,
                        "severity": {"high": total} if total else {},
                        "review_status": {"candidate": total} if total else {},
                        "sources": {"nvd-cve": total} if total else {},
                        "connector_health": {"healthy": 1} if total else {"unknown": 2},
                        "intelligence_trend_7d": {
                            "2026-08-05": 0,
                            "2026-08-06": 0,
                            "2026-08-07": 0,
                            "2026-08-08": 0,
                            "2026-08-09": 0,
                            "2026-08-10": 0,
                            "2026-08-11": total,
                        },
                    }
                ),
            )

        await page.route("**/api/v1/admin/sources/catalog", catalog_route)
        await page.route("**/api/v1/source-center/status", status_route)
        await page.route("**/api/v1/admin/sources", registered_route)
        await page.route("**/api/v1/admin/sources/catalog/bootstrap", bootstrap_route)
        await page.route("**/api/v1/admin/sources/nvd-cve", nvd_route)
        await page.route("**/api/v1/admin/sources/nvd-cve/run", nvd_run_route)
        await page.route("**/api/v1/console/recent-intelligence?*", recent_route)
        await page.route("**/api/v1/dashboards/summary", dashboard_route)

        await page.goto(f"{BASE_URL}/")

        await expect(page.locator("body")).not_to_contain_text(
            "Legacy `/ui/*`-views blijven alleen compatibiliteitspaden"
        )
        await expect(page.locator("#overview-trend-chart")).to_be_visible()
        await expect(page.get_by_test_id("overview-recent")).to_contain_text(
            "Nog geen intelligence ingested"
        )

        await page.get_by_role("button", name="Bronnen & catalogus").click()
        cisa = page.locator('[data-source-card="cisa-kev"]')
        nvd = page.locator('[data-source-card="nvd-cve"]')
        await expect(cisa).to_contain_text("Built-in · handmatige run beschikbaar")
        await expect(cisa.get_by_role("button", name="Feed nu laden")).to_be_visible()
        await expect(nvd).to_contain_text("Nog niet geregistreerd")

        await page.get_by_role("button", name="Frameworkbronnen registreren").click()
        await expect(nvd.get_by_text("Geregistreerd · uitgeschakeld")).to_be_visible()

        await nvd.locator('input[data-enabled="nvd-cve"]').check()
        await nvd.get_by_role("button", name="Opslaan").click()
        await expect(nvd.get_by_text("Operationeel")).to_be_visible()
        await expect(nvd.get_by_role("button", name="Feed nu laden")).to_be_visible()

        await nvd.get_by_role("button", name="Feed nu laden").click()
        await expect(nvd.locator('[data-result="nvd-cve"]')).to_contain_text(
            "completed: 1 records, 1 inserted, 1 indexed"
        )

        await page.get_by_role("button", name="Intelligence", exact=True).click()
        await expect(page.get_by_test_id("intel-recent")).to_contain_text("Synthetic NVD advisory")

        await page.get_by_role("button", name="Overzicht").click()
        await expect(page.locator("#kpi-intel")).to_have_text("1")
        await expect(page.get_by_test_id("overview-recent")).to_contain_text("Synthetic NVD advisory")

        await context.close()
        await browser.close()
