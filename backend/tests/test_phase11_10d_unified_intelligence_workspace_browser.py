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
        pytest.skip("Phase 11.10d browser acceptance requires DTMO_BROWSER_BASE_URL")
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
    route.fulfill(status=status, content_type="application/json", body=json.dumps(payload))


def _session(route: Route) -> None:
    _json(
        route,
        {
            "subject": "analyst@example.invalid",
            "roles": ["analyst"],
            "permissions": ["read:intelligence"],
        },
    )


@pytest.mark.browser
def test_unified_intelligence_search_selects_canonical_detail_and_provenance(page: Page) -> None:
    page.route("**/api/v1/ui/session", _session)
    page.route(
        "**/api/v1/intelligence/search?**",
        lambda route: _json(
            route,
            {
                "query": "ransomware",
                "count": 1,
                "results": [
                    {
                        "id": ITEM_ID,
                        "title": "Education ransomware campaign activity",
                        "summary": "Campaign reporting with education-sector relevance.",
                        "item_type": "article",
                        "source_id": "trusted-feed",
                        "severity": "high",
                        "confidence_score": 87,
                        "confidence_level": "high",
                        "education_relevance": 93,
                        "published_at": "2026-08-20T12:00:00+00:00",
                        "canonical_url": "https://example.invalid/advisory",
                        "tags": ["ransomware", "education"],
                    }
                ],
            },
        ),
    )
    page.route(
        f"**/api/v1/intelligence/{ITEM_ID}/workspace",
        lambda route: _json(
            route,
            {
                "id": ITEM_ID,
                "source_id": "trusted-feed",
                "external_id": "advisory-42",
                "item_type": "article",
                "title": "Education ransomware campaign activity",
                "summary": "Campaign reporting with education-sector relevance.",
                "canonical_url": "https://example.invalid/advisory",
                "published_at": "2026-08-20T12:00:00+00:00",
                "discovered_at": "2026-08-20T12:05:00+00:00",
                "severity": "high",
                "confidence_score": 87,
                "confidence_level": "high",
                "confidence_rationale": "Corroborated primary reporting and validated source lineage.",
                "education_relevance": 93,
                "review_status": "candidate",
                "share_approved": False,
                "tags": ["ransomware", "education"],
                "context": {
                    "cve_ids": ["CVE-2026-4242"],
                    "known_exploited": True,
                    "vendor": "Example Vendor",
                    "product": "Example Product",
                },
                "provenance": [
                    {
                        "source_url": "https://example.invalid/advisory",
                        "source_title": "Primary advisory",
                        "publisher": "Example CERT",
                        "retrieved_at": "2026-08-20T12:04:00+00:00",
                        "source_reliability": "A",
                        "is_primary_source": True,
                        "content_integrity_verified": True,
                        "confidence_score": 95,
                    }
                ],
            },
        ),
    )

    page.goto(f"{BASE_URL}/workbench/intelligence")
    expect(page.get_by_role("heading", name="Threat Intelligence", level=1)).to_be_visible()
    expect(page.get_by_text("Canonical data · no synthetic results", exact=True)).to_be_visible()
    expect(page.get_by_text("Recent intelligence is read from canonical DTMO persistence.", exact=False)).to_be_visible()
    page.get_by_label("Search canonical intelligence").fill("ransomware")
    page.get_by_label("Severity").select_option("high")
    page.get_by_label("Minimum education relevance").fill("80")
    page.get_by_role("button", name="Search intelligence").click()

    expect(page.get_by_text("Education ransomware campaign activity").first).to_be_visible()
    page.get_by_role("button", name="Open Education ransomware campaign activity").click()
    expect(page.get_by_role("heading", name="Education ransomware campaign activity", level=3)).to_be_visible()
    expect(page.get_by_text("candidate", exact=True)).to_be_visible()
    expect(page.get_by_text("Not approved for sharing", exact=True)).to_be_visible()
    expect(page.get_by_text("CVE-2026-4242", exact=True)).to_be_visible()
    expect(page.get_by_role("heading", name="Provenance chain", level=4)).to_be_visible()
    expect(page.get_by_text("Primary advisory", exact=True)).to_be_visible()
    expect(page.get_by_role("heading", name="Canonical recent view without fabricated content", level=2)).to_be_visible()
    expect(page.get_by_text("Search remains a separate governed projection.", exact=False)).to_be_visible()


@pytest.mark.browser
def test_unified_intelligence_fails_closed_when_search_dependency_is_unavailable(page: Page) -> None:
    page.route("**/api/v1/ui/session", _session)
    page.route(
        "**/api/v1/intelligence/search?**",
        lambda route: _json(route, {"detail": "search backend unavailable: RuntimeError"}, status=503),
    )

    page.goto(f"{BASE_URL}/workbench/intelligence")
    page.get_by_label("Search canonical intelligence").fill("malware")
    page.get_by_role("button", name="Search intelligence").click()
    expect(page.get_by_text("Intelligence discovery unavailable", exact=True)).to_be_visible()
    expect(page.get_by_text("search backend unavailable: RuntimeError", exact=False)).to_be_visible()
    expect(page.get_by_text("No intelligence matched this query", exact=True)).to_have_count(0)


@pytest.mark.browser
def test_ioc_explorer_lists_persisted_observables_filters_and_pivots(page: Page) -> None:
    page.route("**/api/v1/ui/session", _session)
    page.route(
        "**/api/v1/iocs?**",
        lambda route: _json(
            route,
            {
                "records": [
                    {
                        "record_id": "00000000-0000-0000-0000-000000000099",
                        "item_id": ITEM_ID,
                        "item_title": "Education ransomware campaign activity",
                        "source_id": "trusted-feed",
                        "severity": "high",
                        "confidence_score": 87,
                        "observable_type": "domain",
                        "observable_value": "malicious.example",
                        "handling": "tlp:amber",
                        "status": "reported_without_inference",
                        "analyzers": ["dns"],
                        "created_at": "2026-08-20T12:10:00+00:00",
                        "external_share_authorized": False,
                        "local_compromise_proven": False,
                    }
                ],
                "evidence_boundary": "Persisted governed observables only; no maliciousness or compromise verdict.",
            },
        ),
    )

    page.goto(f"{BASE_URL}/workbench/intelligence/iocs")
    expect(page.get_by_role("heading", name="IOC Explorer", level=1)).to_be_visible()
    expect(page.get_by_text("Canonical IOC inventory", exact=True)).to_be_visible()
    expect(page.get_by_text("No text-derived or synthetic IOCs", exact=True)).to_be_visible()
    expect(page.get_by_text("malicious.example", exact=True)).to_be_visible()
    page.get_by_label("Type").select_option("domain")
    page.get_by_label("Severity").select_option("high")
    page.get_by_label("Minimum confidence").fill("80")
    expect(page.get_by_text("malicious.example", exact=True)).to_be_visible()
    expect(page.get_by_role("link", name="Enrich / analyze", exact=True)).to_have_attribute("href", f"/workbench/analysis?item={ITEM_ID}")
    expect(page.get_by_role("link", name="Graph", exact=True)).to_have_attribute("href", f"/workbench/intelligence/graph?item={ITEM_ID}")
    expect(page.get_by_role("link", name="Investigate", exact=True)).to_have_attribute("href", f"/workbench/investigations?item={ITEM_ID}")
