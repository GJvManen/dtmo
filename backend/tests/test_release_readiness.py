from __future__ import annotations

from dtmo.release.readiness import (
    REQUIRED_PRODUCTION_GATES,
    GateEvidence,
    GateStatus,
    evaluate_readiness,
)


def _passing_evidence(gate: str) -> GateEvidence:
    return GateEvidence(
        gate=gate,
        status=GateStatus.PASS,
        evidence_url=f"https://example.invalid/evidence/{gate}",
        evidence_sha256="a" * 64,
    )


def test_complete_verified_evidence_is_production_ready() -> None:
    decision = evaluate_readiness(_passing_evidence(gate) for gate in REQUIRED_PRODUCTION_GATES)

    assert decision.ready is True
    assert decision.status is GateStatus.PASS
    assert decision.blockers == ()
    assert set(decision.verified_gates) == REQUIRED_PRODUCTION_GATES


def test_missing_gate_blocks_release() -> None:
    evidence = [
        _passing_evidence(gate)
        for gate in REQUIRED_PRODUCTION_GATES
        if gate != "security-assurance"
    ]

    decision = evaluate_readiness(evidence)

    assert decision.ready is False
    assert "security-assurance: missing evidence" in decision.blockers


def test_pass_without_verifiable_evidence_blocks_release() -> None:
    evidence = [_passing_evidence(gate) for gate in REQUIRED_PRODUCTION_GATES]
    evidence = [
        GateEvidence(gate=item.gate, status=item.status)
        if item.gate == "container-smoke"
        else item
        for item in evidence
    ]

    decision = evaluate_readiness(evidence)

    assert decision.ready is False
    assert "container-smoke: unverifiable evidence" in decision.blockers


def test_pending_failed_and_duplicate_evidence_block_release() -> None:
    evidence = [_passing_evidence(gate) for gate in REQUIRED_PRODUCTION_GATES]
    evidence.append(_passing_evidence("coverage"))
    evidence = [
        GateEvidence(
            gate=item.gate,
            status=GateStatus.PENDING,
            evidence_url=item.evidence_url,
            evidence_sha256=item.evidence_sha256,
        )
        if item.gate == "go-no-go"
        else item
        for item in evidence
    ]

    decision = evaluate_readiness(evidence)

    assert decision.ready is False
    assert "coverage: duplicate evidence" in decision.blockers
    assert "go-no-go: status=pending" in decision.blockers
