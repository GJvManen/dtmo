from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}
RECORD_ID = "11111111-1111-4111-8111-111111111111"
MISP_RECORD_ID = "55555555-5555-4555-8555-555555555555"


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


def search_fixture() -> dict[str, object]:
    return {
        "query": "login.example",
        "count": 1,
        "results": [{"id": RECORD_ID, "title": "AIL domain indicator", "summary": "AIL extracted domain indicator: login.example", "source_id": "ail", "severity": "informational", "education_relevance": 80, "confidence_score": 75}],
    }


def misp_search_fixture() -> dict[str, object]:
    return {
        "query": "misp",
        "count": 1,
        "results": [{"id": MISP_RECORD_ID, "title": "MISP phishing campaign — documentation fixture", "summary": "Sanitized MISP-origin CTI retained as canonical DTMO intelligence with provenance and distribution restrictions.", "source_id": "misp", "severity": "high", "education_relevance": 92, "confidence_score": 88}],
    }


def workspace_fixture() -> dict[str, object]:
    return {"id": RECORD_ID, "source_id": "ail", "external_id": "domain:None:login.example", "item_type": "indicator", "title": "AIL domain indicator", "summary": "AIL extracted domain indicator: login.example", "canonical_url": "https://ail.example.test/api/v1/object?gid=domain%3ANone%3Alogin.example", "severity": "informational", "confidence_score": 75, "confidence_level": "high", "education_relevance": 80, "review_status": "candidate", "share_approved": False, "tags": ["documentation-fixture"], "context": {"cve_ids": [], "known_exploited": False, "vendor": None, "product": None}, "metadata": {}, "provenance": [], "published_at": None, "discovered_at": "2026-08-15T10:00:00+00:00", "confidence_rationale": ["Synthetic fixture for visual documentation"]}


def correlation_fixture() -> dict[str, object]:
    return {"status": "ok", "indicator": {"type": "domain", "value": "login.example"}, "investigation_references": [{"id": "case-docs-42"}], "raw_content_exposed": False, "analysis_only": True, "degraded_reasons": [], "claim_boundary": "Exact correlation is analytical context only; it does not prove exposure, compromise, attribution or share authority.", "correlations": [{"source_id": "misp", "external_id": "event-docs-1", "item_type": "cti_event", "title": "MISP phishing event — documentation fixture", "relation": "misp_object_attribute", "matched_value": "login.example", "context": {"object_name": "domain-ip", "type": "domain"}}, {"source_id": "opencve", "external_id": "CVE-2026-DOCS", "item_type": "vulnerability", "title": "Synthetic affected product context", "relation": "canonical_exact_match", "matched_value": "login.example", "context": {"vendor": "Example", "product": "Education Portal"}}]}


