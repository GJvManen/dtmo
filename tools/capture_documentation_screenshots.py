from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}


def dashboard_fixture() -> dict[str, object]:
    return {
        "generated_at": "2026-08-15T10:00:00+00:00",
        "total_intelligence": 24,
        "new_last_24h": 7,
        "average_confidence": 87.4,
        "severity": {"high": 5, "medium": 10, "low": 7, "informational": 2},
        "review_status": {"candidate": 11, "reviewed": 9, "published": 4},
        "sources": {"opencve": 8, "cisa-kev": 6, "nvd-cve": 5, "ail": 3, "misp": 2},
        "connector_health": {"healthy": 5, "degraded": 1},
        "intelligence_trend_7d": {
            "2026-08-09": 2,
            "2026-08-10": 3,
            "2026-08-11": 2,
            "2026-08-12": 4,
            "2026-08-13": 3,
            "2026-08-14": 3,
            "2026-08-15": 7,
        },
    }


def recent_intelligence_fixture() -> list[dict[str, object]]:
    return [
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "source_id": "opencve",
            "title": "Governed vulnerability intelligence example",
            "summary": "Sanitized documentation fixture with preserved provenance.",
            "severity": "high",
            "confidence_score": 94,
            "education_relevance": 91,
            "review_status": "candidate",
            "share_approved": False,
            "canonical_url": "https://example.invalid/CVE-2026-DOCS",
            "published_at": None,
            "discovered_at": "2026-08-15T09:30:00+00:00",
        },
        {
            "id": "22222222-2222-2222-2222-222222222222",
            "source_id": "ail",
            "title": "Correlated threat-intelligence observation",
            "summary": "Synthetic AIL correlation example for documentation rendering.",
            "severity": "medium",
            "confidence_score": 82,
            "education_relevance": 78,
            "review_status": "reviewed",
            "share_approved": False,
            "canonical_url": "https://example.invalid/AIL-DOCS",
            "published_at": None,
            "discovered_at": "2026-08-15T08:45:00+00:00",
        },
    ]


def source_catalog_fixture() -> list[dict[str, object]]:
    return [
        {
            "id": "cisa-kev",
            "name": "CISA Known Exploited Vulnerabilities",
            "endpoint_url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
            "reliability": "authoritative",
            "category": "exploited-vulnerabilities",
            "execution_profile": "built-in-cisa-kev",
            "execution_status": "supported-built-in",
            "provenance_note": "Documentation fixture — no live retrieval performed",
            "recommended_interval_seconds": 3600,
            "secret_ref": None,
        },
        {
            "id": "nvd-cve",
            "name": "NIST NVD CVE API 2.0",
            "endpoint_url": "https://services.nvd.nist.gov/rest/json/cves/2.0",
            "reliability": "authoritative",
            "category": "vulnerabilities",
            "execution_profile": "nvd-cve-v2",
            "execution_status": "supported",
            "provenance_note": "Documentation fixture — no live retrieval performed",
            "recommended_interval_seconds": 7200,
            "secret_ref": None,
        },
    ]


def source_status_fixture() -> list[dict[str, object]]:
    return [
        {
            "id": "cisa-kev",
            "name": "CISA Known Exploited Vulnerabilities",
            "category": "exploited-vulnerabilities",
            "source_type": "cisa-kev",
            "execution_profile": "built-in-cisa-kev",
            "execution_status": "supported-built-in",
            "registered": True,
            "enabled": True,
            "interval_seconds": 3600,
            "reliability": "authoritative",
            "health_status": "healthy",
            "last_success_at": "2026-08-15T09:15:00+00:00",
            "last_failure_at": None,
            "consecutive_failures": 0,
            "isolated_until": None,
            "manual_run_available": True,
            "provenance": {"endpoint": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"},
        },
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
            "last_success_at": "2026-08-15T09:05:00+00:00",
            "last_failure_at": None,
            "consecutive_failures": 0,
            "isolated_until": None,
            "manual_run_available": True,
            "provenance": {"endpoint": "https://services.nvd.nist.gov/rest/json/cves/2.0"},
        },
    ]


def vulnerability_fixture() -> dict[str, object]:
    return {
        "status": "ok",
        "degraded_reasons": [],
        "filters": {"window": "30d"},
        "summary": {
            "total": 12,
            "kev": 4,
            "with_sightings": 6,
            "average_cvss": 8.1,
            "average_epss": 0.64,
        },
        "facets": {
            "vendors": {"Example Vendor": 5, "Education Platform": 4, "Network Vendor": 3},
            "products": {"Gateway": 4, "Collaboration Suite": 4, "Edge Appliance": 4},
            "cwes": {"CWE-78": 4, "CWE-79": 3, "CWE-89": 2},
            "sighting_types": {"exploitation": 4, "reported": 2},
        },
        "trend": [
            {"date": "2026-08-11", "count": 1},
            {"date": "2026-08-12", "count": 2},
            {"date": "2026-08-13", "count": 2},
            {"date": "2026-08-14", "count": 3},
            {"date": "2026-08-15", "count": 4},
        ],
        "items": [
            {
                "cve_id": "CVE-2026-DOCS",
                "title": "Synthetic governed vulnerability",
                "cvss": 9.8,
                "epss": 0.91,
                "kev": True,
                "vendors": ["Example Vendor"],
                "products": ["Gateway"],
                "cwes": ["CWE-78"],
                "sighting_count": 2,
                "sighting_types": ["exploitation"],
                "provenance": {
                    "source_id": "opencve",
                    "canonical_url": "https://example.invalid/CVE-2026-DOCS",
                    "raw_sha256": "a" * 64,
                },
            }
        ],
        "claim_boundary": (
            "Documentation fixture: prioritization does not prove local deployment, "
            "exploitability, compromise or remediation status."
        ),
    }


