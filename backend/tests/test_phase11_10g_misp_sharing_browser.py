from __future__ import annotations

import json
import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import Page, Route, expect, sync_playwright

BASE_URL = os.getenv("DTMO_BROWSER_BASE_URL", "").rstrip("/")
ITEM_ID = "00000000-0000-0000-0000-000000000052"


@pytest.fixture()
def page() -> Iterator[Page]:
    if not BASE_URL:
        pytest.skip("Phase 11.10g browser acceptance requires DTMO_BROWSER_BASE_URL")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            browser.close()


def respond(route: Route, payload: object, status: int = 200) -> None:
    route.fulfill(status=status, content_type="application/json", body=json.dumps(payload))


def health(route: Route) -> None:
    respond(route, {"status": "healthy", "version": "test", "environment": "test", "publication_gate": "human-approval-required", "authentication": "api-key-and-rbac"})


def session(route: Route) -> None:
    respond(route, {"subject": "publisher@example.invalid", "roles": ["publisher"], "permissions": ["read:intelligence", "approve:share", "export:reports"]})


def sharing_state(*, reviewer: str = "reviewer@example.invalid", approved: bool = True) -> dict[str, object]:
    return {
        "item_id": ITEM_ID,
        "title": "Canonical test intelligence",
        "source_id": "misp",
        "canonical_url": "https://example.invalid/intelligence/52",
        "review_status": "reviewed",
        "reviewed_by": reviewer,
        "share_approved": approved,
        "share_approved_by": "publisher@example.invalid" if approved else None,
        "misp_restrictions": {"restriction_authoritative": True, "distribution": "0", "sharing_group_id": None, "tlp_tags": ["tlp:amber"]},
        "misp_exports": [],
        "current_event_uuid": "event-52",
        "export_eligible": approved,
        "export_blockers": [] if approved else ["separate human share approval required"],
        "principal_actions": {"can_review": False, "can_approve_share": True},
        "misp_export_enabled": True,
        "misp_export_configured": True,
        "runtime_health_claim": False,
        "publication_authority": False,
        "synchronization_authority": False,
        "evidence_boundary": "Configuration does not prove live MISP health. Export grants no publication or synchronization authority.",
    }


@pytest.mark.browser
def test_workspace_exposes_governed_unpublished_export_boundary(page: Page) -> None:
    page.route("**/health", health)
    page.route("**/api/v1/ui/session", session)
    page.route(f"**/api/v1/sharing/items/{ITEM_ID}", lambda route: respond(route, sharing_state()))
    page.goto(f"{BASE_URL}/workbench/sharing?item={ITEM_ID}")

    expect(page.get_by_role("heading", name="Sharing & Exchange", level=1)).to_be_visible()
    expect(page.get_by_text("11.10g MISP Sharing · 11.10q recovery", exact=True)).to_be_visible()
    expect(page.get_by_text("Reviewed by reviewer@example.invalid", exact=True)).to_be_visible()
    expect(page.get_by_text("Approved by publisher@example.invalid", exact=True)).to_be_visible()
    expect(page.get_by_role("combobox", name="TLP")).to_have_value("tlp:amber")
    expect(page.get_by_role("button", name="Export approved intelligence")).to_be_enabled()
    expect(page.get_by_text("Runtime health: not inferred", exact=True)).to_be_visible()
    expect(page.get_by_text("Publication authority: no", exact=True)).to_be_visible()
    expect(page.get_by_text("Synchronization authority: no", exact=True)).to_be_visible()
    expect(page.get_by_role("button", name="Publish")).to_have_count(0)
    expect(page.get_by_role("button", name="Synchronize")).to_have_count(0)


@pytest.mark.browser
def test_reviewer_cannot_become_share_approver_in_same_session(page: Page) -> None:
    page.route("**/health", health)
    page.route("**/api/v1/ui/session", session)
    page.route(f"**/api/v1/sharing/items/{ITEM_ID}", lambda route: respond(route, sharing_state(reviewer="publisher@example.invalid", approved=False)))
    page.goto(f"{BASE_URL}/workbench/sharing?item={ITEM_ID}")

    expect(page.get_by_role("button", name="Approve sharing")).to_be_disabled()
    expect(page.get_by_text("This principal performed the review and therefore cannot approve sharing for the same item.", exact=True)).to_be_visible()
    expect(page.get_by_role("button", name="Export approved intelligence")).to_be_disabled()


@pytest.mark.browser
def test_sharing_state_failure_is_not_promoted_to_approval(page: Page) -> None:
    page.route("**/health", health)
    page.route("**/api/v1/ui/session", session)
    page.route(f"**/api/v1/sharing/items/{ITEM_ID}", lambda route: respond(route, {"detail": "sharing state unavailable"}, 503))
    page.goto(f"{BASE_URL}/workbench/sharing?item={ITEM_ID}")

    expect(page.get_by_text("Sharing state unavailable", exact=True)).to_be_visible()
    expect(page.get_by_text("No approval, export or MISP-health conclusion is inferred.", exact=False)).to_be_visible()
    expect(page.get_by_role("button", name="Export approved intelligence")).to_have_count(0)
