from __future__ import annotations

from dtmo.e8_governance_evidence import router, vulnerability_evidence_mapping


def test_e8_evidence_maps_vulnerability_lifecycle_to_sm07() -> None:
    payload = vulnerability_evidence_mapping()
    assert payload["status"] == "repository_backed_explicit_evidence_mapping"
    assert payload["primary_control"] == "SM.07"
    assert "SM.04" in payload["supporting_controls"]
    mappings = payload["mappings"]
    assert len(mappings) >= 6
    assert all("SM.07" in item["normenkader"] for item in mappings)


def test_e8_evidence_preserves_semantic_boundaries() -> None:
    semantics = vulnerability_evidence_mapping()["semantic_boundaries"]
    assert semantics["CVSS"] == "vulnerability severity"
    assert "probability" in semantics["EPSS"]
    assert "known-exploited" in semantics["KEV"]
    assert "adversary behavior" in semantics["MITRE ATT&CK"]
    assert "sharing constraints" in semantics["MISP taxonomy/TLP/distribution"]
    assert "investigative" in semantics["AIL"]


def test_e8_evidence_has_repository_refs_and_truthful_boundaries() -> None:
    payload = vulnerability_evidence_mapping()
    for mapping in payload["mappings"]:
        assert mapping["evidence_refs"]
        assert mapping["boundary"]
    boundary = payload["claim_boundary"].lower()
    for prohibited_claim in ("compliance", "certification", "exposure", "compromise", "remediation-completion", "external-acceptance"):
        assert prohibited_claim in boundary


def test_e8_evidence_api_is_registered_on_router() -> None:
    assert "/api/v1/governance/vulnerability-evidence-mapping" in {route.path for route in router.routes}
