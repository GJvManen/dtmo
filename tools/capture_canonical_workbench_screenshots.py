from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}
COMMAND_CENTER_ROUTE = "/workbench/command-center"


def session_fixture() -> dict[str, object]:
    return {
        "subject": "docs-admin@example.test",
        "roles": ["admin"],
        "permissions": [
            "read:intelligence",
            "review:intelligence",
            "manage:connectors",
            "handoff:case",
            "approve:share",
            "manage:users",
        ],
    }


def command_center_fixture() -> dict[str, object]:
    return {
        "generated_at": "2026-08-27T12:00:00+00:00",
        "data_state": "available",
        "metrics": [
            {"id": "intel", "label": "Canonical intelligence", "value": 128, "tone": "accent"},
            {"id": "high", "label": "High severity", "value": 14, "tone": "critical"},
            {"id": "review", "label": "Awaiting review", "value": 9, "tone": "warning"},
            {"id": "sources", "label": "Active sources", "value": 7, "tone": "neutral"},
            {"id": "cases", "label": "Open investigations", "value": 5, "tone": "neutral"},
            {"id": "runs", "label": "Recent automation runs", "value": 11, "tone": "neutral"},
        ],
        "recent_intelligence": [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "title": "Governed vulnerability intelligence example",
                "source_id": "cisa-kev",
                "severity": "high",
                "education_relevance": 93,
                "review_status": "candidate",
                "discovered_at": "2026-08-27T11:45:00+00:00",
            },
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "title": "Correlated threat-intelligence observation",
                "source_id": "ail",
                "severity": "medium",
                "education_relevance": 81,
                "review_status": "reviewed",
                "discovered_at": "2026-08-27T10:30:00+00:00",
            },
        ],
        "trends": {
            "intelligence_7d": [
                {"date": "2026-08-21", "count": 8},
                {"date": "2026-08-22", "count": 11},
                {"date": "2026-08-23", "count": 7},
                {"date": "2026-08-24", "count": 15},
                {"date": "2026-08-25", "count": 13},
                {"date": "2026-08-26", "count": 19},
                {"date": "2026-08-27", "count": 16},
            ],
            "severity_distribution": [
                {"severity": "critical", "count": 3},
                {"severity": "high", "count": 14},
                {"severity": "medium", "count": 37},
                {"severity": "low", "count": 49},
                {"severity": "informational", "count": 25},
            ],
        },
        "integrations": [
            {
                "id": "taranis",
                "label": "Taranis AI",
                "state": "enabled",
                "enabled": True,
                "configured": True,
                "scheduled_collection": True,
                "runtime_observation": "success",
                "last_observed_at": "2026-08-27T11:30:00+00:00",
                "runtime_health_claim": False,
            },
            {
                "id": "ail",
                "label": "AIL",
                "state": "enabled",
                "enabled": True,
                "configured": True,
                "scheduled_collection": False,
                "runtime_observation": "success",
                "last_observed_at": "2026-08-27T11:20:00+00:00",
                "runtime_health_claim": False,
            },
            {
                "id": "intelowl",
                "label": "IntelOwl",
                "state": "configuration-required",
                "enabled": False,
                "configured": False,
                "scheduled_collection": False,
                "runtime_observation": None,
                "last_observed_at": None,
                "runtime_health_claim": False,
            },
        ],
        "evidence_boundary": (
            "Synthetic documentation fixture: capability and runtime observations do not prove "
            "live-source truth, production-equivalent behavior or production authorization."
        ),
    }


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/ui/session", lambda route: _json(route, session_fixture()))
    await page.route("**/api/v1/command-center", lambda route: _json(route, command_center_fixture()))


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        await install_routes(page)
        url = base_url.rstrip("/") + COMMAND_CENTER_ROUTE
        await page.goto(url, wait_until="networkidle")
        await page.get_by_role("heading", name="Command Center", exact=True).wait_for(state="visible")
        await page.get_by_text("Canonical data available", exact=True).wait_for(state="visible")
        await page.screenshot(path=str(output / "command-center-workbench.png"), full_page=True)

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "canonical_route": COMMAND_CENTER_ROUTE,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "live_connectivity_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
            "files": ["command-center-workbench.png"],
        }
        (output / "canonical-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture current canonical DTMO workbench screenshots.")
    parser.add_argument("--base-url", required=True, help="Running DTMO base URL")
    parser.add_argument("--output", required=True, help="Output directory for unreviewed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
