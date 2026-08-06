from pathlib import Path


MIGRATION = Path("database/migrations/versions/0005_connector_runtime_state.py")


def test_connector_state_migration_is_reversible_and_fail_closed() -> None:
    content = MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "0005_connector_state"' in content
    assert 'down_revision: str | None = "0004_privacy_projection"' in content
    for table in (
        "connector_runtime_states",
        "connector_health_events",
        "connector_quarantine_records",
    ):
        assert f'"{table}"' in content
        assert f'op.drop_table("{table}")' in content
    assert "ck_connector_health_never_publishes" in content
    assert "ck_connector_quarantine_never_publishes" in content
    assert "ck_connector_quarantine_recovery_evidence" in content
    assert "uq_connector_health_run" in content
    assert "uq_connector_quarantine_evidence" in content
