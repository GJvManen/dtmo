from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IOC = ROOT / "frontend/src/IocExplorerWorkspace.tsx"
OPERATOR = ROOT / "docs/user/AIL_CORRELATION_WORKSPACE.md"
WORKFLOW = ROOT / ".github/workflows/e8-ail-correlation-workspace.yml"


def test_canonical_ioc_explorer_exposes_same_origin_read_only_ail_correlation():
    text = IOC.read_text(encoding="utf-8")
    for marker in (
        "Inspect AIL correlation",
        "/api/v1/intelligence/${encodeURIComponent(record.item_id)}/ail-correlations",
        "AIL · read-only correlation",
        "Same-origin DTMO API",
        "raw_content_exposed",
        "analysis_only",
        "claim_boundary",
        "never exposes the AIL API key",
        "review/share/case/publication authority",
    ):
        assert marker in text, marker


def test_canonical_ail_operator_and_browser_gate_are_route_explicit_and_fail_closed():
    operator = OPERATOR.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "/workbench/ioc-explorer" in operator
    assert "Inspect AIL correlation" in operator
    assert "zero-correlation, upstream-health or local-compromise conclusion" in operator
    assert "test_canonical_ail_correlation_browser_e2e.py" in workflow
    assert "DTMO_FRONTEND_DIST" in workflow
    assert "'/workbench/ioc-explorer'" in workflow
    for marker in (
        "live_ail_misp_connectivity_proven",
        "owner_acceptance_proven",
        "pentest_acceptance_proven",
        "review_share_case_publication_authority_proven",
    ):
        assert marker in workflow, marker
