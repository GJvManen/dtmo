from __future__ import annotations

import json
import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import Page, Route, expect, sync_playwright

BASE_URL = os.getenv("DTMO_BROWSER_BASE_URL", "").rstrip("/")
ITEM_ID = "00000000-0000-0000-0000-000000000042"
MAPPING_ID = "00000000-0000-0000-0000-000000000142"


@pytest.fixture()
def page() -> Iterator[Page]:
    if not BASE_URL:
        pytest.skip("Phase 11.10f browser acceptance requires DTMO_BROWSER_BASE_URL")
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
    respond(route, {"subject": "analyst@example.invalid", "roles": ["analyst"], "permissions": ["read:intelligence"]})


def capabilities(route: Route) -> None:
    respond(route, {
        "enabled": True,
        "configured": True,
        "allowed_entity_types": ["indicator", "malware"],
        "runtime_health_claim": False,
        "upstream_relationship_topology_persisted": False,
        "external_share_authority": False,
        "local_compromise_proof": False,
    })


def graph(route: Route) -> None:
    respond(route, {
        "item_id": ITEM_ID,
        "title": "Education-sector ransomware campaign",
        "nodes": [
            {"id": f"dtmo:{ITEM_ID}", "kind": "canonical-intelligence", "label": "Education-sector ransomware campaign", "entity_type": "DTMO Intelligence", "stix_id": None, "confidence": 88, "markings": [], "last_seen_at": None},
            {"id": f"opencti:{MAPPING_ID}", "kind": "opencti-entity", "label": "indicator--abc", "entity_type": "Indicator", "stix_id": "indicator--abc", "confidence": 82, "markings": [{"definition": "TLP:AMBER"}], "last_seen_at": "2026-08-20T12:00:00Z"},
            {"id": "opencti:00000000-0000-0000-0000-000000000143", "kind": "opencti-entity", "label": "malware--xyz", "entity_type": "Malware", "stix_id": "malware--xyz", "confidence": 76, "markings": [], "last_seen_at": "2026-08-20T12:10:00Z"},
        ],
        "edges": [
            {"id": f"mapping:{MAPPING_ID}", "source": f"dtmo:{ITEM_ID}", "target": f"opencti:{MAPPING_ID}", "relationship_type": "canonical-mapping", "evidence_class": "persisted-dtmo-opencti-mapping"},
            {"id": "mapping:143", "source": f"dtmo:{ITEM_ID}", "target": "opencti:00000000-0000-0000-0000-000000000143", "relationship_type": "canonical-mapping", "evidence_class": "persisted-dtmo-opencti-mapping"},
        ],
        "topology_scope": "persisted canonical DTMO-to-OpenCTI mappings only",
        "upstream_relationship_topology_persisted": False,
        "evidence_boundary": "Only persisted DTMO-to-OpenCTI identity mappings are rendered as edges. Upstream entity-to-entity relationships must not be inferred. Graph presence does not prove local exposure, compromise or attribution.",
    })


def entity(route: Route) -> None:
    respond(route, {
        "mapping_id": MAPPING_ID,
        "item_id": ITEM_ID,
        "opencti_id": "opencti--internal-42",
        "stix_id": "indicator--abc",
        "entity_type": "Indicator",
        "parent_types": ["Stix-Core-Object"],
        "markings": [{"definition": "TLP:AMBER"}],
        "confidence": 82,
        "upstream_created_at": "2026-08-19T10:00:00Z",
        "upstream_updated_at": "2026-08-20T11:00:00Z",
        "external_references": [{"source_name": "CERT advisory", "external_id": "ADV-42"}],
        "provenance": {"system": "OpenCTI", "read_only": True},
        "snapshot_hash": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        "last_seen_at": "2026-08-20T12:00:00Z",
        "external_share_authorized": False,
        "local_compromise_proven": False,
        "revisions": [{"id": "00000000-0000-0000-0000-000000000242", "snapshot_hash": "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789", "recorded_at": "2026-08-20T12:00:00Z", "snapshot": {"confidence": 82}}],
        "evidence_boundary": "This is persisted OpenCTI-derived context. It is read-only, grants no publication/share authority and does not prove local exposure or compromise.",
    })


@pytest.mark.browser
def test_graph_workspace_renders_persisted_mapping_graph_and_entity_evidence(page: Page) -> None:
    page.route("**/api/v1/ui/session", session)
    page.route("**/api/v1/opencti/capabilities", capabilities)
    page.route(f"**/api/v1/opencti/items/{ITEM_ID}/graph", graph)
    page.route(f"**/api/v1/opencti/entities/{MAPPING_ID}", entity)

    page.goto(f"{BASE_URL}/workbench/intelligence/graph?item={ITEM_ID}")
    expect(page.get_by_role("heading", name="Knowledge Graph", level=1)).to_be_visible()
    expect(page.get_by_text("11.10f OpenCTI Graph", exact=True)).to_be_visible()
    expect(page.get_by_text("2 OpenCTI mappings", exact=True)).to_be_visible()
    expect(page.get_by_text("Relationship topology", exact=True)).to_be_visible()
    expect(page.get_by_text("not persisted", exact=True)).to_be_visible()
    expect(page.get_by_role("heading", name="Graph presence is context, not a verdict", level=2)).to_be_visible()

    page.get_by_role("button", name="Indicator").click()
    expect(page.get_by_role("heading", name="Indicator", level=2)).to_be_visible()
    expect(page.get_by_text("TLP:AMBER", exact=True)).to_be_visible()
    expect(page.get_by_text("not authorized", exact=True)).to_be_visible()
    expect(page.get_by_text("not proven", exact=True)).to_be_visible()
    expect(page.get_by_text("abcdef012345", exact=False)).to_be_visible()


@pytest.mark.browser
def test_graph_empty_state_does_not_claim_opencti_absence(page: Page) -> None:
    page.route("**/api/v1/ui/session", session)
    page.route("**/api/v1/opencti/capabilities", capabilities)
    page.route(f"**/api/v1/opencti/items/{ITEM_ID}/graph", lambda route: respond(route, {
        "item_id": ITEM_ID,
        "title": "Canonical item",
        "nodes": [{"id": f"dtmo:{ITEM_ID}", "kind": "canonical-intelligence", "label": "Canonical item", "entity_type": "DTMO Intelligence", "stix_id": None, "confidence": 50, "markings": [], "last_seen_at": None}],
        "edges": [],
        "topology_scope": "persisted canonical DTMO-to-OpenCTI mappings only",
        "upstream_relationship_topology_persisted": False,
        "evidence_boundary": "No inference beyond persisted mappings.",
    }))

    page.goto(f"{BASE_URL}/workbench/intelligence/graph?item={ITEM_ID}")
    expect(page.get_by_text("No persisted OpenCTI mapping context", exact=True)).to_be_visible()
    expect(page.get_by_text("not evidence that OpenCTI has no related knowledge", exact=False)).to_be_visible()


@pytest.mark.browser
def test_graph_dependency_failure_is_unavailable_not_empty(page: Page) -> None:
    page.route("**/api/v1/ui/session", session)
    page.route("**/api/v1/opencti/capabilities", capabilities)
    page.route(f"**/api/v1/opencti/items/{ITEM_ID}/graph", lambda route: respond(route, {"detail": "canonical backend unavailable"}, 503))

    page.goto(f"{BASE_URL}/workbench/intelligence/graph?item={ITEM_ID}")
    expect(page.get_by_text("Graph context unavailable", exact=True)).to_be_visible()
    expect(page.get_by_text("No persisted OpenCTI mapping context", exact=True)).not_to_be_visible()
