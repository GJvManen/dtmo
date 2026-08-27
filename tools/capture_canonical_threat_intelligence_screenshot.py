from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}
THREAT_INTELLIGENCE_ROUTE = "/workbench/intelligence"
ITEM_ID = "11111111-1111-1111-1111-111111111111"


def session_fixture() -> dict[str, object]:
    return {
        "subject": "docs-analyst@example.test",
        "roles": ["analyst"],
        "permissions": ["read:intelligence", "review:intelligence"],
    }


def command_center_fixture() -> dict[str, object]:
    return {
        "generated_at": "2026-08-27T12:00:00+00:00",
        "data_state": "available",
        "metrics": [],
        "recent_intelligence": [
            {
                "id": ITEM_ID,
                "title": "Critical edge-device exploitation activity",
                "source_id": "cisa-kev",
                "severity": "high",
                "education_relevance": 94,
                "review_status": "candidate",
                "discovered_at": "2026-08-27T11:45:00+00:00",
            },
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "title": "Credential-phishing infrastructure correlation",
                "source_id": "ail",
                "severity": "medium",
                "education_relevance": 86,
                "review_status": "reviewed",
                "discovered_at": "2026-08-27T10:30:00+00:00",
            },
        ],
        "integrations": [],
        "evidence_boundary": "Synthetic documentation fixture only.",
    }


def detail_fixture() -> dict[str, object]:
    return {
        "id": ITEM_ID,
        "source_id": "cisa-kev",
        "external_id": "CVE-2026-DOCS",
        "item_type": "vulnerability-intelligence",
        "title": "Critical edge-device exploitation activity",
        "summary": (
            "Governed canonical intelligence example showing an actively exploited edge-device vulnerability "
            "relevant to education-sector perimeter services."
        ),
        "canonical_url": "https://example.invalid/advisories/CVE-2026-DOCS",
        "published_at": "2026-08-27T10:00:00+00:00",
        "discovered_at": "2026-08-27T11:45:00+00:00",
        "severity": "high",
        "confidence_score": 92,
        "confidence_level": "high",
        "confidence_rationale": "Primary-source advisory and attributable exploitation evidence are present in the fixture.",
        "education_relevance": 94,
        "review_status": "candidate",
        "share_approved": False,
        "tags": ["edge-device", "education-sector", "active-exploitation"],
        "context": {
            "cve_ids": ["CVE-2026-DOCS"],
            "known_exploited": True,
            "vendor": "Example Networks",
            "product": "Edge Gateway",
        },
        "provenance": [
            {
                "source_url": "https://example.invalid/advisories/CVE-2026-DOCS",
                "source_title": "Example primary security advisory",
                "publisher": "Example Networks",
                "retrieved_at": "2026-08-27T11:40:00+00:00",
                "source_reliability": "A",
                "is_primary_source": True,
                "content_integrity_verified": True,
                "confidence_score": 95,
            },
            {
                "source_url": "https://example.invalid/kev/CVE-2026-DOCS",
                "source_title": "Known exploited catalogue record",
                "publisher": "CISA KEV fixture",
                "retrieved_at": "2026-08-27T11:42:00+00:00",
                "source_reliability": "A",
                "is_primary_source": False,
                "content_integrity_verified": True,
                "confidence_score": 91,
            },
        ],
    }


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/ui/session", lambda route: _json(route, session_fixture()))
    await page.route("**/api/v1/command-center", lambda route: _json(route, command_center_fixture()))
    await page.route(
        f"**/api/v1/intelligence/{ITEM_ID}/workspace",
        lambda route: _json(route, detail_fixture()),
    )


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        await install_routes(page)
        url = base_url.rstrip("/") + THREAT_INTELLIGENCE_ROUTE
        await page.goto(url, wait_until="networkidle")
        await page.get_by_role("heading", name="Threat Intelligence", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Recent canonical intelligence", exact=True).wait_for(state="visible")
        await page.get_by_role("button", name="Open Critical edge-device exploitation activity", exact=True).click()
        await page.get_by_role("heading", name="Critical edge-device exploitation activity", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Provenance chain", exact=True).wait_for(state="visible")
        await page.get_by_text("Example primary security advisory", exact=True).wait_for(state="visible")
        await page.screenshot(path=str(output / "threat-intelligence-workbench.png"), full_page=True)

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "canonical_route": THREAT_INTELLIGENCE_ROUTE,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "journey": "recent canonical intelligence -> object detail -> provenance chain",
            "live_connectivity_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
            "review_authority_proven": False,
            "share_authority_proven": False,
            "files": ["threat-intelligence-workbench.png"],
        }
        (output / "canonical-threat-intelligence-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture canonical DTMO Threat Intelligence documentation screenshot.")
    parser.add_argument("--base-url", required=True, help="Running DTMO base URL")
    parser.add_argument("--output", required=True, help="Output directory for unreviewed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
