from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "opensearch-recovery.yml"
VERIFIER = ROOT / "tools" / "verify_opensearch_reconstruction.py"


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


def test_opensearch_reconstruction_is_clean_observable_and_fail_closed() -> None:
    workflow = _workflow()
    assert workflow["name"] == "RC6 OpenSearch Recovery Gate"
    jobs = workflow["jobs"]
    restore = jobs["opensearch-reconstruction"]
    services = restore["services"]
    assert services["postgres"]["image"] == "postgres:17-alpine"
    assert services["opensearch"]["image"] == "opensearchproject/opensearch:2.19.1"
    commands = _commands(restore)
    assert "python -m alembic upgrade head" in commands
    assert "tools/verify_opensearch_reconstruction.py" in commands
    assert "artifacts/opensearch-reconstruction-evidence.json" in commands
    uploads = [
        step
        for step in restore["steps"]
        if isinstance(step, dict) and str(step.get("uses", "")).startswith("actions/upload-artifact@")
    ]
    assert len(uploads) == 1
    assert uploads[0]["if"] == "always()"
    assert uploads[0]["with"]["name"] == "opensearch-reconstruction-evidence"
    assert uploads[0]["with"]["if-no-files-found"] == "error"

    gate = jobs["recovery-gate"]
    assert gate["if"] == "always()"
    assert gate["needs"] == ["opensearch-reconstruction"]
    assert 'test "$OPENSEARCH_RECONSTRUCTION" = "success"' in _commands(gate)


def test_verifier_preserves_canonical_manifest_and_provenance_contract() -> None:
    source = VERIFIER.read_text(encoding="utf-8")
    assert "dynamic\": \"strict" in source
    assert "source_manifest_sha256" in source
    assert "target_manifest_sha256" in source
    assert "source_target_manifest_equal" in source
    assert "provenance_references_verified" in source
    assert "clean_target_verified" in source
