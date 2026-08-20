from __future__ import annotations

import json
import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import Page, Route, expect, sync_playwright

BASE_URL = os.getenv("DTMO_BROWSER_BASE_URL", "").rstrip("/")
ITEM_ID = "00000000-0000-0000-0000-000000000061"


@pytest.fixture()
def page() -> Iterator[Page]:
    if not BASE_URL:
        pytest.skip("Phase 11.10h browser acceptance requires DTMO_BROWSER_BASE_URL")
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
    respond(route, {"subject": "analyst@example.invalid", "roles": ["senior_analyst"], "permissions": ["read:intelligence", "handoff:case"]})


def investigation_state(*, history: list[dict[str, object]] | None = None, blockers: list[str] | None = None) -> dict[str, object]:
    return {
        "item_id": ITEM_ID,
        "title": "Suspicious education-sector activity",
        "source_id": "analyst",
        "canonical_url": "https://example.invalid/intelligence/61",
        "severity": "high",
        "review_status": "reviewed",
        "provenance_count": 2,
        "authoritative_tlp_tags": ["tlp:amber"],
        "handoff_history": history or [],
        "handoff_blockers": blockers or [],
        "principal_actions": {"can_handoff": True},
        "feature_enabled": True,
        "configured": True,
        "runtime_health_claim": False,
        "upstream_case_readback_supported": False,
        "alerts_tasks_timeline_persisted": False,
        "external_share_authority": False,
        "local_compromise_proof": False,
        "evidence_boundary": "Configuration does not prove live TheHive health. Case handoff evidence does not prove local compromise or upstream case completeness.",
    }


@pytest.mark.browser
def test_workspace_creates_explicit_human_case_handoff_and_reloads_evidence(page: Page) -> None:
    history: list[dict[str, object]] = []
    captured: dict[str, object] = {}

    def state_route(route: Route) -> None:
        respond(route, investigation_state(history=history))

    def create_route(route: Route) -> None:
        payload = route.request.post_data_json
        assert isinstance(payload, dict)
        captured.update(payload)
        record = {
            "handoff_id": "handoff-61",
            "request_id": payload["request_id"],
            "status": "delivered",
            "requested_by": "analyst@example.invalid",
            "organization": "school-cert",
            "tlp": payload["tlp"],
            "pap": payload["pap"],
            "thehive_case_id": "case-61",
            "thehive_case_number": "61",
            "error_detail": None,
            "created_at": "2026-08-20T19:00:00+00:00",
            "updated_at": "2026-08-20T19:00:00+00:00",
            "external_share_authorized": False,
            "local_compromise_proven": False,
        }
        history.append(record)
        respond(route, {"handoff_id": "handoff-61", "request_id": payload["request_id"], "item_id": ITEM_ID, "status": "delivered", "organization": "school-cert", "thehive_case_id": "case-61", "thehive_case_number": "61", "external_share_authorized": False, "local_compromise_proven": False}, 201)

    page.route("**/health", health)
    page.route("**/api/v1/ui/session", session)
    page.route(f"**/api/v1/thehive/items/{ITEM_ID}/investigation", state_route)
    page.route(f"**/api/v1/thehive/items/{ITEM_ID}/cases", create_route)
    page.goto(f"{BASE_URL}/workbench/investigations?item={ITEM_ID}")

    expect(page.get_by_role("heading", name="Investigations", level=1)).to_be_visible()
    expect(page.get_by_text("11.10h TheHive Investigations", exact=True)).to_be_visible()
    expect(page.get_by_text("Suspicious education-sector activity", exact=True)).to_be_visible()
    expect(page.get_by_text("Runtime health: not inferred", exact=True)).to_be_visible()
    expect(page.get_by_text("External share authority: no", exact=True)).to_be_visible()
    expect(page.get_by_text("Local compromise proof: no", exact=True)).to_be_visible()

    page.get_by_label("Reviewed case summary").fill("Reviewed evidence for explicit human case handoff")
    page.get_by_role("button", name="Create TheHive case handoff").click()

    expect(page.get_by_text("TheHive case handoff delivered as case #61.", exact=True)).to_be_visible()
    expect(page.get_by_text("TheHive case #61", exact=True)).to_be_visible()
    assert captured["summary"] == "Reviewed evidence for explicit human case handoff"
    assert captured["tlp"] == "amber"
    assert captured["pap"] == "amber"
    assert isinstance(captured["request_id"], str) and captured["request_id"]


@pytest.mark.browser
def test_ambiguous_handoff_requires_manual_reconciliation_and_blocks_new_case(page: Page) -> None:
    ambiguous = {
        "handoff_id": "handoff-ambiguous",
        "request_id": "00000000-0000-0000-0000-000000000099",
        "status": "ambiguous",
        "requested_by": "analyst@example.invalid",
        "organization": "school-cert",
        "tlp": "amber",
        "pap": "amber",
        "thehive_case_id": None,
        "thehive_case_number": None,
        "error_detail": "delivery ambiguous; manual reconciliation required",
        "created_at": "2026-08-20T19:00:00+00:00",
        "updated_at": "2026-08-20T19:00:00+00:00",
        "external_share_authorized": False,
        "local_compromise_proven": False,
    }
    page.route("**/health", health)
    page.route("**/api/v1/ui/session", session)
    page.route(f"**/api/v1/thehive/items/{ITEM_ID}/investigation", lambda route: respond(route, investigation_state(history=[ambiguous])))
    page.goto(f"{BASE_URL}/workbench/investigations?item={ITEM_ID}")

    expect(page.get_by_text("Manual reconciliation required", exact=True)).to_be_visible()
    page.get_by_label("Reviewed case summary").fill("A blind retry must not be possible")
    expect(page.get_by_role("button", name="Create TheHive case handoff")).to_be_disabled()
    expect(page.get_by_text("Case identity not confirmed", exact=True)).to_be_visible()


@pytest.mark.browser
def test_investigation_failure_is_not_promoted_to_case_or_health_evidence(page: Page) -> None:
    page.route("**/health", health)
    page.route("**/api/v1/ui/session", session)
    page.route(f"**/api/v1/thehive/items/{ITEM_ID}/investigation", lambda route: respond(route, {"detail": "canonical investigation state unavailable"}, 503))
    page.goto(f"{BASE_URL}/workbench/investigations?item={ITEM_ID}")

    expect(page.get_by_text("Investigation state unavailable", exact=True)).to_be_visible()
    expect(page.get_by_text("No case, TheHive-health or compromise conclusion is inferred.", exact=False)).to_be_visible()
    expect(page.get_by_role("button", name="Create TheHive case handoff")).to_have_count(0)
