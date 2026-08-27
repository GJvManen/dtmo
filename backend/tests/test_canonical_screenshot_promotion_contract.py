from __future__ import annotations

import json
import struct
from pathlib import Path

import pytest

from tools.promote_canonical_screenshot import CANONICAL_TARGET, promote

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/documentation-screenshot-promotion.yml"


def _png(width: int = 1440, height: int = 1000) -> bytes:
    return b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + struct.pack(">II", width, height)


def _artifact(tmp_path: Path) -> tuple[Path, str]:
    generated = tmp_path / "artifact" / "generated"
    generated.mkdir(parents=True)
    image = generated / "command-center-workbench.png"
    image.write_bytes(_png())
    import hashlib

    image_sha = hashlib.sha256(image.read_bytes()).hexdigest()
    (generated / "canonical-capture-metadata.json").write_text(
        json.dumps(
            {
                "canonical_route": "/workbench/command-center",
                "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
                "evidence_classification": "documentation-illustration-only",
                "live_connectivity_proven": False,
                "owner_acceptance_proven": False,
                "production_equivalent_proven": False,
            }
        ),
        encoding="utf-8",
    )
    return tmp_path / "artifact", image_sha


def test_promotion_requires_exact_claim_boundaries_and_writes_review_record(tmp_path: Path) -> None:
    artifact, image_sha = _artifact(tmp_path)
    repo = tmp_path / "repo"
    record = promote(
        artifact,
        repo,
        expected_image_sha256=image_sha,
        source_run_id="33075823231",
        source_head_sha="d0d13b74a371e38c4fee965a4eb08f5d7f57cac9",
        source_artifact_digest="sha256:d08d609ada05f92ad7f4f4e69315ca56e61a7537c3ac1bf18a8ac4d9028a5ab0",
        reviewer="documentation-review",
    )
    assert (repo / "docs/visual/screenshots" / CANONICAL_TARGET).is_file()
    assert record["canonical_route"] == "/workbench/command-center"
    assert record["evidence_classification"] == "documentation-illustration-only"
    assert record["claim_boundaries"] == {
        "live_connectivity_proven": False,
        "owner_acceptance_proven": False,
        "production_equivalent_proven": False,
    }


def test_promotion_fails_closed_on_reviewed_hash_mismatch(tmp_path: Path) -> None:
    artifact, _ = _artifact(tmp_path)
    with pytest.raises(ValueError, match="SHA-256"):
        promote(
            artifact,
            tmp_path / "repo",
            expected_image_sha256="0" * 64,
            source_run_id="1",
            source_head_sha="a" * 40,
            source_artifact_digest="sha256:" + "b" * 64,
            reviewer="reviewer",
        )


def test_workflow_is_manual_exact_source_bound_and_never_auto_merges() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    for marker in (
        "workflow_dispatch:",
        "source_run_id:",
        "expected_head_sha:",
        "expected_artifact_digest:",
        "expected_image_sha256:",
        "actions: read",
        "contents: write",
        "pull-requests: write",
        "gh run download",
        "tools/promote_canonical_screenshot.py",
        "gh pr create",
        "promotion branch already exists; refusing to overwrite",
    ):
        assert marker in text, marker
    assert "gh pr merge" not in text
    assert "--admin" not in text
