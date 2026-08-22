from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/assurance/PHASE11_11_INDEPENDENT_EXTERNAL_ASSURANCE.md"


def test_phase11_11_contract_preserves_candidate_and_external_authority_boundaries():
    text = CONTRACT.read_text(encoding="utf-8")
    required = [
        "17e31a839a16a250a94b00a67b3ddd0a8c88fbbf",
        "IN PROGRESS / EXTERNAL EVIDENCE REQUIRED",
        "independent tester/assessor identity",
        "exact candidate SHA/release identity",
        "authentication, authorization and role-boundary assessment",
        "findings with severity",
        "retest evidence",
        "residual-risk statement",
        "Historical Phase 8/9 assurance remains audit history only",
        "does not establish independent external assurance",
        "must fail closed",
        "PASS / EXTERNAL_ASSURANCE_ACCEPTED",
        "Phase 12 formal production GO/NO-GO must not begin before Phase 11.11 is accepted",
    ]
    for marker in required:
        assert marker in text


def test_phase11_11_does_not_claim_external_execution_from_repository_ci():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Repository CI can validate this contract and evidence structure, but cannot substitute for independent external execution or acceptance." in text
    assert "A successful repository workflow does not establish that an external test occurred" in text
