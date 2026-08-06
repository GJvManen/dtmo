from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.verify_multistore_recovery import verify_multistore_recovery


def _write(path: Path, payload: dict[str, object]) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _store_evidence(tmp_path: Path) -> tuple[Path, Path, Path]:
    postgres = _write(
        tmp_path / "postgres.json",
        {
            "decision": "pass",
            "recovery": {
                "clean_target_verified": True,
                "measured_restore_seconds": 1.25,
                "rpo_seconds": 0,
            },
            "integrity": {
                "target_manifest_sha256": "a" * 64,
                "audit_chain_valid": True,
                "audit_tail_hash": "b" * 64,
                "provenance_hashes": ["c" * 64],
            },
        },
    )
    minio = _write(
        tmp_path / "minio.json",
        {
            "decision": "pass",
            "clean_target_verified": True,
            "source_target_manifest_equal": True,
            "provenance_references_verified": True,
            "restore_seconds": 0.5,
            "rpo_basis": "quiesced-source-fixture-zero-seconds",
            "backup_sha256": "d" * 64,
            "object_manifest": [
                {
                    "object_name": "raw/evidence.json",
                    "sha256": "e" * 64,
                    "provenance_reference": "provenance://fixture/001",
                }
            ],
        },
    )
    opensearch = _write(
        tmp_path / "opensearch.json",
        {
            "decision": "pass",
            "recovery": {
                "clean_target_verified": True,
                "measured_reconstruction_seconds": 0.75,
                "rpo_seconds": 0,
            },
            "integrity": {
                "target_manifest_sha256": "f" * 64,
                "source_target_manifest_equal": True,
                "provenance_references_verified": True,
            },
        },
    )
    return postgres, minio, opensearch


def test_multistore_recovery_binds_one_point_and_measures_rto_rpo(tmp_path: Path) -> None:
    postgres, minio, opensearch = _store_evidence(tmp_path)
    result = verify_multistore_recovery(
        recovery_point_id="commit:abc123",
        postgres_path=postgres,
        minio_path=minio,
        opensearch_path=opensearch,
        evidence_path=tmp_path / "combined.json",
    )

    assert result["decision"] == "pass"
    assert result["recovery_point_id"] == "commit:abc123"
    assert result["recovery"]["effective_rpo_seconds"] == 0
    assert result["recovery"]["end_to_end_rto_seconds"] == 2.5
    assert result["recovery"]["single_recovery_point_verified"] is True
    assert result["integrity"]["cross_store_provenance_controls_verified"] is True
    assert len(result["integrity"]["store_binding_sha256"]) == 64


def test_multistore_recovery_fails_closed_on_missing_provenance_control(tmp_path: Path) -> None:
    postgres, minio, opensearch = _store_evidence(tmp_path)
    payload = json.loads(minio.read_text(encoding="utf-8"))
    payload["provenance_references_verified"] = False
    minio.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RuntimeError, match="minio.provenance_references_verified"):
        verify_multistore_recovery(
            recovery_point_id="commit:abc123",
            postgres_path=postgres,
            minio_path=minio,
            opensearch_path=opensearch,
            evidence_path=tmp_path / "combined.json",
        )


def test_multistore_recovery_rejects_unbounded_rpo(tmp_path: Path) -> None:
    postgres, minio, opensearch = _store_evidence(tmp_path)
    payload = json.loads(opensearch.read_text(encoding="utf-8"))
    payload["recovery"]["rpo_seconds"] = -1
    opensearch.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RuntimeError, match="bounded RPO"):
        verify_multistore_recovery(
            recovery_point_id="commit:abc123",
            postgres_path=postgres,
            minio_path=minio,
            opensearch_path=opensearch,
            evidence_path=tmp_path / "combined.json",
        )
