from __future__ import annotations

import ast
from pathlib import Path

MIGRATION = Path("database/migrations/versions/0004_privacy_projection_retention.py")
SCHEDULE = Path("deploy/cron/privacy-projection-purge.cron")


def test_privacy_projection_migration_is_linear_and_preserves_source_audit() -> None:
    source = MIGRATION.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assignments = {
        node.target.id: node.value.value
        for node in tree.body
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and isinstance(node.value, ast.Constant)
    }
    assert assignments["revision"] == "0004_privacy_projection"
    assert assignments["down_revision"] == "0003_persistent_audit"
    assert "audit_projection_records" in source
    assert "audit_event_records.event_id" in source
    assert 'ondelete="RESTRICT"' in source
    assert "legal_hold_reference" in source
    assert "op.drop_table" in source
    assert "op.drop_table(\"audit_event_records\")" not in source


def test_daily_purge_schedule_uses_secret_backed_database_configuration() -> None:
    schedule = SCHEDULE.read_text(encoding="utf-8")
    assert "17 2 * * *" in schedule
    assert "python -m dtmo.privacy.retention_cli --batch-size 500" in schedule
    assert "DTMO_DATABASE_URL" in schedule
    assert "postgresql://" not in schedule
    assert "password=" not in schedule.lower()
