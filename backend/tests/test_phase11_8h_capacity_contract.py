from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def test_capacity_policy_is_bounded_and_fail_closed():
    values = read("deploy/helm/dtmo/values.yaml")
    template = read("deploy/helm/dtmo/templates/capacity.yaml")
    doc = read("docs/architecture/PHASE11_8H_CAPACITY_RESOURCE_PLANNING.md").lower()
    assert "autoscaling:" in values
    assert "minReplicas: 3" in values
    assert "maxReplicas: 10" in values
    assert "kind: HorizontalPodAutoscaler" in template
    assert "autoscaling/v2" in template
    assert "maxReplicas must be >= minReplicas" in template
    for marker in ("saturation", "fails closed", "production-equivalent", "production authorization", "rbac", "licensing"):
        assert marker in doc
