from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/AdministrationWorkspace.tsx"
APP = ROOT / "backend/dtmo/main.py"
CONNECTOR = ROOT / "backend/dtmo/connectors/taranis.py"
READINESS = ROOT / "backend/dtmo/integration_readiness.py"


def test_taranis_can_execute_existing_checkpointed_read_path_from_canonical_administration() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    connector = CONNECTOR.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")

    assert "Run Taranis import now" in workspace
    assert "runJson<ConnectorRunResult>('/connectors/taranis/run')" in workspace
    assert "row.id === 'taranis' && row.enabled && row.state === 'ready' && !dirty" in workspace
    assert "Taranis runtime result" in workspace
    assert "lastTaranisRun.records" in workspace
    assert "lastTaranisRun.inserted" in workspace
    assert "lastTaranisRun.indexed" in workspace
    assert "lastTaranisRun.correlation_id" in workspace

    assert '@app.post("/connectors/taranis/run")' in app
    assert "return await run_taranis()" in app
    assert "ingest_connector_record(result.connector_id, record)" in app

    assert "class TaranisReadConnector" in connector
    assert "_load_checkpoint" in connector
    assert "_save_checkpoint" in connector
    assert "taranis_detail_cti_limit" in connector
    assert '"external_share_authorized": False' in connector

    assert '("taranis", "Taranis AI"' in readiness
    assert "Configure Taranis API base/token and enable the connector." in readiness
