from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "multistore-recovery.yml"


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


def test_multistore_workflow_is_observable_and_fail_closed() -> None:
    workflow = _workflow()
    assert workflow["name"] == "RC6 Multi-Store Recovery Gate"
    assert set(workflow["on"]) == {"workflow_dispatch", "pull_request", "push"}
    assert workflow["permissions"] == {"contents": "read"}

    jobs = workflow["jobs"]
    recovery = jobs["multistore-recovery"]
    services = recovery["services"]
    assert services["postgres"]["image"] == "postgres:16-alpine"
    assert services["opensearch"]["image"] == "opensearchproject/opensearch:2.19.1"
    assert services["opensearch"]["env"]["DISABLE_SECURITY_PLUGIN"] == "true"

    commands = _commands(recovery)
    assert "verify_postgres_backup_restore.py" in commands
    assert "verify_minio_backup_restore.py" in commands
    assert "verify_opensearch_reconstruction.py" in commands
    assert "verify_multistore_recovery.py" in commands
    assert 'commit:${GITHUB_SHA}' in commands

    uploads = [
        step
        for step in recovery["steps"]
        if isinstance(step, dict) and str(step.get("uses", "")).startswith("actions/upload-artifact@")
    ]
    assert len(uploads) == 1
    assert uploads[0]["if"] == "always()"
    assert uploads[0]["with"]["name"] == "multistore-recovery-evidence"
    assert uploads[0]["with"]["if-no-files-found"] == "error"

    gate = jobs["recovery-acceptance-gate"]
    assert gate["if"] == "always()"
    assert gate["needs"] == ["multistore-recovery"]
    assert 'test "$MULTISTORE_RECOVERY" = "success"' in _commands(gate)
