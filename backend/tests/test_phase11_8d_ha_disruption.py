from pathlib import Path

import yaml

ROOT = Path(__file__).parents[2]
VALUES = ROOT / "deploy/helm/dtmo/values.yaml"
RUNTIME = ROOT / "deploy/helm/dtmo/templates/runtime.yaml"
ARCH = ROOT / "docs/architecture/PHASE11_8D_HA_DISRUPTION.md"
RUNBOOK = ROOT / "docs/operations/PHASE11_8D_HA_DISRUPTION_RUNBOOK.md"
QA = ROOT / "docs/qa/PHASE11_8D_HA_DISRUPTION_GATE.md"


def test_multi_zone_defaults_are_fail_closed() -> None:
    values = yaml.safe_load(VALUES.read_text(encoding="utf-8"))
    assert values["replicaCount"] >= 2
    assert values["availability"]["topologySpread"]["enabled"] is True
    assert values["availability"]["podAntiAffinity"]["enabled"] is True
    assert values["podDisruptionBudget"]["enabled"] is True
    assert values["podDisruptionBudget"]["minAvailable"] >= 1


def test_runtime_enforces_multi_zone_and_host_spread() -> None:
    text = RUNTIME.read_text(encoding="utf-8")
    for marker in (
        "topology.kubernetes.io/zone",
        "kubernetes.io/hostname",
        "DoNotSchedule",
        "requiredDuringSchedulingIgnoredDuringExecution",
        "terminationGracePeriodSeconds",
        "replicaCount must be at least 2",
    ):
        assert marker in text


def test_documentation_preserves_evidence_boundary() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in (ARCH, RUNBOOK, QA))
    for marker in (
        "stateful",
        "multi-zone",
        "fail closed",
        "does not prove",
        "production authorization",
        "rollback",
    ):
        assert marker.lower() in combined.lower()
