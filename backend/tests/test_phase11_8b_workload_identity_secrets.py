from pathlib import Path

import yaml

ROOT = Path(__file__).parents[2]
VALUES = ROOT / "deploy/helm/dtmo/values.yaml"
RUNTIME = ROOT / "deploy/helm/dtmo/templates/runtime.yaml"
EXTERNAL_SECRET = ROOT / "deploy/helm/dtmo/templates/external-secret.yaml"
ARCH = ROOT / "docs/architecture/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md"
ADMIN = ROOT / "docs/administration/WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md"
RUNBOOK = ROOT / "docs/operations/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_RUNBOOK.md"
QA = ROOT / "docs/qa/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_GATE.md"


def test_values_fail_closed_by_default() -> None:
    values = yaml.safe_load(VALUES.read_text(encoding="utf-8"))
    assert values["serviceAccount"]["automountServiceAccountToken"] is False
    assert values["serviceAccount"]["annotations"] == {}
    assert values["externalSecret"]["enabled"] is False
    assert values["externalSecret"]["secretStoreRef"]["name"] == ""
    assert values["externalSecret"]["remoteKeys"] == {}
    assert values["existingSecret"] == "dtmo-runtime"


def test_runtime_identity_and_secret_consumption_are_bounded() -> None:
    text = RUNTIME.read_text(encoding="utf-8")
    assert "serviceAccount.annotations" in text
    assert "automountServiceAccountToken: false" in text
    assert "secretRef:" in text
    assert ".Values.externalSecret.targetName" in text
    assert "kind: Secret" not in text


def test_external_secret_requires_explicit_store_and_mappings() -> None:
    text = EXTERNAL_SECRET.read_text(encoding="utf-8")
    assert "external-secrets.io/v1beta1" in text
    assert 'fail "externalSecret.secretStoreRef.name is required' in text
    assert 'fail "externalSecret.remoteKeys must define at least one runtime secret mapping"' in text
    assert "secretStoreRef:" in text
    assert "remoteRef:" in text
    assert "creationPolicy: Owner" in text


def test_professional_documentation_preserves_authority_and_evidence_boundaries() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in (ARCH, ADMIN, RUNBOOK, QA)
    )
    for marker in (
        "automountServiceAccountToken",
        "publication/share authority",
        "fail closed",
        "Repository CI",
        "production authorization",
    ):
        assert marker.lower() in combined.lower()
    assert "private key" in combined.lower()
    assert "secret values" in combined.lower()
