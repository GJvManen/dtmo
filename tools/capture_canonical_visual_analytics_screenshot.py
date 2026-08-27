from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}
ANALYTICS_ROUTE = "/workbench/analytics"


def session_fixture() -> dict[str, object]:
    return {
        "subject": "docs-analyst@example.test",
        "roles": ["analyst"],
        "permissions": ["read:intelligence", "read:vulnerabilities"],
    }


def command_center_fixture() -> dict[str, object]:
    return {
        "data_state": "available",
        "trends": {
            "intelligence_7d": [
                {"date": "2026-08-21", "count": 8},
                {"date": "2026-08-22", "count": 13},
                {"date": "2026-08-23", "count": 10},
                {"date": "2026-08-24", "count": 17},
                {"date": "2026-08-25", "count": 14},
                {"date": "2026-08-26", "count": 21},
                {"date": "2026-08-27", "count": 18},
            ],
            "severity_distribution": [
                {"severity": "critical", "count": 4},
                {"severity": "high", "count": 11},
                {"severity": "medium", "count": 19},
                {"severity": "low", "count": 9},
                {"severity": "informational", "count": 6},
            ],
        },
    }


def vulnerability_fixture() -> dict[str, object]:
    return {
        "status": "ok",
        "trend": [
            {"date": "2026-08-21", "count": 3},
            {"date": "2026-08-22", "count": 5},
            {"date": "2026-08-23", "count": 4},
            {"date": "2026-08-24", "count": 7},
            {"date": "2026-08-25", "count": 6},
            {"date": "2026-08-26", "count": 9},
            {"date": "2026-08-27", "count": 8},
        ],
        "summary": {"total": 42, "kev": 5, "with_sightings": 7},
        "claim_boundary": (
            "Repository-controlled documentation fixtures illustrate prioritization context only; "
            "they do not prove that any local asset is exposed, affected or exploitable."
        ),
    }


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/ui/session", lambda route: _json(route, session_fixture()))
    await page.route("**/api/v1/command-center", lambda route: _json(route, command_center_fixture()))
    await page.route(
        "**/api/v1/console/vulnerability-analytics",
        lambda route: _json(route, vulnerability_fixture()),
    )


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        await install_routes(page)
        await page.goto(base_url.rstrip("/") + ANALYTICS_ROUTE, wait_until="networkidle")

        await page.get_by_role("heading", name="Visual Analytics", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Intelligence arrivals · 7 days", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Severity distribution", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Vulnerability observations", exact=True).wait_for(state="visible")
        await page.get_by_role("table", name="Intelligence arrivals · 7 days table").wait_for(state="visible")
        await page.get_by_role("table", name="Severity distribution table").wait_for(state="visible")
        await page.get_by_role("table", name="Vulnerability observations table").wait_for(state="visible")
        boundary = page.get_by_role("region", name="Analytics evidence boundary")
        await boundary.wait_for(state="visible")
        await boundary.get_by_text("does not prove local exposure", exact=False).wait_for(state="visible")

        candidate_filename = "visual-analytics-workbench.png"
        await page.screenshot(path=str(output / candidate_filename), full_page=True)

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "canonical_route": ANALYTICS_ROUTE,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "journey": "canonical intelligence trends -> severity distribution -> vulnerability observations -> evidence boundary",
            "fixture_backed": True,
            "credential_value_exposed": False,
            "live_connectivity_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
            "local_exposure_proven": False,
            "review_authority_proven": False,
            "share_authority_proven": False,
            "publication_authority_proven": False,
            "files": [candidate_filename],
        }
        (output / "canonical-visual-analytics-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture canonical DTMO UI-07 Visual Analytics documentation screenshot.")
    parser.add_argument("--base-url", required=True, help="Running DTMO canonical base URL")
    parser.add_argument("--output", required=True, help="Output directory for unreviewed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
