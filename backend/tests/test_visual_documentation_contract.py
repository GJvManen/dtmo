from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STANDARD = ROOT / "docs/visual/DOCUMENTATION_VISUAL_STANDARD.md"
WORKFLOWS = ROOT / "docs/architecture/SYSTEM_WORKFLOWS.md"
SCREENSHOTS = ROOT / "docs/visual/screenshots/README.md"
CAPTURE = ROOT / "tools/capture_documentation_screenshots.py"
INVESTIGATION_CAPTURE = ROOT / "tools/capture_documentation_investigation_screenshots.py"
CI = ROOT / ".github/workflows/documentation-screenshots.yml"


def test_visual_documentation_standard_has_professional_information_architecture() -> None:
    text = STANDARD.read_text(encoding="utf-8")
    for heading in (
        "Product Guide",
        "User Guide",
        "Administrator Guide",
        "Architecture",
        "Security",
        "Governance",
        "Operations",
        "Integrations",
        "Deployment",
        "QA & Assurance",
        "Evidence",
        "Developer Reference",
    ):
        assert heading in text
    for workflow_id in range(1, 13):
        assert f"WF-{workflow_id:02d}" in text
    for screenshot_id in range(1, 11):
        assert f"UI-{screenshot_id:02d}" in text
    assert "must come from an actual DTMO runtime" in text
    assert "must never be presented as runtime evidence" in text


def test_system_workflow_reference_covers_all_required_flows_and_claim_boundary() -> None:
    text = WORKFLOWS.read_text(encoding="utf-8")
    for workflow_id in range(1, 13):
        assert f"WF-{workflow_id:02d}" in text
    assert text.count("```mermaid") >= 12
    for term in (
        "Source-to-intelligence",
        "Vulnerability prioritization",
        "Identity, bearer trust and RBAC",
        "MISP governed read and export",
        "AIL enrichment and correlation",
        "Audit and correlation trace",
        "Governance mapping and evidence",
        "Observability",
        "Backup, recovery and rollback",
        "immutable staging identity",
        "Production-readiness acceptance lifecycle",
    ):
        assert term in text
    assert "not, by themselves, staging evidence" in text
    assert "Evidence from different deployment identities must not be combined" in text


def test_screenshot_catalogue_is_runtime_backed_and_fail_closed() -> None:
    text = SCREENSHOTS.read_text(encoding="utf-8")
    assert "actual DTMO runtime UI" in text
    assert "runtime UI with synthetic fixture data" in text
    assert "documentation illustration only" in text
    assert "must never be presented as proof of live-source connectivity" in text
    for filename in (
        "overview-dashboard.png",
        "intelligence-workspace.png",
        "sources-catalogue.png",
        "vulnerability-analytics.png",
        "misp-governed-workflow.png",
        "ail-correlation-workspace.png",
        "visual-analytics.png",
        "governance-frameworks.png",
        "administration-rbac.png",
        "audit-correlation.png",
    ):
        assert filename in text


def test_capture_runner_uses_only_documentation_classification_and_sanitized_targets() -> None:
    text = CAPTURE.read_text(encoding="utf-8")
    assert "actual-runtime-ui-with-synthetic-fixture-data" in text
    assert "documentation-illustration-only" in text
    assert "example.test" in text
    assert "example.invalid" in text
    assert "X-DTMO-Subject" in text
    assert "X-DTMO-Roles" in text
    assert "page.screenshot" in text
    assert "production" not in "\n".join(
        line for line in text.splitlines() if "credential" in line.lower()
    ).lower()


def test_investigation_capture_includes_misp_without_outbound_share() -> None:
    text = INVESTIGATION_CAPTURE.read_text(encoding="utf-8")
    assert "/ui/misp-workspace" in text
    assert "misp-governed-workflow.png" in text
    assert "misp-read-and-governed-export-workspace" in text
    assert '"misp_export_executed": False' in text
    assert '"misp_live_connectivity_proven": False' in text
    assert "docs-publisher@example.test" in text


def test_screenshot_ci_is_artifact_only_and_fail_closed() -> None:
    text = CI.read_text(encoding="utf-8")
    assert "workflow_dispatch" in text
    assert "permissions:\n  contents: read" in text
    assert "DTMO_FEATURE_LIVE_CONNECTORS: \"false\"" in text
    assert "playwright install --with-deps chromium" in text
    assert "capture_documentation_screenshots.py" in text
    assert "actions/upload-artifact@v7" in text
    assert "dtmo-documentation-screenshots" in text
    assert "documentation-illustration-only" in text
    assert "misp-governed-workflow.png" in text
    assert "misp_export_executed" in text
    assert "misp_live_connectivity_proven" in text
    assert "contents: write" not in text
    assert "git push" not in text
    assert "Fail closed on missing or failed screenshot artifacts" in text
