from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}
COLLECTION_ROUTE = "/workbench/collection"


def session_fixture() -> dict[str, object]:
    return {
        "subject": "docs-admin@example.test",
        "roles": ["admin"],
        "permissions": ["manage:connectors", "read:intelligence"],
    }


def catalog_fixture() -> list[dict[str, object]]:
    return [
        {
            "id": "cisa-kev",
            "name": "CISA KEV",
            "endpoint_url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
            "execution_status": "supported-built-in",
            "execution_profile": "governed-server-side",
            "reliability": "high",
            "recommended_interval_seconds": 3600,
        },
        {
            "id": "vendor-advisory",
            "name": "Vendor Advisory Feed",
            "endpoint_url": "https://example.invalid/advisories.json",
            "execution_status": "registration-required",
            "execution_profile": "json-feed",
            "reliability": "medium",
            "recommended_interval_seconds": 7200,
        },
    ]


def sources_fixture() -> list[dict[str, object]]:
    return [
        {
            "id": "vendor-advisory",
            "name": "Vendor Advisory Feed",
            "source_type": "json-feed",
            "endpoint_url": "https://example.invalid/advisories.json",
            "enabled": False,
            "interval_seconds": 7200,
            "reliability": "medium",
            "secret_ref": "vault://dtmo/sources/vendor-advisory",
            "authentication_mode": "secret-reference",
            "owner": "security-operations",
        }
    ]


def source_center_fixture() -> list[dict[str, object]]:
    return [
        {
            "id": "cisa-kev",
            "name": "CISA KEV",
            "execution_status": "supported-built-in",
            "registered": True,
            "enabled": True,
            "manual_run_available": True,
            "health_status": "ready",
            "last_success_at": "2026-08-27T12:15:00+00:00",
            "last_failure_at": None,
            "consecutive_failures": 0,
            "provenance": {
                "endpoint": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                "configured_reliability": "high",
                "note": "Public CISA source identity shown for deterministic documentation only.",
            },
        },
        {
            "id": "vendor-advisory",
            "name": "Vendor Advisory Feed",
            "execution_status": "registered-adapter",
            "registered": True,
            "enabled": False,
            "manual_run_available": False,
            "health_status": "disabled",
            "last_success_at": None,
            "last_failure_at": None,
            "consecutive_failures": 0,
            "provenance": {
                "endpoint": "https://example.invalid/advisories.json",
                "configured_reliability": "medium",
                "note": "Synthetic documentation source; disabled and not executed.",
            },
        },
    ]


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/ui/session", lambda route: _json(route, session_fixture()))
    await page.route("**/api/v1/admin/sources/catalog", lambda route: _json(route, catalog_fixture()))
    await page.route("**/api/v1/admin/sources", lambda route: _json(route, sources_fixture()))
    await page.route("**/api/v1/source-center/status", lambda route: _json(route, source_center_fixture()))


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        await install_routes(page)
        url = base_url.rstrip("/") + COLLECTION_ROUTE
        await page.goto(url, wait_until="networkidle")
        await page.get_by_role("heading", name="Sources & Collection", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Code-reviewed source profiles", exact=True).wait_for(state="visible")
        await page.get_by_role("button").filter(has_text="CISA KEV").first.click()
        await page.get_by_role("heading", name="CISA KEV", exact=True).wait_for(state="visible")
        await page.get_by_text("Built-in DTMO adapter", exact=False).wait_for(state="visible")
        await page.get_by_text("manual load available", exact=False).first.wait_for(state="visible")
        await page.screenshot(path=str(output / "sources-collection-workbench.png"), full_page=True)

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "canonical_route": COLLECTION_ROUTE,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "journey": "source catalog -> built-in readiness -> provenance boundary",
            "live_connectivity_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
            "connector_execution_proven": False,
            "source_activation_authority_proven": False,
            "publication_authority_proven": False,
            "credential_value_exposed": False,
            "files": ["sources-collection-workbench.png"],
        }
        (output / "canonical-sources-collection-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture canonical DTMO Sources & Collection documentation screenshot.")
    parser.add_argument("--base-url", required=True, help="Running DTMO base URL")
    parser.add_argument("--output", required=True, help="Output directory for unreviewed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