def audit_fixture() -> dict[str, object]:
    return {"count": 3, "read_only": True, "events": [{"event_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "action": "share.review", "principal": "reviewer@example.test", "decision": "permit", "resource": "intelligence:11111111-1111-4111-8111-111111111111", "event_hash": "7c6fe84f5db9d8f11b8ea52d0edb8a0f"}, {"event_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb", "action": "misp.export.prepare", "principal": "publisher@example.test", "decision": "permit", "resource": "misp:event-docs-1", "event_hash": "0ab9e671fc78ef38aa9b9d33727f1728"}, {"event_id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc", "action": "rbac.role.update", "principal": "admin@example.test", "decision": "permit", "resource": "role:analyst", "event_hash": "9c047193ae63ef01d955de5af6c5cc41"}]}


def auditor_session_fixture() -> dict[str, object]:
    return {"subject": "docs-auditor@example.test", "roles": ["auditor"], "permissions": ["read:audit"]}


def publisher_session_fixture() -> dict[str, object]:
    return {"subject": "docs-publisher@example.test", "roles": ["publisher"], "permissions": ["read:intelligence", "approve:share", "export:reports"], "service_account": False, "publication_requires_separate_human_approval": True}


async def install_routes(page: Page) -> None:
    await page.route("**/api/v1/intelligence/search?*", lambda route: _json(route, search_fixture()))
    await page.route(f"**/api/v1/intelligence/{RECORD_ID}/workspace", lambda route: _json(route, workspace_fixture()))
    await page.route(f"**/api/v1/intelligence/{RECORD_ID}/ail-correlations", lambda route: _json(route, correlation_fixture()))


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        analyst = await browser.new_context(viewport=VIEWPORT, extra_http_headers={"X-DTMO-Subject": "docs-analyst@example.test", "X-DTMO-Roles": "analyst"})
        page = await analyst.new_page()
        await install_routes(page)
        await page.goto(base_url.rstrip("/") + "/ui/intelligence-workspace", wait_until="networkidle")
        await page.locator("#query").fill("login.example")
        await page.get_by_role("button", name="Zoeken").click()
        await page.locator("[data-id]").click()
        await page.locator("#ail-correlation-panel").wait_for(state="visible")
        await page.locator("#ail-correlation-status").wait_for(state="visible")
        await page.screenshot(path=str(output / "ail-correlation-workspace.png"), full_page=True)
        await analyst.close()

        auditor = await browser.new_context(viewport=VIEWPORT, extra_http_headers={"X-DTMO-Subject": "docs-auditor@example.test", "X-DTMO-Roles": "auditor"})
        audit_page = await auditor.new_page()
        await audit_page.route("**/api/v1/ui/session", lambda route: _json(route, auditor_session_fixture()))
        await audit_page.route("**/api/v1/audit/events?*", lambda route: _json(route, audit_fixture()))
        await audit_page.goto(base_url.rstrip("/") + "/ui/auditor", wait_until="networkidle")
        await audit_page.locator("#audit-panel").wait_for(state="visible")
        await audit_page.get_by_role("button", name="Evidence laden").click()
        # A generic table row exists during the loading state. Wait for deterministic
        # fixture content instead so governed documentation never publishes a spinner.
        await audit_page.get_by_text("share.review", exact=True).wait_for(state="visible")
        await audit_page.get_by_text("misp.export.prepare", exact=True).wait_for(state="visible")
        await audit_page.get_by_text("rbac.role.update", exact=True).wait_for(state="visible")
        await audit_page.get_by_text("7c6fe84f5db9d8f11b8ea52d0edb8a0f", exact=True).wait_for(state="visible")
        await audit_page.screenshot(path=str(output / "audit-correlation.png"), full_page=True)
        await auditor.close()

        publisher = await browser.new_context(viewport=VIEWPORT, extra_http_headers={"X-DTMO-Subject": "docs-publisher@example.test", "X-DTMO-Roles": "publisher"})
        misp_page = await publisher.new_page()
        await misp_page.route("**/api/v1/ui/session", lambda route: _json(route, publisher_session_fixture()))
        await misp_page.route("**/api/v1/intelligence/search?*", lambda route: _json(route, misp_search_fixture()))
        await misp_page.goto(base_url.rstrip("/") + "/ui/misp-workspace", wait_until="networkidle")
        await misp_page.locator("#search-form").wait_for(state="visible")
        await misp_page.get_by_role("button", name="Zoeken").click()
        await misp_page.locator("#results .result").first.wait_for(state="visible")
        await misp_page.screenshot(path=str(output / "misp-governed-workflow.png"), full_page=True)
        await publisher.close()

        metadata = {"generated_at": datetime.now(UTC).isoformat(), "base_url": base_url, "browser": "chromium/playwright", "viewport": VIEWPORT, "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data", "evidence_classification": "documentation-illustration-only", "journeys": ["ail-indicator-to-correlation-workspace", "auditor-read-only-evidence-viewer", "misp-read-and-governed-export-workspace"], "raw_content_exposed": False, "audit_read_only": True, "audit_fixture_rendered": True, "misp_export_executed": False, "misp_live_connectivity_proven": False, "files": ["ail-correlation-workspace.png", "audit-correlation.png", "misp-governed-workflow.png"]}
        (output / "investigation-capture-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture governed DTMO investigation documentation screenshots.")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output", default="docs/visual/screenshots/generated", help="Output directory for unreviewed generated screenshots")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
