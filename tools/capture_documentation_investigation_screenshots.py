from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}
RECORD_ID = "11111111-1111-4111-8111-111111111111"


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


def search_fixture() -> dict[str, object]:
    return {
        "query": "login.example",
        "count": 1,
        "results": [
            {
                "id": RECORD_ID,
                "title": "AIL domain indicator",
                "summary": "AIL extracted domain indicator: login.example",
                "source_id": "ail",
                "severity": "informational",
                "education_relevance": 80,
                "confidence_score": 75,
            }
        ],
    }


def workspace_fixture() -> dict[str, object]:
    return {
        "id": RECORD_ID,
        "source_id": "ail",
        "external_id": "domain:None:login.example",
        "item_type": "indicator",
        "title": "AIL domain indicator",
        "summary": "AIL extracted domain indicator: login.example",
        "canonical_url": "https://ail.example.test/api/v1/object?gid=domain%3ANone%3Alogin.example",
        "severity": "informational",
        "confidence_score": 75,
        "confidence_level": "high",
        "education_relevance": 80,
        "review_status": "candidate",
        "share_approved": False,
        "tags": ["documentation-fixture"],
        "context": {"cve_ids": [], "known_exploited": False, "vendor": None, "product": None},
        "metadata": {},
        "provenance": [],
        "published_at": None,
        "discovered_at": "2026-08-15T10:00:00+00:00",
        "confidence_rationale": ["Synthetic fixture for visual documentation"],
    }


def correlation_fixture() -> dict[str, object]:
    return {
        "status": "ok",
        "indicator": {"type": "domain", "value": "login.example"},
        "investigation_references": [{"id": "case-docs-42"}],
        "raw_content_exposed": False,
        "analysis_only": True,
        "degraded_reasons": [],
        "claim_boundary": (
            "Exact correlation is analytical context only; it does not prove exposure, "
            "compromise, attribution or share authority."
        ),
        "correlations": [
            {
                "source_id": "misp",
                "external_id": "event-docs-1",
                "item_type": "cti_event",
                "title": "MISP phishing event — documentation fixture",
                "relation": "misp_object_attribute",
                "matched_value": "login.example",
                "context": {"object_name": "domain-ip", "type": "domain"},
            },
            {
                "source_id": "opencve",
                "external_id": "CVE-2026-DOCS",
                "item_type": "vulnerability",
                "title": "Synthetic affected product context",
                "relation": "canonical_exact_match",
                "matched_value": "login.example",
                "context": {"vendor": "Example", "product": "Education Portal"},
            },
        ],
    }


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/intelligence/search?*", lambda route: _json(route, search_fixture()))
    await page.route(
        f"**/api/v1/intelligence/{RECORD_ID}/workspace",
        lambda route: _json(route, workspace_fixture()),
    )
    await page.route(
        f"**/api/v1/intelligence/{RECORD_ID}/ail-correlations",
        lambda route: _json(route, correlation_fixture()),
    )


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            viewport=VIEWPORT,
            extra_http_headers={
                "X-DTMO-Subject": "docs-analyst@example.test",
                "X-DTMO-Roles": "analyst",
            },
        )
        page = await context.new_page()
        await install_routes(page)
        await page.goto(base_url.rstrip("/") + "/ui/intelligence-workspace", wait_until="networkidle")
        await page.locator("#query").fill("login.example")
        await page.get_by_role("button", name="Zoeken").click()
        await page.locator("[data-id]").click()
        await page.locator("#ail-correlation-panel").wait_for(state="visible")
        await page.locator("#ail-correlation-status").wait_for(state="visible")
        await page.screenshot(path=str(output / "ail-correlation-workspace.png"), full_page=True)

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "journey": "ail-indicator-to-correlation-workspace",
            "raw_content_exposed": False,
            "files": ["ail-correlation-workspace.png"],
        }
        (output / "investigation-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture governed DTMO investigation documentation screenshots.")
    parser.add_argument("--base-url", required=True)
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
