from tools.phase11_production_equivalent_validation import build_contract


def test_phase11_10_requires_fresh_candidate_bound_evidence() -> None:
    contract = build_contract()
    assert contract["phase"] == "11.10"
    assert contract["status"] == "IN_PROGRESS"
    assert contract["historical_phase8_evidence_reusable"] is False
    assert contract["fresh_candidate_bound_evidence_required"] is True
    assert contract["missing_or_ambiguous_evidence"] == "FAIL_CLOSED"
    assert contract["production_authorized"] is False


def test_phase11_10_requires_complete_integrated_evidence_set() -> None:
    contract = build_contract()
    required = set(contract["required_evidence_classes"])
    assert required == {
        "immutable_candidate_identity",
        "migration_compatibility",
        "upgrade",
        "rollback",
        "health",
        "saturation",
        "recovery",
    }
    assert contract["same_candidate_required_for_phase11_11"] is True
