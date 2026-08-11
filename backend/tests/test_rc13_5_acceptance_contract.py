from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_rc13_5_workflow_runs_one_session_browser_journey_fail_closed() -> None:
    workflow = (ROOT / ".github/workflows/rc13-full-functional-console-acceptance.yml").read_text(
        encoding="utf-8"
    )
    assert "RC13 Full Functional Console Acceptance Gate" in workflow
    assert "test_rc13_5_full_console_browser_e2e.py" in workflow
    assert '"one_browser_context": True' in workflow
    assert '"synthetic_browser_fixtures_only": True' in workflow
    assert '"project_owner_functional_retest_required": True' in workflow
    assert '"phase8_status": "PAUSED_PENDING_RC13_OWNER_RETEST"' in workflow
    assert 'test "$BROWSER_RESULT" = "success"' in workflow


def test_rc13_5_browser_journey_covers_all_canonical_areas() -> None:
    source = (ROOT / "backend/tests/test_rc13_5_full_console_browser_e2e.py").read_text(
        encoding="utf-8"
    )
    for label in (
        'name="Overzicht"',
        'name="Intelligence"',
        'name="Bronnen & catalogus"',
        'name="Visual analytics"',
        'name="Administration"',
        'name="Governance"',
    ):
        assert label in source
    assert "Frameworkbronnen registreren" in source
    assert "Feed nu laden" in source
    assert "Principal aanmaken" in source
    assert "publication/share authority" in source
    assert "assert grafana_requests == []" in source


def test_phase8_remains_paused_until_owner_retest_after_rc13_5_ci() -> None:
    gate = (ROOT / "docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md").read_text(
        encoding="utf-8"
    )
    phase8 = (ROOT / "docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md").read_text(
        encoding="utf-8"
    )
    assert "RC13.4" in gate and "PASS" in gate
    assert "RC13.5" in gate and "PENDING_CI" in gate
    assert "project-owner" in gate.lower()
    assert "PAUSED_PENDING_RC13" in phase8
    assert "owner" in phase8.lower()
