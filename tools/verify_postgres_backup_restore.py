from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from sqlalchemy import create_engine, select, text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import Session

from dtmo.audit import AuditDecision
from dtmo.audit.store import append_persistent_audit_event, verify_persistent_audit_chain
from dtmo.intelligence.model import (
    ConfidenceLevel,
    IntelligenceSeverity,
    IntelligenceType,
    SourceReliability,
)
from dtmo.persistence.models import IntelligenceItem, ProvenanceRecord


def _postgres_cli_url(value: str) -> str:
    url = make_url(value)
    if not url.drivername.startswith("postgresql"):
        raise ValueError("backup and restore verification requires PostgreSQL")
    cli_url: URL = url.set(drivername="postgresql")
    return cli_url.render_as_string(hide_password=False)


def _run(command: list[str]) -> None:
    # Commands are fixed internal argv lists built by this recovery verifier; shell=False.
    subprocess.run(command, check=True, text=True)  # noqa: S603


def _seed_source(session: Session) -> None:
    existing = session.scalar(
        select(IntelligenceItem).where(IntelligenceItem.source_id == "recovery-fixture")
    )
    if existing is not None:
        raise RuntimeError("recovery fixture already exists; source database must be fresh")

    item = IntelligenceItem(
        id=uuid4(),
        source_id="recovery-fixture",
        external_id="education-advisory-001",
        item_type=IntelligenceType.ADVISORY,
        title="Recovery integrity fixture",
        summary="Controlled record for clean-environment PostgreSQL restore verification.",
        canonical_url="https://example.test/recovery/education-advisory-001",
        published_at=datetime(2026, 8, 6, 12, 0, tzinfo=UTC),
        discovered_at=datetime(2026, 8, 6, 12, 5, tzinfo=UTC),
        content_hash="a" * 64,
        severity=IntelligenceSeverity.HIGH,
        confidence_score=92,
        confidence_level=ConfidenceLevel.VERY_HIGH,
        confidence_rationale=["authoritative recovery fixture", "content integrity verified"],
        education_relevance=95,
        review_status="reviewed",
        share_approved=True,
        tags=["recovery", "education"],
        metadata_json={
            "reviewed_by": "reviewer@example.test",
            "share_approved_by": "publisher@example.test",
        },
    )
    item.provenance.append(
        ProvenanceRecord(
            id=uuid4(),
            source_url="https://vendor.example.test/advisories/education-advisory-001",
            source_title="Education advisory 001",
            publisher="Recovery Fixture Vendor",
            retrieved_at=datetime(2026, 8, 6, 12, 6, tzinfo=UTC),
            content_hash="b" * 64,
            exact_passage="Controlled provenance text for restore verification.",
            source_reliability=SourceReliability.AUTHORITATIVE,
            is_primary_source=True,
            content_integrity_verified=True,
            confidence_score=95,
        )
    )
    session.add(item)
    session.flush()

    append_persistent_audit_event(
        session,
        principal="reviewer@example.test",
        principal_type="human",
        action="intelligence.review",
        resource=f"intelligence:{item.id}",
        decision=AuditDecision.ALLOW,
        request_id="recovery-request-review",
        provenance_reference=item.canonical_url,
    )
    append_persistent_audit_event(
        session,
        principal="publisher@example.test",
        principal_type="human",
        action="intelligence.share_approve",
        resource=f"intelligence:{item.id}",
        decision=AuditDecision.ALLOW,
        request_id="recovery-request-share",
        provenance_reference=item.canonical_url,
    )
    session.commit()


def _canonical_rows(session: Session, statement: str) -> list[dict[str, Any]]:
    rows = [dict(row) for row in session.execute(text(statement)).mappings().all()]
    return json.loads(json.dumps(rows, default=str, sort_keys=True))


