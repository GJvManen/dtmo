from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALUES = ROOT / "deploy" / "helm" / "dtmo" / "values.yaml"
TEMPLATE = ROOT / "deploy" / "helm" / "dtmo" / "templates" / "runtime.yaml"
GITOPS = ROOT / "deploy" / "gitops" / "phase11-8" / "values.yaml"
ARCH = ROOT / "docs" / "architecture" / "PHASE11_8_RUNTIME_FOUNDATION.md"
ADMIN = ROOT / "docs" / "administration" / "KUBERNETES_RUNTIME_CONFIGURATION.md"
RUNBOOK = ROOT / "docs" / "operations" / "PHASE11_8_RUNTIME_FOUNDATION_RUNBOOK.md"
QA = ROOT / "docs" / "qa" / "PHASE11_8_RUNTIME_FOUNDATION_GATE.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_runtime_foundation_is_secure_by_default() -> None:
    values = _read(VALUES)
    template = _read(TEMPLATE)
    for marker in (
        "replicaCount: 2",
        "automountServiceAccountToken: false",
        "runAsNonRoot: true",
        "readOnlyRootFilesystem: true",
        "allowPrivilegeEscalation: false",
        'drop: ["ALL"]',
        "existingSecret: dtmo-runtime",
        "enabled: true",
        "minAvailable: 1",
    ):
        assert marker in values
    for marker in (
        'fail "image.digest is required',
        "RuntimeDefault",
        "automountServiceAccountToken: false",
        "secretRef:",
        "readinessProbe:",
        "livenessProbe:",
        "kind: NetworkPolicy",
        "kind: PodDisruptionBudget",
        "kubernetes.io/metadata.name: kube-system",
    ):
        assert marker in template


def test_gitops_values_do_not_embed_secret_material() -> None:
    text = _read(GITOPS)
    assert 'digest: ""' in text
    assert "existingSecret: dtmo-runtime" in text
    for forbidden in ("password:", "api_token:", "secretKey:", "BEGIN PRIVATE KEY"):
        assert forbidden not in text


def test_runtime_foundation_documentation_preserves_evidence_boundary() -> None:
    combined = "\n".join(_read(path) for path in (ARCH, ADMIN, RUNBOOK, QA))
    for marker in (
        "immutable",
        "NetworkPolicy",
        "external-secret",
        "non-root",
        "publication/share authority",
        "Repository CI",
        "production",
        "rollback",
    ):
        assert marker in combined