def rbac_roles_fixture() -> list[dict[str, object]]:
    return [
        {
            "role": "admin",
            "permissions": ["manage:users", "manage:connectors", "approve:share"],
            "eligible_principal_types": ["human"],
            "immutable": True,
        },
        {
            "role": "analyst",
            "permissions": ["read:intelligence", "ingest:intelligence"],
            "eligible_principal_types": ["human"],
            "immutable": True,
        },
        {
            "role": "reviewer",
            "permissions": ["read:intelligence", "review:intelligence"],
            "eligible_principal_types": ["human"],
            "immutable": True,
        },
        {
            "role": "publisher",
            "permissions": ["read:intelligence", "approve:share", "export:reports"],
            "eligible_principal_types": ["human"],
            "immutable": True,
        },
    ]


def principals_fixture() -> list[dict[str, object]]:
    return [
        {
            "subject": "docs-admin@example.test",
            "display_name": "Documentation Administrator",
            "principal_type": "human",
            "active": True,
            "roles": ["admin"],
            "created_by": "documentation-capture",
            "updated_by": "documentation-capture",
            "created_at": "2026-08-15T09:00:00+00:00",
            "updated_at": "2026-08-15T09:00:00+00:00",
            "requires_token_reissue": False,
            "authorization_note": "Synthetic documentation identity; not a production principal.",
        },
        {
            "subject": "reviewer@example.test",
            "display_name": "Education Reviewer",
            "principal_type": "human",
            "active": True,
            "roles": ["reviewer"],
            "created_by": "documentation-capture",
            "updated_by": "documentation-capture",
            "created_at": "2026-08-15T09:00:00+00:00",
            "updated_at": "2026-08-15T09:00:00+00:00",
            "requires_token_reissue": True,
            "authorization_note": "Synthetic documentation identity; not a production principal.",
        },
    ]


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/dashboards/summary", lambda route: _json(route, dashboard_fixture()))
    await page.route(
        "**/api/v1/console/recent-intelligence?*",
        lambda route: _json(route, recent_intelligence_fixture()),
    )
    await page.route("**/api/v1/admin/sources/catalog", lambda route: _json(route, source_catalog_fixture()))
    await page.route("**/api/v1/source-center/status", lambda route: _json(route, source_status_fixture()))
    await page.route("**/api/v1/admin/sources", lambda route: _json(route, []))
    await page.route(
        "**/api/v1/console/vulnerability-analytics*",
        lambda route: _json(route, vulnerability_fixture()),
    )
    await page.route("**/api/v1/admin/rbac/roles", lambda route: _json(route, rbac_roles_fixture()))
    await page.route("**/api/v1/admin/rbac/principals", lambda route: _json(route, principals_fixture()))


async def capture(page: Page, output: Path, filename: str) -> None:
    await page.screenshot(path=str(output / filename), full_page=True)


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            viewport=VIEWPORT,
            extra_http_headers={
                "X-DTMO-Subject": "docs-admin@example.test",
                "X-DTMO-Roles": "admin",
            },
        )
        page = await context.new_page()
        await install_routes(page)
        await page.goto(base_url.rstrip("/") + "/", wait_until="networkidle")

        await page.locator('[data-view-panel="overview"]').wait_for(state="visible")
        await capture(page, output, "overview-dashboard.png")

        await page.get_by_role("button", name="Intelligence", exact=True).click()
        await page.locator('[data-view-panel="intelligence"]').wait_for(state="visible")
        await capture(page, output, "intelligence-workspace.png")

        await page.get_by_role("button", name="Bronnen & catalogus").click()
        await page.locator('[data-view-panel="sources"]').wait_for(state="visible")
        await capture(page, output, "sources-catalogue.png")

        await page.get_by_role("button", name="Intelligence", exact=True).click()
        await page.get_by_test_id("vuln-intelligence").wait_for(state="visible")
        await capture(page, output, "vulnerability-analytics.png")

        await page.get_by_role("button", name="Visual analytics", exact=True).click()
        await page.get_by_test_id("vuln-analytics").wait_for(state="visible")
        await capture(page, output, "visual-analytics.png")

        await page.get_by_role("button", name="Governance").click()
        await page.locator("#governance-knowledge").wait_for(state="visible")
        await capture(page, output, "governance-frameworks.png")

        await page.get_by_role("button", name="Administration").click()
        await page.locator("#rbac-administration").wait_for(state="visible")
        await capture(page, output, "administration-rbac.png")

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "files": sorted(path.name for path in output.glob("*.png")),
        }
        (output / "capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture sanitized deterministic screenshots from a running DTMO UI."
    )
    parser.add_argument("--base-url", required=True, help="Running DTMO base URL")
    parser.add_argument(
        "--output",
        default="docs/visual/screenshots/generated",
        help="Output directory for unreviewed generated screenshots",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
