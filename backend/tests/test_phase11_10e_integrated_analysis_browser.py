from __future__ import annotations

import json
import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import Page, Route, expect, sync_playwright

BASE_URL = os.getenv("DTMO_BROWSER_BASE_URL", "").rstrip("/")
ITEM_ID = "00000000-0000-0000-0000-000000000042"


@pytest.fixture()
def page() -> Iterator[Page]:
    if not BASE_URL:
        pytest.skip("Phase 11.10e browser acceptance requires DTMO_BROWSER_BASE_URL")
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


def session(route: Route) -> None:
    respond(route, {"subject": "senior@example.invalid", "roles": ["senior_analyst"], "permissions": ["read:intelligence", "review:intelligence"]})


def capabilities(route: Route) -> None:
    respond(
        route,
        {
            "intelowl_enabled": True,
            "intelowl_observable_types": ["domain", "ip"],
            "intelowl_analyzers": ["DNSResolver", "Reputation"],
            "cortex_enabled": True,
            "cortex_observable_types": ["domain", "ip"],
            "cortex_analyzers": ["CortexDomainAnalyzer"],
            "runtime_health_claim": False,
            "responder_actions_allowed": False,
            "external_share_authority": False,
            "local_compromise_proof": False,
        },
    )


def history(route: Route) -> None:
    respond(
        route,
        {
            "item_id": ITEM_ID,
            "intelowl": {
                "records": [
                    {
                        "record_id": "00000000-0000-0000-0000-000000000101",
                        "item_id": ITEM_ID,
                        "job_id": "intelowl-42",
                        "status": "success",
                        "partial": False,
                        "analyzers": ["DNSResolver"],
                        "external_share_authorized": False,
                        "local_compromise_proven": False,
                    }
                ]
            },
            "cortex": {
                "records": [
                    {
                        "record_id": "00000000-0000-0000-0000-000000000102",
                        "item_id": ITEM_ID,
                        "job_id": "cortex-42",
                        "status": "success",
                        "analyzer_id": "CortexDomainAnalyzer",
                        "tlp": 2,
                        "report": {"summary": "bounded test result"},
                        "external_share_authorized": False,
                        "local_compromise_proven": False,
                    }
                ]
            },
            "evidence_boundary": "IntelOwl and Cortex outputs are enrichment evidence only. They do not authorize external sharing, do not prove local compromise by themselves, and do not establish live upstream health.",
        },
    )


@pytest.mark.browser
def test_integrated_analysis_renders_both_persisted_evidence_streams(page: Page) -> None:
    page.route("**/api/v1/ui/session", session)
    page.route("**/api/v1/analysis/capabilities", capabilities)
    page.route(f"**/api/v1/analysis/items/{ITEM_ID}/history", history)

    page.goto(f"{BASE_URL}/workbench/analysis?item={ITEM_ID}")
    expect(page.get_by_role("heading", name="Analysis & Enrichment", level=1)).to_be_visible()
    expect(page.get_by_text("11.10e Integrated Analysis", exact=False)).to_be_visible()
    expect(page.get_by_text("11.10q recovery", exact=False)).to_be_visible()
    expect(page.get_by_role("heading", name="IntelOwl history", level=2)).to_be_visible()
    expect(page.get_by_text("intelowl-42", exact=False)).to_be_visible()
    expect(page.get_by_role("heading", name="Cortex history", level=2)).to_be_visible()
    expect(page.get_by_text("cortex-42", exact=False)).to_be_visible()
    expect(page.get_by_role("heading", name="Enrichment is evidence, not a verdict", level=2)).to_be_visible()
    expect(page.get_by_text("No responder authority", exact=True)).to_be_visible()


@pytest.mark.browser
def test_read_only_principal_cannot_present_execution_as_authorized(page: Page) -> None:
    page.route("**/api/v1/ui/session", lambda route: respond(route, {"subject": "auditor@example.invalid", "roles": ["auditor"], "permissions": ["read:intelligence"]}))
    page.route("**/api/v1/analysis/capabilities", capabilities)
    page.goto(f"{BASE_URL}/workbench/analysis")

    expect(page.get_by_text("Read-only principal", exact=True)).to_be_visible()
    expect(page.get_by_role("button", name="Run IntelOwl")).to_be_disabled()
    expect(page.get_by_role("button", name="Run Cortex")).to_be_disabled()
