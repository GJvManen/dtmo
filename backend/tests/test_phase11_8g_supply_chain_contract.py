from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_pr_supply_chain_gate_is_exact_head_and_fail_closed() -> None:
    workflow = read(".github/workflows/phase11-supply-chain-hardening.yml")
    assert "github.event.pull_request.head.sha" in workflow
    assert "Verify exact PR head" in workflow
    assert "pip_audit --format cyclonedx-json" in workflow
    assert "python-vulnerabilities.json" in workflow
    assert "aquasecurity/trivy-action@v0.36.0" in workflow
    assert "Generate Trivy-owned container CycloneDX SBOM" in workflow
    assert "scan-type: sbom" in workflow
    assert "scan-ref: artifacts/container-sbom.cdx.json" in workflow
    assert "severity: HIGH,CRITICAL" in workflow
    assert "exit-code: '1'" in workflow
    assert "container-sbom.cdx.json" in workflow
    assert "sha256sum" in workflow


def test_release_attestation_path_is_signed_and_not_a_pr_event() -> None:
    workflow = read(".github/workflows/release-artifact-attestation.yml")
    assert "pull_request:" not in workflow
    assert "id-token: write" in workflow
    assert "attestations: write" in workflow
    assert "actions/attest@v4" in workflow
    assert workflow.count("actions/attest@v4") >= 4
    assert "subject-path: artifacts/dist/*.whl" in workflow
    assert "subject-path: artifacts/dtmo-image.tar" in workflow
    assert "sbom-path: artifacts/python-sbom.cdx.json" in workflow
    assert "sbom-path: artifacts/container-sbom.cdx.json" in workflow


def test_professional_supply_chain_boundaries_are_documented() -> None:
    security = read("docs/security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md").lower()
    runbook = read("docs/operations/PHASE11_8G_SUPPLY_CHAIN_RUNBOOK.md").lower()
    gate = read("docs/qa/PHASE11_8G_SUPPLY_CHAIN_GATE.md").lower()
    for marker in (
        "cyclonedx",
        "vulnerability",
        "sha-256",
        "signed",
        "provenance",
        "sigstore",
        "fail closed",
        "does not prove",
    ):
        assert marker in security or marker in gate
    assert "rollback" in runbook
    assert "long-lived signing key" in runbook
    assert "production authorization" in security
