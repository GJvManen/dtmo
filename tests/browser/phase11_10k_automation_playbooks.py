from __future__ import annotations

import json
import os

from playwright.sync_api import sync_playwright


BASE_URL = os.environ.get("DTMO_BROWSER_BASE_URL", "http://127.0.0.1:4173/workbench/")


def fulfill(route, payload, status: int = 200) -> None:
    route.fulfill(status=status, content_type="application/json", body=json.dumps(payload))


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.route("**/health", lambda route: fulfill(route, {
            "status": "healthy",
            "version": "phase11.10k-browser-fixture",
            "environment": "repository-browser-fixture",
            "publication_gate": "human-approval-required",
            "authentication": "fixture",
            "scheduler": {"running": True, "started_at": "2026-08-21T12:00:00Z", "jobs": [{"id": "cisa-kev", "next_run_time": "2026-08-21 13:00:00+00:00"}]},
        }))
        page.route("**/api/v1/ui/session", lambda route: fulfill(route, {
            "subject": "phase11-10k-admin",
            "roles": ["admin"],
            "permissions": ["manage:connectors"],
        }))
        page.route("**/connectors", lambda route: fulfill(route, [{
            "id": "cisa-kev", "enabled": True, "reliability": "authoritative", "schedule_seconds": 3600, "manual_run_available": True,
        }]))
        page.route("**/connectors/cisa-kev/run", lambda route: fulfill(route, {
            "connector_id": "cisa-kev", "status": "completed", "records": 2, "inserted": 1, "indexed": 1, "attempts": 1, "error": None, "alert_state": "clear", "correlation_id": "fixture-correlation",
        }))

        page.goto(BASE_URL, wait_until="networkidle")
        page.get_by_role("link", name="Automation & Playbooks", exact=True).click()
        page.get_by_role("heading", name="Automation & Playbooks").wait_for()
        assert page.get_by_text("Automation ≠ remediation authority").is_visible()
        assert page.get_by_text("cisa-kev", exact=True).first.is_visible()
        page.get_by_role("button", name="cisa-kev").click()
        page.get_by_role("button", name="Run bounded collection playbook").click()
        page.get_by_text("Observed bounded execution result").wait_for()
        assert page.get_by_text("Correlation: fixture-correlation").is_visible()
        body = page.locator("body").inner_text().lower()
        assert "source truth" in body
        assert "remediation" in body
        assert "publication authority" in body
        assert "production authorization" in body
        browser.close()


if __name__ == "__main__":
    main()
