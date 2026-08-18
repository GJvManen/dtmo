from pathlib import Path

import yaml

ROOT = Path(__file__).parents[2]
VALUES = ROOT / "deploy/helm/dtmo/values.yaml"
RUNTIME = ROOT / "deploy/helm/dtmo/templates/runtime.yaml"
INGRESS = ROOT / "deploy/helm/dtmo/templates/ingress.yaml"
ARCH = ROOT / "docs/architecture/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION.md"
ADMIN = ROOT / "docs/administration/INGRESS_TLS_NETWORK_SEGMENTATION.md"
RUNBOOK = ROOT / "docs/operations/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_RUNBOOK.md"
QA = ROOT / "docs/qa/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_GATE.md"


def test_ingress_fails_closed_by_default() -> None:
    values = yaml.safe_load(VALUES.read_text(encoding="utf-8"))
    assert values["service"]["type"] == "ClusterIP"
    assert values["ingress"]["enabled"] is False
    assert values["ingress"]["tls"]["enabled"] is True
    assert values["ingress"]["className"] == ""
    assert values["ingress"]["host"] == ""
    assert values["ingress"]["tls"]["secretName"] == ""
    assert values["networkPolicy"]["enabled"] is True
    assert values["networkPolicy"]["ingressController"]["namespaceSelector"] == {}
    assert values["networkPolicy"]["ingressController"]["podSelector"] == {}


def test_ingress_template_requires_tls_and_explicit_identity() -> None:
    text = INGRESS.read_text(encoding="utf-8")
    for marker in (
        "ingress.className is required",
        "ingress.host is required",
        "ingress.tls.enabled must be true",
        "ingress.tls.secretName is required",
        "kind: Ingress",
        "ingressClassName:",
        "tls:",
        "secretName:",
    ):
        assert marker in text


def test_network_policy_restricts_ingress_controller_peer() -> None:
    text = RUNTIME.read_text(encoding="utf-8")
    for marker in (
        "networkPolicy.enabled must remain true",
        "networkPolicy.ingressController.namespaceSelector is required",
        "networkPolicy.ingressController.podSelector is required",
        "namespaceSelector:",
        "podSelector:",
        "port: 8000",
    ):
        assert marker in text
    assert "kubernetes.io/metadata.name: {{ .Release.Namespace }}" not in text.split("ingress:", 1)[1].split("egress:", 1)[0]


def test_professional_docs_preserve_security_and_evidence_boundaries() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in (ARCH, ADMIN, RUNBOOK, QA))
    for marker in (
        "fail closed",
        "publication/share authority",
        "private key",
        "rollback",
        "does not prove",
        "production authorization",
    ):
        assert marker.lower() in combined.lower()
