from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/phase11-10q-same-origin-browser-acceptance.yml"
MATRIX = ROOT / "docs/qa/CANONICAL_FUNCTIONAL_BROWSER_MATRIX.md"
READINESS = ROOT / "docs/qa/WHOLE_PRODUCT_OWNER_RETEST_READINESS.md"


def test_composed_same_origin_gate_includes_all_deep_recovery_journeys() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    required_tests = (
        "test_phase11_10q_same_origin_browser_acceptance.py",
        "test_owner_functional_recovery_browser_matrix.py",
        "test_owner_functional_recovery_threat_intelligence.py",
        "test_owner_functional_recovery_ioc_explorer.py",
        "test_owner_functional_recovery_knowledge_graph.py",
        "test_owner_functional_recovery_exposure.py",
        "test_owner_functional_recovery_investigations.py",
        "test_owner_functional_recovery_analysis.py",
        "test_owner_functional_recovery_governance.py",
        "test_owner_functional_recovery_operations.py",
    )
    for filename in required_tests:
        assert filename in text

    for marker in (
        "route_interception\": False",
        "same_origin_http\": True",
        "governance_deep_evidence_included\": True",
        "operations_runtime_evidence_included\": True",
        "owner_functional_acceptance\": False",
        "clean_external_installation_evidence\": False",
    ):
        assert marker in text


def test_browser_matrix_covers_every_owner_rejected_canonical_surface() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    for heading in (
        "Command Center",
        "Threat Intelligence",
        "IOC Explorer",
        "Knowledge Graph",
        "Vulnerability & Exposure Center",
        "Investigations",
        "Analysis & Enrichment",
        "Sharing & Exchange",
        "Automation & Playbooks",
        "Sources & Collection",
        "Governance & Evidence",
        "Operations",
        "Administration",
    ):
        assert heading in text
    assert "whole-product owner retest" in text.lower()


def test_retest_readiness_document_fails_closed_on_external_acceptance_boundary() -> None:
    text = READINESS.read_text(encoding="utf-8").lower()
    for marker in (
        "clean supported installation",
        "external owner retest",
        "does not constitute owner acceptance",
        "candidate freeze remains blocked",
        "production-equivalent validation remains blocked",
        "no `/ui/*` compatibility route",
    ):
        assert marker in text
