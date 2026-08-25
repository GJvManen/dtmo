from __future__ import annotations

import json
import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import Page, Route, expect, sync_playwright

BASE_URL = os.getenv("DTMO_BROWSER_BASE_URL", "").rstrip("/")


@pytest.fixture()
def page() -> Iterator[Page]:
    if not BASE_URL:
        pytest.skip("Phase 11.10c browser acceptance requires DTMO_BROWSER_BASE_URL")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            browser.close()


def _json(route: Route, payload: object, status: int = 200) -> None:
    route.fulfill(
        status=status,
        content_type="application/json",
        body=json.dumps(payload),
    )


@pytest.mark.browser
def test_command_center_renders_canonical_operational_snapshot(page: Page) -> None:
    page.route(
        "**/api/v1/ui/session",
        lambda route: _json(
            route,
            {
                "subject": "analyst@example.invalid",
                "roles": ["admin"],
                "permissions": [
                    "read:intelligence",
                    "review:intelligence",
                    "manage:connectors",
                    "handoff:case",
                    "approve:share",
                    "manage:users",
                ],
            },
        ),
    )
    page.route(
        "**/api/v1/command-center",
        lambda route: _json(
            route,
            {
                "generated_at": "2026-08-20T12:00:00+00:00",
                "data_state": "available",
                "metrics": [
                    {"id": "intelligence-total", "label": "Intelligence objects", "value": 247, "tone": "neutral"},
                    {"id": "high-priority", "label": "High / critical", "value": 18, "tone": "critical"},
                    {"id": "new-24h", "label": "New in 24h", "value": 31, "tone": "accent"},
                    {"id": "pending-review", "label": "Pending review", "value": 7, "tone": "warning"},
                    {"id": "share-approvals", "label": "Share approvals", "value": 3, "tone": "warning"},
                    {"id": "education-relevant", "label": "Education relevance ≥80", "value": 54, "tone": "accent"},
                ],
                "recent_intelligence": [
                    {
                        "id": "00000000-0000-0000-0000-000000000001",
                        "title": "High-impact vulnerability activity",
                        "source_id": "cisa-kev",
                        "severity": "high",
                        "education_relevance": 94,
                        "review_status": "candidate",
                        "discovered_at": "2026-08-20T11:55:00+00:00",
                    }
                ],
                "trends": {
                    "intelligence_7d": [
                        {"date": "2026-08-14", "count": 8},
                        {"date": "2026-08-15", "count": 12},
                        {"date": "2026-08-16", "count": 7},
                        {"date": "2026-08-17", "count": 19},
                        {"date": "2026-08-18", "count": 16},
                        {"date": "2026-08-19", "count": 23},
                        {"date": "2026-08-20", "count": 31},
                    ],
                    "severity_distribution": [
                        {"severity": "critical", "count": 4},
                        {"severity": "high", "count": 14},
                        {"severity": "medium", "count": 63},
                        {"severity": "low", "count": 91},
                        {"severity": "informational", "count": 75},
                    ],
                },
                "integrations": [
                    {"id": "taranis", "label": "Taranis", "state": "enabled", "enabled": True, "configured": True, "scheduled_collection": True, "runtime_observation": "completed", "last_observed_at": "2026-08-20T11:58:00+00:00", "runtime_health_claim": False},
                    {"id": "intelowl", "label": "IntelOwl", "state": "enabled", "enabled": True, "configured": True, "scheduled_collection": False, "runtime_observation": None, "last_observed_at": None, "runtime_health_claim": False},
                    {"id": "opencti", "label": "OpenCTI", "state": "enabled", "enabled": True, "configured": True, "scheduled_collection": False, "runtime_observation": None, "last_observed_at": None, "runtime_health_claim": False},
                    {"id": "misp", "label": "MISP", "state": "enabled", "enabled": True, "configured": True, "scheduled_collection": True, "runtime_observation": "completed", "last_observed_at": "2026-08-20T11:50:00+00:00", "runtime_health_claim": False},
                    {"id": "thehive", "label": "TheHive", "state": "disabled", "enabled": False, "configured": False, "scheduled_collection": False, "runtime_observation": None, "last_observed_at": None, "runtime_health_claim": False},
                    {"id": "cortex", "label": "Cortex", "state": "configuration-required", "enabled": True, "configured": False, "scheduled_collection": False, "runtime_observation": None, "last_observed_at": None, "runtime_health_claim": False},
                ],
                "evidence_boundary": "Command Center values and trends are canonical DTMO read models; no runtime health is inferred.",
            },
        ),
    )

    page.goto(f"{BASE_URL}/workbench/command-center")
    expect(page.get_by_role("heading", name="Command Center", level=1)).to_be_visible()
    expect(page.get_by_text("247", exact=True)).to_be_visible()
    expect(page.get_by_text("18", exact=True).first).to_be_visible()
    expect(page.get_by_text("High-impact vulnerability activity")).to_be_visible()
    expect(page.get_by_text("Taranis", exact=True)).to_be_visible()
    expect(page.get_by_role("heading", name="Intelligence arrivals · 7 days")).to_be_visible()
    expect(page.get_by_role("heading", name="Severity composition")).to_be_visible()
    expect(page.get_by_text("31", exact=True).last).to_be_visible()
    expect(page.get_by_text("1 configuration required · 2 runtime observed", exact=True)).to_be_visible()
    expect(page.get_by_role("link", name="Configure")).to_be_visible()
    expect(page.get_by_role("link", name="Collection control")).to_be_visible()
    expect(page.get_by_role("link", name="Sharing approvals")).to_be_visible()


@pytest.mark.browser
def test_command_center_fails_closed_when_canonical_data_is_unavailable(page: Page) -> None:
    page.route(
        "**/api/v1/ui/session",
        lambda route: _json(route, {"subject": "auditor@example.invalid", "roles": ["auditor"], "permissions": ["read:intelligence", "read:audit"]}),
    )
    page.route(
        "**/api/v1/command-center",
        lambda route: _json(
            route,
            {
                "generated_at": "2026-08-20T12:00:00+00:00",
                "data_state": "unavailable",
                "metrics": [
                    {"id": name, "label": label, "value": None, "tone": "neutral"}
                    for name, label in [
                        ("intelligence-total", "Intelligence objects"),
                        ("high-priority", "High / critical"),
                        ("new-24h", "New in 24h"),
                        ("pending-review", "Pending review"),
                        ("share-approvals", "Share approvals"),
                        ("education-relevant", "Education relevance ≥80"),
                    ]
                ],
                "recent_intelligence": [],
                "trends": {"intelligence_7d": [], "severity_distribution": []},
                "integrations": [],
                "evidence_boundary": "Missing evidence is unavailable rather than synthesized.",
            },
        ),
    )

    page.goto(f"{BASE_URL}/workbench/command-center")
    expect(page.get_by_text("Canonical data unavailable", exact=True)).to_be_visible()
    expect(page.get_by_text("Canonical store unavailable", exact=True)).to_be_visible()
    expect(page.get_by_text("Trend unavailable while canonical intelligence cannot be observed.", exact=True)).to_be_visible()
    expect(page.get_by_text("Severity distribution unavailable.", exact=True)).to_be_visible()
    expect(page.get_by_text("No attributable value").first).to_be_visible()
    expect(page.get_by_text("0", exact=True)).to_have_count(0)
