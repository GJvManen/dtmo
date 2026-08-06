from __future__ import annotations

import ast
from pathlib import Path

MIGRATION = (
    Path(__file__).parents[2]
    / "database"
    / "migrations"
    / "versions"
    / "0002_rc5_canonical_intelligence.py"
)


def _source() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def test_canonical_migration_has_linear_reversible_revision_chain() -> None:
    source = _source()
    tree = ast.parse(source)

    assignments = {
        node.targets[0].id: ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id in {"revision", "down_revision"}
    }

    assert assignments == {
        "revision": "0002_rc5_canonical",
        "down_revision": "0001_rc4_core",
    }
    function_names = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    assert {"upgrade", "downgrade"}.issubset(function_names)


def test_canonical_migration_backfills_before_dropping_legacy_confidence() -> None:
    source = _source()

    item_backfill = source.index("UPDATE intelligence_items")
    item_drop = source.index('op.drop_column("intelligence_items", "confidence")')
    provenance_backfill = source.index("UPDATE provenance_records")
    provenance_drop = source.index('op.drop_column("provenance_records", "confidence")')

    assert item_backfill < item_drop
    assert provenance_backfill < provenance_drop
    assert "migrated from RC4 confidence" in source


def test_canonical_migration_preserves_governance_and_integrity_constraints() -> None:
    source = _source()

    required_controls = {
        "ck_intelligence_confidence_score",
        "ck_intelligence_education_relevance",
        "ck_provenance_confidence_score",
        "uq_provenance_item_source_content",
        "ck_intelligence_revision_number",
        "uq_intelligence_item_revision",
        "uq_intelligence_item_revision_hash",
        'ondelete="CASCADE"',
    }

    assert required_controls.issubset(set(control for control in required_controls if control in source))
    assert "share_approved" not in source
    assert "review_status" not in source
