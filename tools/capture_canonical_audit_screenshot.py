from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

AUDIT_ROUTE = "/workbench/administration"
VIEWPORT = {"width": 1440, "height": 1000}


def _json(route: Route, payload: object) -> None:
    asyncio.create_task(route.fulfill(status=200, content_type="application/json", body=json.dumps(payload)))


def session_fixture() -> dict[str, object]:
    return {
        "subject": "documentation-auditor@example.invalid",
        "roles": ["auditor"],
        "permissions": ["read:audit"],
        "service_account": False,
    }


def audit_fixture() -> dict[str, object]:
    return {
        "count": 3,
        "read_only": True,
        "events": [
            {
                "sequence_number": 101,
                "event_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                "occurred_at": "2026-08-27T16:30:00Z",
                "principal": "reviewer@example.invalid",
                "principal_type": "human",
                "action": "share.review",
                "resource": "intelligence:11111111-1111-4111-8111-111111111111",
                "decision": "permit",
                "request_id": "req-docs-review-001",
                "provenance_reference": "prov-docs-intel-001",
                "event_hash": "7c6fe84f5db9d8f11b8ea52d0edb8a0f",
            },
            {
                "sequence_number": 102,
                "event_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                "occurred_at": "2026-08-27T16:31:00Z",
                "principal": "publisher@example.invalid",
                "principal_type": "human",
                "action": "misp.export.prepare",
                "resource": "misp:event-docs-1",
                "decision": "permit",
                "request_id": "req-docs-export-002",
                "provenance_reference": "prov-docs-misp-002",
                "event_hash": "0ab9e671fc78ef38aa9b9d33727f1728",
            },
            {
                "sequence_number": 103,
                "event_id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
                "occurred_at": "2026-08-27T16:32:00Z",
                "principal": "admin@example.invalid",
                "principal_type": "human",
                "action": "rbac.role.update",
                "resource": "principal:alice@example.invalid",
                "decision": "permit",
                "request_id": "req-docs-rbac-003",
                "provenance_reference": "prov-docs-rbac-003",
                "event_hash": "9c047193ae63ef01d955de5af6c5cc41",
            },
        ],
    }


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/ui/session", lambda route: _json(route, session_fixture()))
    await page.route("**/api/v1/audit/events?*", lambda route: _json(route, audit_fixture()))


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        await install_routes(page)
        await page.goto(base_url.rstrip("/") + AUDIT_ROUTE, wait_until="networkidle")

        await page.get_by_role("heading", name="Security & audit", exact=True).wait_for(state="visible")
        audit_panel = page.locator('[data-admin-security="audit-evidence"]')
        await audit_panel.wait_for(state="visible")
        await audit_panel.get_by_text("share.review", exact=True).wait_for(state="visible")
        await audit_panel.get_by_text("misp.export.prepare", exact=True).wait_for(state="visible")
        await audit_panel.get_by_text("rbac.role.update", exact=True).wait_for(state="visible")
        await audit_panel.get_by_text("req-docs-review-001", exact=True).wait_for(state="visible")
        await audit_panel.get_by_text("7c6fe84f5db9d8f11b8ea52d0edb8a0f", exact=True).wait_for(state="visible")

        candidate_filename = "audit-correlation-workbench.png"
        await audit_panel.screenshot(path=str(output / candidate_filename))

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "canonical_route": AUDIT_ROUTE,
            "canonical_section": "security-audit/read-only-audit-evidence",
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "journey": "canonical administration -> security & audit -> read-only append-only audit evidence -> request/event correlation attributes",
            "fixture_backed": True,
            "audit_read_only": True,
            "audit_fixture_rendered": True,
            "request_id_correlation_rendered": True,
            "mutation_executed": False,
            "token_revocation_executed": False,
            "live_connectivity_proven": False,
            "production_activity_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
            "independent_assurance_proven": False,
            "review_authority_proven": False,
            "share_authority_proven": False,
            "publication_authority_proven": False,
            "files": [candidate_filename],
        }
        (output / "canonical-audit-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture canonical DTMO UI-10 read-only audit documentation screenshot.")
    parser.add_argument("--base-url", required=True, help="Running DTMO canonical base URL")
    parser.add_argument("--output", required=True, help="Output directory for unreviewed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
