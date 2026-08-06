from __future__ import annotations

import ast
from pathlib import Path

MIGRATION = Path("database/migrations/versions/0003_persistent_audit_chain.py")


def test_persistent_audit_migration_is_linear_and_append_only() -> None:
    source = MIGRATION.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assignments = {
        node.target.id: node.value.value
        for node in tree.body
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and isinstance(node.value, ast.Constant)
    }
    assert assignments["revision"] == "0003_persistent_audit"
    assert assignments["down_revision"] == "0002_rc5_canonical"
    assert "audit_event_records" in source
    assert "BEFORE UPDATE OR DELETE" in source
    assert "append-only" in source
    assert "DROP TRIGGER IF EXISTS" in source
