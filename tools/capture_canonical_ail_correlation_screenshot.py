from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}
IOC_ROUTE = "/workbench/intelligence/iocs"
ITEM_ID = "11111111-1111-4111-8111-111111111111"


def session_fixture() -> dict[str, object]:
    return {
        "subject": "docs-analyst@example.test",
        "roles": ["analyst"],
        "permissions": ["read:intelligence"],
    }


def inventory_fixture() -> dict[str, object]:
    return {
        "records": [
            {
                "record_id": "ioc-docs-1",
                "item_id": ITEM_ID,
                "item_title": "AIL domain indicator",
                "source_id": "ail",
                "severity": "informational",
                "confidence_score": 75,
                "observable_type": "domain",
                "observable_value": "login.example",
                "handling": "TLP:AMBER",
                "status": "persisted",
                "analyzers": ["ail"],
                "created_at": "2026-08-27T12:00:00+00:00",
                "external_share_authorized": False,
                "local_compromise_proven": False,
            }
        ],
        "evidence_boundary": (
            "Persisted IOC evidence only; no verdict, compromise finding or sharing authority is inferred."
        ),
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
            "Exact correlation is analytical context only; it does not prove exposure, compromise, "
            "attribution or share authority."
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


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/ui/session", lambda route: _json(route, session_fixture()))
    await page.route("**/api/v1/iocs?*", lambda route: _json(route, inventory_fixture()))
    await page.route(
        f"**/api/v1/intelligence/{ITEM_ID}/ail-correlations",
        lambda route: _json(route, correlation_fixture()),
    )


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        await install_routes(page)
        await page.goto(base_url.rstrip("/") + IOC_ROUTE, wait_until="networkidle")

        await page.get_by_role("heading", name="IOC Explorer", exact=True).wait_for(state="visible")
        await page.get_by_text("login.example", exact=True).wait_for(state="visible")
        await page.get_by_role("button", name="Inspect AIL correlation", exact=True).click()
        panel = page.get_by_role("article", name="AIL correlation context")
        await panel.wait_for(state="visible")
        await panel.get_by_text("MISP phishing event — documentation fixture", exact=True).wait_for(state="visible")
        await panel.get_by_text("Synthetic affected product context", exact=True).wait_for(state="visible")
        await panel.get_by_text("AIL investigation references: case-docs-42.", exact=False).wait_for(state="visible")
        await panel.get_by_text("Raw content exposed", exact=True).wait_for(state="visible")
        await panel.get_by_text("no", exact=True).first.wait_for(state="visible")

        candidate_filename = "ail-correlation-workbench.png"
        await page.screenshot(path=str(output / candidate_filename), full_page=True)

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "canonical_route": IOC_ROUTE,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "journey": "persisted IOC -> read-only AIL correlation context -> evidence boundary",
            "raw_content_exposed": False,
            "analysis_only": True,
            "credential_value_exposed": False,
            "live_connectivity_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
            "review_authority_proven": False,
            "share_authority_proven": False,
            "case_authority_proven": False,
            "publication_authority_proven": False,
            "files": [candidate_filename],
        }
        (output / "canonical-ail-correlation-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture canonical DTMO UI-06 AIL correlation documentation screenshot.")
    parser.add_argument("--base-url", required=True, help="Running DTMO canonical base URL")
    parser.add_argument("--output", required=True, help="Output directory for unreviewed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
