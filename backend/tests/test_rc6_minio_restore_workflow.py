from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
VERIFIER = ROOT / "tools" / "verify_minio_backup_restore.py"


def _workflow() -> dict[str, Any]:
    # BaseLoader intentionally preserves GitHub Actions keys such as `on` as strings.
    # The input is a trusted repository-controlled workflow file, not untrusted YAML.
    loaded = yaml.load(  # noqa: S506
        WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader
    )
    assert isinstance(loaded, dict)
    return loaded


def _commands(job: dict[str, Any]) -> str:
    steps = job.get("steps")
    assert isinstance(steps, list)
    return "\n".join(str(step.get("run", "")) for step in steps if isinstance(step, dict))


def test_minio_restore_is_isolated_release_blocking_and_observable() -> None:
    jobs = _workflow()["jobs"]
    assert isinstance(jobs, dict)
    restore = jobs["minio-restore"]
    assert isinstance(restore, dict)
    commands = _commands(restore)
    assert "minio-source" in commands
    assert "minio-target" in commands
    assert "127.0.0.1:9000" in commands
    assert "127.0.0.1:9002" in commands
    assert "tools/verify_minio_backup_restore.py" in commands
    assert "artifacts/dtmo-minio-backup.tar.gz" in commands
    assert "artifacts/minio-restore-evidence.json" in commands

    uploads = [
        step
        for step in restore["steps"]
        if isinstance(step, dict) and str(step.get("uses", "")).startswith("actions/upload-artifact@")
    ]
    assert len(uploads) == 1
    upload = uploads[0]
    assert upload.get("if") == "always()"
    upload_with = upload["with"]
    assert upload_with["name"] == "minio-restore-evidence"
    assert upload_with["if-no-files-found"] == "error"

    release_gate = jobs["release-gate"]
    assert "minio-restore" in release_gate["needs"]
    gate_commands = _commands(release_gate)
    assert '"minio-restore": os.environ["MINIO_RESTORE"]' in gate_commands
    assert "needs.minio-restore.result" in gate_commands


def test_minio_verifier_preserves_digest_and_provenance_contract() -> None:
    source = VERIFIER.read_text(encoding="utf-8")
    assert "sha256" in source
    assert "provenance-reference" in source
    assert "source_target_manifest_equal" in source
    assert "clean_target_verified" in source
    assert "rpo_basis" in source
    assert "tarfile.open" in source
