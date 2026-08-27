from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}
SHARING_ROUTE = "/workbench/sharing"
ITEM_ID = "66666666-6666-4666-8666-666666666666"


def session_fixture() -> dict[str, object]:
    return {
        "subject": "docs-approver@example.test",
        "roles": ["publisher"],
        "permissions": ["read:intelligence", "approve:share"],
    }


def command_center_fixture() -> dict[str, object]:
    return {
        "data_state": "available",
        "recent_intelligence": [
            {
                "id": ITEM_ID,
                "title": "Phishing campaign — canonical documentation fixture",
                "source_id": "misp",
                "severity": "high",
                "education_relevance": 92,
                "review_status": "reviewed",
                "discovered_at": "2026-08-27T12:00:00+00:00",
            }
        ],
    }


def sharing_state_fixture() -> dict[str, object]:
    return {
        "item_id": ITEM_ID,
        "title": "Phishing campaign — canonical documentation fixture",
        "source_id": "misp",
        "canonical_url": "https://example.invalid/canonical/misp-event-docs",
        "review_status": "reviewed",
        "reviewed_by": "docs-reviewer@example.test",
        "share_approved": True,
        "share_approved_by": "docs-approver@example.test",
        "misp_restrictions": {
            "restriction_authoritative": True,
            "distribution": "1",
            "sharing_group_id": None,
            "tlp_tags": ["tlp:amber"],
        },
        "misp_exports": [
            {
                "status": "success",
                "event_uuid": "77777777-7777-4777-8777-777777777777",
                "misp_event_id": "docs-event-42",
                "distribution": "1",
                "sharing_group_id": None,
                "tlp": "tlp:amber",
                "requested_by": "docs-approver@example.test",
            }
        ],
        "current_event_uuid": "77777777-7777-4777-8777-777777777777",
        "export_eligible": True,
        "export_blockers": [],
        "principal_actions": {"can_review": False, "can_approve_share": True},
        "misp_export_enabled": True,
        "misp_export_configured": True,
        "runtime_health_claim": False,
        "publication_authority": False,
        "synchronization_authority": False,
        "evidence_boundary": (
            "Synthetic fixture-backed transfer history demonstrates the rendered governance chain only. "
            "It does not prove live MISP connectivity, publication, synchronization or production authorization."
        ),
    }


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/ui/session", lambda route: _json(route, session_fixture()))
    await page.route("**/api/v1/command-center", lambda route: _json(route, command_center_fixture()))
    await page.route(
        f"**/api/v1/sharing/items/{ITEM_ID}",
        lambda route: _json(route, sharing_state_fixture()),
    )


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        await install_routes(page)
        url = base_url.rstrip("/") + SHARING_ROUTE + f"?item={ITEM_ID}"
        await page.goto(url, wait_until="networkidle")
        await page.get_by_role("heading", name="Sharing & Exchange", exact=True).wait_for(state="visible")
        await page.get_by_role(
            "heading", name="Phishing campaign — canonical documentation fixture", exact=True
        ).wait_for(state="visible")
        await page.get_by_role("heading", name="Create unpublished event", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Authoritative source constraints", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="MISP export history", exact=True).wait_for(state="visible")
        await page.get_by_text("Publication authority: no", exact=True).wait_for(state="visible")
        await page.get_by_text("Synchronization authority: no", exact=True).wait_for(state="visible")
        await page.screenshot(path=str(output / "sharing-exchange-workbench.png"), full_page=True)

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "canonical_route": SHARING_ROUTE,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "journey": "independent review -> separate share approval -> unpublished MISP export evidence -> authority boundary",
            "live_connectivity_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
            "human_review_executed": False,
            "share_approval_executed": False,
            "misp_export_executed": False,
            "publication_authority_proven": False,
            "synchronization_authority_proven": False,
            "credential_value_exposed": False,
            "files": ["sharing-exchange-workbench.png"],
        }
        (output / "canonical-sharing-exchange-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture canonical DTMO Sharing & Exchange documentation screenshot.")
    parser.add_argument("--base-url", required=True, help="Running DTMO base URL")
    parser.add_argument("--output", required=True, help="Output directory for unreviewed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
