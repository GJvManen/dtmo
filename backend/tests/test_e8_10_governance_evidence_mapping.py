from pathlib import Path

from dtmo.governance_crosswalk import control_crosswalk


MAPPING = Path("docs/governance/E8_VULNERABILITY_CTI_EVIDENCE_MAPPING.md")


def test_e8_mapping_binds_sm07_to_completed_capabilities() -> None:
    text = MAPPING.read_text(encoding="utf-8")
    required = (
        "SM.07",
        "backend/dtmo/connectors/opencve.py",
        "backend/dtmo/connectors/vulnerability_lookup.py",
        "backend/dtmo/vulnerability_prioritization.py",
        "backend/dtmo/vulnerability_relevance.py",
        "backend/dtmo/vulnerability_analytics.py",
        "backend/dtmo/connectors/misp.py",
        "backend/dtmo/governance/misp_export.py",
        "backend/dtmo/connectors/ail.py",
        "backend/dtmo/ail_correlation.py",
        "backend/dtmo/ail_correlation_workspace.py",
    )
    for token in required:
        assert token in text


def test_e8_mapping_preserves_semantic_and_authority_boundaries() -> None:
    text = MAPPING.read_text(encoding="utf-8")
    for token in (
        "CVSS",
        "EPSS",
        "KEV",
        "MITRE ATT&CK",
        "MISP taxonomies, galaxies, TLP and distribution",
        "AIL",
        "DTMO provenance",
        "does not authorize redistribution",
        "No fuzzy attribution inference",
        "owner acceptance",
        "penetration-test acceptance",
    ):
        assert token in text


def test_existing_runtime_crosswalk_remains_primary_sm07_contract() -> None:
    payload = control_crosswalk()
    tvm = next(control for control in payload["controls"] if control["dtmo_control_id"] == "DTMO-TVM-01")
    normenkader = [mapping for mapping in tvm["mappings"] if mapping["framework_id"] == "normenkader-ibp"]
    assert any(mapping["object_id"] == "SM.07" and mapping["relationship"] == "supports" for mapping in normenkader)
    assert "do not constitute certification" in payload["claim_boundary"]


def test_all_referenced_repository_paths_exist() -> None:
    for path in (
        "backend/dtmo/connectors/opencve.py",
        "backend/dtmo/connectors/vulnerability_lookup.py",
        "backend/dtmo/vulnerability_prioritization.py",
        "backend/dtmo/vulnerability_relevance.py",
        "backend/dtmo/vulnerability_analytics.py",
        "backend/dtmo/connectors/misp.py",
        "backend/dtmo/governance/misp_export.py",
        "backend/dtmo/connectors/ail.py",
        "backend/dtmo/ail_correlation.py",
        "backend/dtmo/ail_correlation_workspace.py",
    ):
        assert Path(path).exists(), path
