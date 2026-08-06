from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "multistore-recovery.yml"
VERIFIER = ROOT / "tools" / "verify_multistore_recovery.py"


def _workflow() -> dict[str, Any]:
    loaded = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    if True in loaded and "on" not in loaded:
        loaded["on"] = loaded.pop(True)
    return loaded


def _commands(job: dict[str, Any]) -> str:
    steps = job.get("steps")
    assert isinstance(steps, list)
    return "\n".join(str(step.get("run", "")) for step in steps if isinstance(step, dict))


def test_multistore_recovery_is_single_point_observable_and_fail_closed() -> None:
    workflow = _workflow()
    assert workflow["name"] == "RC6 Multi-store Recovery Gate"
    jobs = workflow["jobs"]
    recovery = jobs["multistore-recovery"]
    services = recovery["services"]
    assert services["postgres"]["image"] == "postgres:17-alpine"
    assert services["opensearch"]["image"] == "opensearchproject/opensearch:2.19.1"
    commands = _commands(recovery)
    assert "RECOVERY_POINT_ID=" in commands
    assert "RECOVERY_STARTED_AT=" in commands
    assert "verify_postgres_backup_restore.py" in commands
    assert "verify_minio_backup_restore.py" in commands
    assert "verify_opensearch_reconstruction.py" in commands
    assert "verify_multistore_recovery.py" in commands
    assert "multistore-recovery-evidence.json" in commands

    uploads = [
        step
        for step in recovery["steps"]
        if isinstance(step, dict) and str(step.get("uses", "")).startswith("actions/upload-artifact@")
    ]
    assert len(uploads) == 1
    assert uploads[0]["if"] == "always()"
    assert uploads[0]["with"]["if-no-files-found"] == "error"

    gate = jobs["recovery-gate"]
    assert gate["if"] == "always()"
    assert gate["needs"] == ["multistore-recovery"]
    assert 'test "$MULTISTORE_RECOVERY" = "success"' in _commands(gate)


def test_combined_verifier_requires_all_integrity_domains() -> None:
    source = VERIFIER.read_text(encoding="utf-8")
    assert "audit_chain_valid" in source
    assert "provenance_hashes" in source
    assert "provenance_references_verified" in source
    assert "source_target_manifest_equal" in source
    assert "cross_store_provenance_envelope_sha256" in source
    assert "end_to_end_rto_seconds" in source
    assert '"rpo_seconds": 0' in source
