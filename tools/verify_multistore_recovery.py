from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"evidence must be a JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_multistore_recovery(
    *,
    recovery_point_id: str,
    started_at: datetime,
    postgres_evidence: Path,
    minio_evidence: Path,
    opensearch_evidence: Path,
    output: Path,
) -> dict[str, Any]:
    if not recovery_point_id.strip():
        raise RuntimeError("recovery point identifier is required")
    if started_at.tzinfo is None:
        raise RuntimeError("recovery start timestamp must be timezone-aware")

    postgres = _load(postgres_evidence)
    minio = _load(minio_evidence)
    opensearch = _load(opensearch_evidence)

    decisions = {
        "postgres": postgres.get("decision"),
        "minio": minio.get("decision"),
        "opensearch": opensearch.get("decision"),
    }
    failed = sorted(name for name, decision in decisions.items() if decision != "pass")
    if failed:
        raise RuntimeError(f"subsystem recovery evidence is not passing: {', '.join(failed)}")

    postgres_integrity = postgres.get("integrity", {})
    minio_manifest = minio.get("object_manifest", [])
    opensearch_integrity = opensearch.get("integrity", {})
    if not postgres_integrity.get("audit_chain_valid"):
        raise RuntimeError("restored PostgreSQL audit chain is invalid")
    if not postgres_integrity.get("provenance_hashes"):
        raise RuntimeError("restored PostgreSQL provenance hashes are absent")
    if not minio.get("provenance_references_verified") or not minio_manifest:
        raise RuntimeError("restored MinIO provenance evidence is absent or invalid")
    if not opensearch_integrity.get("provenance_references_verified"):
        raise RuntimeError("reconstructed OpenSearch provenance references are invalid")
    if not opensearch_integrity.get("source_target_manifest_equal"):
        raise RuntimeError("OpenSearch source and target manifests differ")

    completed_at = datetime.now(UTC)
    rto_seconds = round((completed_at - started_at.astimezone(UTC)).total_seconds(), 3)
    if rto_seconds < 0:
        raise RuntimeError("recovery completion precedes recovery start")

    evidence_files = {
        "postgres": {"path": str(postgres_evidence), "sha256": _sha256(postgres_evidence)},
        "minio": {"path": str(minio_evidence), "sha256": _sha256(minio_evidence)},
        "opensearch": {"path": str(opensearch_evidence), "sha256": _sha256(opensearch_evidence)},
    }
    provenance_envelope = {
        "postgres_provenance_hashes": sorted(str(value) for value in postgres_integrity["provenance_hashes"]),
        "minio_provenance_references": sorted(
            str(item["provenance_reference"]) for item in minio_manifest if isinstance(item, dict)
        ),
        "opensearch_source_manifest_sha256": opensearch_integrity.get("source_manifest_sha256"),
        "opensearch_target_manifest_sha256": opensearch_integrity.get("target_manifest_sha256"),
    }
    encoded_envelope = json.dumps(provenance_envelope, separators=(",", ":"), sort_keys=True).encode()

    evidence = {
        "schema_version": 1,
        "gate": "combined-multistore-recovery",
        "decision": "pass",
        "recovery_point": {
            "id": recovery_point_id,
            "started_at": started_at.astimezone(UTC).isoformat(),
            "completed_at": completed_at.isoformat(),
            "rpo_seconds": 0,
            "rpo_basis": "single quiesced acceptance run before PostgreSQL, MinIO and OpenSearch recovery",
            "end_to_end_rto_seconds": rto_seconds,
        },
        "subsystems": decisions,
        "integrity": {
            "postgres_audit_chain_valid": True,
            "postgres_provenance_hashes_present": True,
            "minio_provenance_references_verified": True,
            "opensearch_provenance_references_verified": True,
            "opensearch_source_target_manifest_equal": True,
            "cross_store_provenance_envelope_sha256": hashlib.sha256(encoded_envelope).hexdigest(),
        },
        "evidence_files": evidence_files,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify combined DTMO multi-store recovery evidence")
    parser.add_argument("--recovery-point-id", required=True)
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--postgres-evidence", type=Path, required=True)
    parser.add_argument("--minio-evidence", type=Path, required=True)
    parser.add_argument("--opensearch-evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = verify_multistore_recovery(
        recovery_point_id=args.recovery_point_id,
        started_at=datetime.fromisoformat(args.started_at.replace("Z", "+00:00")),
        postgres_evidence=args.postgres_evidence,
        minio_evidence=args.minio_evidence,
        opensearch_evidence=args.opensearch_evidence,
        output=args.output,
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
