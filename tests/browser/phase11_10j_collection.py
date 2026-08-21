from __future__ import annotations

import json
import os

from playwright.sync_api import sync_playwright


BASE_URL = os.environ.get("DTMO_BROWSER_BASE_URL", "http://127.0.0.1:4173")


def fulfill(route, payload, status: int = 200) -> None:
    route.fulfill(status=status, content_type="application/json", body=json.dumps(payload))


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.route("**/health", lambda route: fulfill(route, {
            "status": "healthy",
            "version": "phase11.10j-browser-fixture",
            "environment": "repository-browser-fixture",
            "publication_gate": "human-review-required",
            "authentication": "fixture",
        }))
        page.route("**/api/v1/ui/session", lambda route: fulfill(route, {
            "subject": "phase11-10j-admin",
            "roles": ["admin"],
            "permissions": ["manage:connectors"],
        }))
        page.route("**/api/v1/admin/sources/catalog", lambda route: fulfill(route, [{
            "id": "fixture-source",
            "name": "Fixture source",
            "endpoint_url": "https://example.test/feed.json",
            "execution_status": "supported",
            "execution_profile": "fixture",
            "reliability": "medium",
            "recommended_interval_seconds": 3600,
        }]))
        page.route("**/api/v1/admin/sources", lambda route: fulfill(route, [{
            "id": "fixture-source",
            "name": "Fixture source",
            "source_type": "json-feed",
            "endpoint_url": "https://example.test/feed.json",
            "enabled": False,
            "interval_seconds": 3600,
            "reliability": "medium",
            "secret_ref": None,
            "authentication_mode": "anonymous",
            "owner": "phase11-10j-admin",
            "created_by": "phase11-10j-admin",
            "updated_by": "phase11-10j-admin",
        }]))
        page.route("**/api/v1/admin/sources/fixture-source/validate", lambda route: fulfill(route, {
            "id": "fixture-source",
            "valid": True,
            "enabled": False,
            "authentication_mode": "anonymous",
            "note": "repository browser fixture only",
        }))

        page.goto(BASE_URL, wait_until="networkidle")
        page.get_by_role("link", name="Collection", exact=True).click()
        page.get_by_role("heading", name="Sources & Collection").wait_for()
        assert page.get_by_text("Collection ≠ publication").is_visible()
        assert page.get_by_text("Fixture source").is_visible()
        page.get_by_role("button", name="Fixture source").click()
        page.get_by_role("button", name="validate").click()
        page.get_by_text("Last bounded action").wait_for()
        assert page.get_by_text("Attributable collection without inferred trust").is_visible()
        body = page.locator("body").inner_text().lower()
        assert "production readiness" in body
        assert "publication authorization" in body
        browser.close()


if __name__ == "__main__":
    main()
