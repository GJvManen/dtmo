from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend" / "src" / "AutomationWorkspace.tsx"
DOC = ROOT / "docs" / "user" / "AUTOMATION_PLAYBOOKS_WORKSPACE.md"


def test_automation_recovery_refreshes_runtime_state_after_execution():
    source = WORKSPACE.read_text(encoding="utf-8")
    assert "useQueryClient" in source
    assert "Refresh runtime observation" in source
    assert "invalidateQueries({ queryKey: ['automation', 'health'] })" in source
    assert "invalidateQueries({ queryKey: ['automation', 'connectors'] })" in source
    assert "onSuccess: async (data)" in source
    assert "await refreshRuntimeObservation()" in source


def test_manual_execution_fails_closed_when_capability_is_not_advertised():
    source = WORKSPACE.read_text(encoding="utf-8")
    assert "manual_run_available" in source
    assert "!selectedConnector?.manual_run_available" in source
    assert "does not advertise manual-run availability" in source
    assert "manage:connectors" in source
    assert "service_account" in source


def test_execution_evidence_is_visible_without_overclaiming_history():
    source = WORKSPACE.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")
    for marker in ("Observed bounded execution result", "attempts", "alert_state", "correlation_id"):
        assert marker in source
    assert "not durable execution-history evidence" in source
    assert "not durable execution-history evidence" in doc
    assert "production authorization" in source
