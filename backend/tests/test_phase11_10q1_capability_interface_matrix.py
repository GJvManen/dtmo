import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "docs/roadmap/CAPABILITY_INTERFACE_MATRIX.json"


def test_capability_matrix_uses_governed_status_model_and_covers_critical_domains():
    payload = json.loads(MATRIX.read_text(encoding="utf-8"))
    allowed = set(payload["status_model"])
    rows = payload["capabilities"]
    assert payload["phase"] == "11.10q1"
    assert rows
    assert all(row["status"] in allowed for row in rows)
    ids = {row["id"] for row in rows}
    required = {
        "dashboard.summary",
        "operations.metrics",
        "sources.catalog-bootstrap-run-health",
        "intelligence.workspace-detail",
        "intelligence.ail-correlation",
        "ioc.inventory",
        "analysis.intelowl",
        "analysis.cortex",
        "opencti.graph-mappings-revisions",
        "vulnerability.analytics",
        "misp.read-export",
        "thehive.handoff",
        "governance.frameworks-crosswalks",
        "administration.rbac",
    }
    assert required <= ids


def test_user_facing_gaps_have_target_slice_and_non_user_facing_is_explicit():
    payload = json.loads(MATRIX.read_text(encoding="utf-8"))
    for row in payload["capabilities"]:
        if row["status"] == "INTENTIONALLY_NON_USER_FACING":
            assert row["canonical_ui"] is None
        else:
            assert row["canonical_ui"]
            assert row["target_slice"] and row["target_slice"].startswith("11.10q")
