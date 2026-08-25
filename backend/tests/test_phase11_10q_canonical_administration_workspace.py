from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/AdministrationWorkspace.tsx"
MAIN = ROOT / "frontend/src/main.tsx"
BACKEND = ROOT / "backend/dtmo/admin_center.py"
APP = ROOT / "backend/dtmo/main.py"


def test_canonical_administration_route_is_not_a_generic_empty_foundation() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    main = MAIN.read_text(encoding="utf-8")
    assert "AdministrationWorkspace" in main
    assert 'path="/administration"' in main
    assert "<AdministrationWorkspace />" in main
    assert "Framework integrations" in workspace
    assert "Runtime configuration" in workspace


def test_canonical_administration_uses_same_origin_governed_read_and_patch() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")
    assert "credentials: 'same-origin'" in workspace
    assert "'/api/v1/admin/integrations'" in workspace
    assert "writeJson<IntegrationRow>(`/api/v1/admin/integrations/${encodeURIComponent(id)}`, 'PATCH'" in workspace
    assert "/api/v1/admin/integrations/${encodeURIComponent(id)}" in workspace
    assert 'require_permission(Permission.MANAGE_CONNECTORS)' in backend
    assert '@router.patch("/api/v1/admin/integrations/{integration_id}")' in backend


def test_browser_can_replace_credentials_write_only_without_receiving_secret_values() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")
    assert "Credential (write-only)" in workspace
    assert 'type="password"' in workspace
    assert "Leave blank to keep current credential" in workspace
    assert "credential: credential.trim()" in workspace
    assert "Credentials remain server-side and are never returned by this API." in backend
    assert "_RUNTIME_SECRET_PATH" in backend
    assert "chmod(0o600)" in backend
    assert '"credential_configured": credential_configured' in backend
    assert '"credential":' not in backend.split("return {", 1)[1].split("}", 1)[0]


def test_ready_misp_can_execute_existing_server_side_import_from_canonical_administration() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    assert "Run MISP import now" in workspace
    assert "runJson<ConnectorRunResult>('/connectors/misp/run')" in workspace
    assert "row.id === 'misp' && row.enabled && row.state === 'ready' && !dirty" in workspace
    assert "Records {lastMispRun.records}; inserted {lastMispRun.inserted}; indexed {lastMispRun.indexed}" in workspace
    assert "lastMispRun.correlation_id" in workspace
    assert '@app.post("/connectors/misp/run")' in app
    assert 'require_permission(Permission.MANAGE_CONNECTORS)' in app
    assert "return await run_misp()" in app
    assert "ingest_connector_record(result.connector_id, record)" in app


def test_ail_can_be_scoped_and_executed_end_to_end_from_canonical_administration() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    assert "AIL object scope" in workspace
    assert "ail_object_global_ids" in backend
    assert "activation_blockers" in backend
    assert "Run AIL import now" in workspace
    assert "runJson<ConnectorRunResult>('/connectors/ail/run')" in workspace
    assert "row.id === 'ail' && row.enabled && row.state === 'ready' && !dirty" in workspace
    assert '@app.post("/connectors/ail/run")' in app
    assert "return await run_ail()" in app
    assert "ingest_connector_record(result.connector_id, record)" in app


def test_intelowl_analyzer_policy_is_configurable_without_moving_execution_into_administration() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")
    assert "IntelOwl analyzer allowlist" in workspace
    assert "intelowl_allowed_analyzers" in workspace
    assert "intelowl_allowed_analyzers" in backend
    assert 'integration_id in {"ail", "intelowl", "cortex"}' in backend
    assert "IntelOwl analyzer allowlist is only valid for the IntelOwl integration" in backend
    assert "Analyzer execution still occurs only from governed analyst workflows" in workspace
    assert "Run IntelOwl" not in workspace
