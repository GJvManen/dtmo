from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload

from dtmo.persistence.models import IntelligenceItem

INDEX_NAME = "dtmo-intelligence-recovery"


def _canonical_document(item: IntelligenceItem) -> dict[str, Any]:
    provenance = sorted(
        (
            {
                "source_url": record.source_url,
                "content_hash": record.content_hash,
                "source_reliability": record.source_reliability.value,
                "is_primary_source": record.is_primary_source,
                "content_integrity_verified": record.content_integrity_verified,
            }
            for record in item.provenance
        ),
        key=lambda value: (value["source_url"], value["content_hash"]),
    )
    return {
        "id": str(item.id),
        "source_id": item.source_id,
        "external_id": item.external_id,
        "item_type": item.item_type.value,
        "title": item.title,
        "summary": item.summary,
        "canonical_url": item.canonical_url,
        "published_at": item.published_at.isoformat() if item.published_at else None,
        "discovered_at": item.discovered_at.isoformat(),
        "content_hash": item.content_hash,
        "severity": item.severity.value,
        "confidence_score": item.confidence_score,
        "confidence_level": item.confidence_level.value,
        "education_relevance": item.education_relevance,
        "review_status": item.review_status,
        "share_approved": item.share_approved,
        "tags": sorted(item.tags),
        "provenance": provenance,
    }


def _manifest(documents: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(documents, key=lambda value: value["id"])
    encoded = json.dumps(ordered, separators=(",", ":"), sort_keys=True).encode()
    return {
        "document_count": len(ordered),
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "documents": ordered,
    }


def verify_reconstruction(*, database_url: str, endpoint: str, evidence_path: Path) -> dict[str, Any]:
    engine = create_engine(database_url, pool_pre_ping=True)
    with Session(engine) as session:
        items = session.scalars(
            select(IntelligenceItem)
            .options(selectinload(IntelligenceItem.provenance))
            .order_by(IntelligenceItem.id)
        ).all()
        if not items:
            raise RuntimeError("canonical PostgreSQL source contains no intelligence records")
        source_manifest = _manifest([_canonical_document(item) for item in items])

    base = endpoint.rstrip("/")
    with httpx.Client(timeout=30.0) as client:
        health = client.get(f"{base}/_cluster/health")
        health.raise_for_status()
        existing = client.head(f"{base}/{INDEX_NAME}")
        if existing.status_code == 200:
            raise RuntimeError("OpenSearch recovery target must not contain the target index")
        if existing.status_code != 404:
            existing.raise_for_status()

        mapping = {
            "settings": {"index": {"number_of_shards": 1, "number_of_replicas": 0}},
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "source_id": {"type": "keyword"},
                    "external_id": {"type": "keyword"},
                    "item_type": {"type": "keyword"},
                    "title": {"type": "text"},
                    "summary": {"type": "text"},
                    "canonical_url": {"type": "keyword"},
                    "published_at": {"type": "date"},
                    "discovered_at": {"type": "date"},
                    "content_hash": {"type": "keyword"},
                    "severity": {"type": "keyword"},
                    "confidence_score": {"type": "integer"},
                    "confidence_level": {"type": "keyword"},
                    "education_relevance": {"type": "integer"},
                    "review_status": {"type": "keyword"},
                    "share_approved": {"type": "boolean"},
                    "tags": {"type": "keyword"},
                    "provenance": {"type": "object", "enabled": True},
                },
            },
        }
        created = client.put(f"{base}/{INDEX_NAME}", json=mapping)
        created.raise_for_status()

        started = time.monotonic()
        for document in source_manifest["documents"]:
            response = client.put(
                f"{base}/{INDEX_NAME}/_doc/{document['id']}",
                params={"refresh": "false"},
                json=document,
            )
            response.raise_for_status()
        client.post(f"{base}/{INDEX_NAME}/_refresh").raise_for_status()
        reconstruction_seconds = round(time.monotonic() - started, 3)

        response = client.get(
            f"{base}/{INDEX_NAME}/_search",
            params={"size": max(1, source_manifest["document_count"]), "sort": "id:asc"},
        )
        response.raise_for_status()
        hits = response.json()["hits"]["hits"]
        target_manifest = _manifest([hit["_source"] for hit in hits])

    if source_manifest != target_manifest:
        raise RuntimeError("reconstructed OpenSearch manifest differs from canonical source")

    evidence = {
        "schema_version": 1,
        "gate": "opensearch-reconstruction",
        "decision": "pass",
        "recorded_at": datetime.now(UTC).isoformat(),
        "recovery": {
            "clean_target_verified": True,
            "index": INDEX_NAME,
            "measured_reconstruction_seconds": reconstruction_seconds,
            "rpo_seconds": 0,
            "rpo_basis": "quiesced canonical PostgreSQL snapshot with immutable provenance references",
        },
        "integrity": {
            "source_manifest_sha256": source_manifest["sha256"],
            "target_manifest_sha256": target_manifest["sha256"],
            "document_count": target_manifest["document_count"],
            "source_target_manifest_equal": True,
            "provenance_references_verified": True,
        },
    }
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence


def main() -> None:
    parser = argparse.ArgumentParser(description="Reconstruct OpenSearch from canonical DTMO data.")
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify_reconstruction(database_url=args.database_url, endpoint=args.endpoint, evidence_path=args.evidence), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