def _manifest(session: Session) -> dict[str, Any]:
    audit_valid, audit_reason = verify_persistent_audit_chain(session)
    if not audit_valid:
        raise RuntimeError(f"audit chain verification failed: {audit_reason}")

    datasets = {
        "intelligence": _canonical_rows(
            session,
            """
            SELECT id, source_id, external_id, item_type, title, summary, canonical_url,
                   published_at, discovered_at, content_hash, severity, confidence_score,
                   confidence_level, confidence_rationale, education_relevance,
                   review_status, share_approved, tags, metadata_json
            FROM intelligence_items
            ORDER BY id
            """,
        ),
        "provenance": _canonical_rows(
            session,
            """
            SELECT id, item_id, source_url, source_title, publisher, retrieved_at,
                   content_hash, exact_passage, source_reliability, is_primary_source,
                   content_integrity_verified, confidence_score
            FROM provenance_records
            ORDER BY id
            """,
        ),
        "audit": _canonical_rows(
            session,
            """
            SELECT sequence_number, event_id, occurred_at, principal, principal_type,
                   action, resource, decision, request_id, provenance_reference,
                   previous_hash, event_hash, schema_version
            FROM audit_event_records
            ORDER BY sequence_number
            """,
        ),
        "alembic": _canonical_rows(
            session,
            "SELECT version_num FROM alembic_version ORDER BY version_num",
        ),
    }
    encoded = json.dumps(datasets, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return {
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "counts": {name: len(rows) for name, rows in datasets.items()},
        "audit_chain_valid": True,
        "audit_tail_hash": datasets["audit"][-1]["event_hash"],
        "provenance_hashes": [row["content_hash"] for row in datasets["provenance"]],
        "datasets": datasets,
    }


def verify_backup_restore(
    *,
    source_url: str,
    target_url: str,
    backup_path: Path,
    evidence_path: Path,
) -> dict[str, Any]:
    source_engine = create_engine(source_url, pool_pre_ping=True)
    target_engine = create_engine(target_url, pool_pre_ping=True)

    with Session(target_engine) as target_session:
        tables = target_session.execute(
            text(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'public' ORDER BY tablename"
            )
        ).scalars().all()
        if tables:
            raise RuntimeError("restore target must be a clean database")

    with Session(source_engine) as source_session:
        _seed_source(source_session)
        source_manifest = _manifest(source_session)

    backup_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    source_cli = _postgres_cli_url(source_url)
    target_cli = _postgres_cli_url(target_url)

    _run(
        [
            "pg_dump",
            "--format=custom",
            "--no-owner",
            "--no-acl",
            f"--file={backup_path}",
            f"--dbname={source_cli}",
        ]
    )
    if not backup_path.is_file() or backup_path.stat().st_size == 0:
        raise RuntimeError("pg_dump did not produce a non-empty backup")

    restore_started = time.monotonic()
    _run(
        [
            "pg_restore",
            "--exit-on-error",
            "--no-owner",
            "--no-acl",
            f"--dbname={target_cli}",
            str(backup_path),
        ]
    )
    restore_seconds = round(time.monotonic() - restore_started, 3)

    with Session(target_engine) as target_session:
        target_manifest = _manifest(target_session)

    if source_manifest != target_manifest:
        raise RuntimeError("restored database manifest differs from the source manifest")

    backup_sha256 = hashlib.sha256(backup_path.read_bytes()).hexdigest()
    evidence = {
        "schema_version": 1,
        "gate": "postgres-backup-restore",
        "decision": "pass",
        "backup": {
            "format": "pg_dump-custom",
            "sha256": backup_sha256,
            "size_bytes": backup_path.stat().st_size,
        },
        "recovery": {
            "clean_target_verified": True,
            "measured_restore_seconds": restore_seconds,
            "rpo_seconds": 0,
            "rpo_basis": "quiesced logical snapshot after committed fixture transaction",
        },
        "integrity": {
            "source_manifest_sha256": source_manifest["sha256"],
            "target_manifest_sha256": target_manifest["sha256"],
            "audit_chain_valid": target_manifest["audit_chain_valid"],
            "audit_tail_hash": target_manifest["audit_tail_hash"],
            "provenance_hashes": target_manifest["provenance_hashes"],
            "row_counts": target_manifest["counts"],
        },
    }
    evidence_path.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return evidence


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create and restore a PostgreSQL logical backup and emit integrity evidence."
    )
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--target-url", required=True)
    parser.add_argument("--backup", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    evidence = verify_backup_restore(
        source_url=args.source_url,
        target_url=args.target_url,
        backup_path=args.backup,
        evidence_path=args.evidence,
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
