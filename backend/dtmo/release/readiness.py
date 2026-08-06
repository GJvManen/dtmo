from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable


class GateStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    PENDING = "pending"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class GateEvidence:
    gate: str
    status: GateStatus
    evidence_url: str | None = None
    evidence_sha256: str | None = None
    detail: str | None = None

    @property
    def verifiable(self) -> bool:
        return bool(self.evidence_url and self.evidence_sha256)


@dataclass(frozen=True, slots=True)
class ReadinessDecision:
    ready: bool
    status: GateStatus
    blockers: tuple[str, ...]
    verified_gates: tuple[str, ...]


REQUIRED_PRODUCTION_GATES = frozenset(
    {
        "workflow-contracts",
        "lint",
        "type-check",
        "unit-tests",
        "coverage",
        "migrations",
        "container-smoke",
        "dependency-audit",
        "backup-restore",
        "staging-acceptance",
        "security-assurance",
        "go-no-go",
    }
)


def evaluate_readiness(
    evidence: Iterable[GateEvidence],
    *,
    required_gates: frozenset[str] = REQUIRED_PRODUCTION_GATES,
) -> ReadinessDecision:
    """Evaluate release readiness using a fail-closed evidence policy.

    A required gate only counts as verified when it has status PASS and carries both
    an evidence URL and a SHA-256 digest. Missing, duplicated, pending, blocked or
    failed gates prevent a production-ready decision.
    """

    by_gate: dict[str, GateEvidence] = {}
    duplicates: set[str] = set()
    for item in evidence:
        if item.gate in by_gate:
            duplicates.add(item.gate)
        by_gate[item.gate] = item

    blockers: list[str] = []
    verified: list[str] = []

    for gate in sorted(required_gates):
        item = by_gate.get(gate)
        if item is None:
            blockers.append(f"{gate}: missing evidence")
            continue
        if gate in duplicates:
            blockers.append(f"{gate}: duplicate evidence")
            continue
        if item.status is not GateStatus.PASS:
            blockers.append(f"{gate}: status={item.status.value}")
            continue
        if not item.verifiable:
            blockers.append(f"{gate}: unverifiable evidence")
            continue
        verified.append(gate)

    ready = not blockers
    return ReadinessDecision(
        ready=ready,
        status=GateStatus.PASS if ready else GateStatus.BLOCKED,
        blockers=tuple(blockers),
        verified_gates=tuple(verified),
    )
