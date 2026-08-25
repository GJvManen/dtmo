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
    assert "invalidateQueries({ queryKey: ['automation', 'persisted-source-status'] })" in source
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
    assert "not a complete immutable run history" in source
    assert "not a complete immutable run history" in doc
    assert "production authorization" in source


def test_automation_reads_persisted_latest_execution_observation_from_canonical_source_center():
    source = WORKSPACE.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")
    assert "'/api/v1/source-center/status'" in source
    assert "Latest durable execution observation" in source
    assert "last_success_at" in source
    assert "last_failure_at" in source
    assert "consecutive_failures" in source
    assert "isolated_until" in source
    assert "No persisted Source Center observation is available" in source
    assert "does not prove that no execution has occurred" in source
    assert "latest persisted connector state" in doc
