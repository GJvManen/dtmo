from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "architecture" / "PHASE11_10O_CONSOLIDATION_FULL_FUNCTIONAL_ACCEPTANCE.md"


def test_phase11_10o_contract_exists_and_preserves_acceptance_boundaries():
    text = CONTRACT.read_text(encoding="utf-8")
    required = [
        "Phase 11.10o — Consolidation & Full Functional Acceptance",
        "browser -> DTMO same-origin API -> server-side policy/authority",
        "Browser visibility is never authority",
        "role-aware read-only, disabled, unavailable and authorized states",
        "fail-closed handling",
        "Historical Phase 8/9 evidence remains audit history only",
        "No synthetic screenshot or fixture-only browser state may be promoted",
        "completed/success",
        "expected-head protection",
        "Phase 11.10p production-equivalent validation",
        "freeze one immutable candidate",
    ]
    for marker in required:
        assert marker in text


def test_phase11_10o_does_not_claim_repository_ci_is_production_proof():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "does not prove staging or production behavior" in text
    assert "does not establish production-equivalent operation" in text
    assert "production authorization" in text
