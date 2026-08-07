from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from dtmo.connectors.provenance import IngestionContext, normalize_connector_records


def build_evidence() -> dict[str, object]:
    context = IngestionContext(
        connector_id="cisa-kev-canary",
        run_id=UUID("22222222-2222-4222-8222-222222222222"),
        source_uri="https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        fetched_at=datetime(2026, 8, 7, 5, 40, tzinfo=UTC),
        confidence=95,
    )
    result = normalize_connector_records(
        [
            {"cveID": "CVE-2026-0001", "dateAdded": "2026-08-06", "vulnerabilityName": "Evidence fixture"},
            {"cveID": "CVE-2026-0001", "dateAdded": "2026-08-07", "vulnerabilityName": "Duplicate fixture"},
            {"dateAdded": "2026-08-07"},
        ],
        context=context,
        external_id_field="cveID",
        source_timestamp_field="dateAdded",
    )
    candidate = result.candidates[0]
    return {
        "schema_version": 1,
        "decision": "pass" if len(result.candidates) == 1 and len(result.quarantined) == 2 else "blocked",
        "connector_id": candidate.connector_id,
        "run_id": str(candidate.run_id),
        "source_uri": candidate.source_uri,
        "source_timestamp": candidate.source_timestamp,
        "fetched_at": candidate.fetched_at.isoformat(),
        "payload_digest": candidate.payload_digest,
        "confidence": candidate.confidence,
        "quarantine_reasons": sorted(item.reason for item in result.quarantined),
        "duplicate_count": result.duplicate_count,
        "publish_approved": result.publish_approved,
        "candidate_publish_approved": candidate.publish_approved,
        "quarantine_publish_approved": all(item.publish_approved is False for item in result.quarantined),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_evidence(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
