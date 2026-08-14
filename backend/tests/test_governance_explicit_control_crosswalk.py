from __future__ import annotations

from dtmo.governance_crosswalk import control_crosswalk, router as crosswalk_router
from dtmo.governance_crosswalk_experience import _PAGE, _SCRIPT, router as experience_router


def test_crosswalk_contains_explicit_framework_relationships() -> None:
    payload = control_crosswalk()
    assert payload["status"] == "repository_backed_explicit_partial_crosswalk"
    assert payload["verified_on"] == "2026-08-14"
    assert payload["mapping_count"] >= 10
    counts = payload["mapping_count_by_framework"]
    assert counts["normenkader-ibp"] >= 6
    assert counts["mitre-attack"] >= 2
    assert counts["nist-csf"] >= 4
    assert counts["cvss"] >= 1


def test_crosswalk_includes_high_value_normenkader_controls() -> None:
    payload = control_crosswalk()
    mappings = [mapping for control in payload["controls"] for mapping in control["mappings"]]
    norm_ids = {mapping["object_id"] for mapping in mappings if mapping["framework_id"] == "normenkader-ibp"}
    assert {"ID.02", "ID.05", "SM.02", "SM.04", "SM.07", "SM.11", "OP.02", "BC.03", "GO.03"} <= norm_ids


def test_crosswalk_does_not_claim_full_compliance_or_equivalence() -> None:
    payload = control_crosswalk()
    boundary = str(payload["claim_boundary"]).lower()
    assert "do not constitute certification" in boundary
    assert "full compliance" in boundary
    relationships = {
        mapping["relationship"]
        for control in payload["controls"]
        for mapping in control["mappings"]
    }
    assert "supports" in relationships
    assert "partial-support" in relationships
    assert "context-only" in relationships
    assert "detection-and-mitigation-context" in relationships


def test_crosswalk_api_and_canonical_governance_ui_are_exposed() -> None:
    assert "/api/v1/governance/control-crosswalk" in {route.path for route in crosswalk_router.routes}
    assert 'id="governance-crosswalk"' in _PAGE
    assert "Uitgewerkte kaders & expliciete DTMO-mappings" in _PAGE
    assert "/api/v1/governance/control-crosswalk" in _SCRIPT
    assert "Normenkader IBP" in _SCRIPT
    assert "MITRE ATT&CK" in _SCRIPT
    assert "NIST CSF" in _SCRIPT
    assert "CVSS" in _SCRIPT
    routes = [route for route in experience_router.routes if route.path in {"/", "/ui/console"}]
    assert {route.path for route in routes} == {"/", "/ui/console"}
