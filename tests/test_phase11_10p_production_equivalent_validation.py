from pathlib import Path

CONTRACT = Path("docs/architecture/PHASE11_10P_PRODUCTION_EQUIVALENT_VALIDATION.md")


def test_phase11_10p_contract_freezes_one_candidate_and_preserves_evidence_boundaries():
    text = CONTRACT.read_text(encoding="utf-8")
    required = [
        "Phase 11.10p — Production-Equivalent Validation",
        "one immutable candidate",
        "exact candidate SHA",
        "deployment and startup on a production-equivalent topology",
        "migration and compatibility checks",
        "upgrade execution and rollback execution",
        "health/readiness",
        "load, saturation and degraded-dependency behavior",
        "recovery and restart behavior",
        "fail-closed handling",
        "Repository CI can validate deterministic contracts and automation, but repository CI does not prove production-equivalent operation by itself",
        "Historical Phase 8/9 evidence remains audit history only",
        "No synthetic screenshot, fixture-only browser state, stale artifact or evidence from another candidate SHA",
        "does not itself grant production authorization, owner acceptance or independent assurance",
        "completed/success",
        "expected-head protection",
    ]
    for marker in required:
        assert marker in text


def test_phase11_10p_candidate_is_derived_from_accepted_11_10o_main():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "b4ceeccac390cab10b81a215004e061e518c3928" in text
