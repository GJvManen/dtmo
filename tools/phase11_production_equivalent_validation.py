from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_EVIDENCE_CLASSES = (
    "immutable_candidate_identity",
    "migration_compatibility",
    "upgrade",
    "rollback",
    "health",
    "saturation",
    "recovery",
)


def build_contract() -> dict[str, object]:
    return {
        "phase": "11.10",
        "status": "IN_PROGRESS",
        "candidate_identity_policy": "single immutable integrated deployment identity",
        "required_evidence_classes": list(REQUIRED_EVIDENCE_CLASSES),
        "historical_phase8_evidence_reusable": False,
        "fresh_candidate_bound_evidence_required": True,
        "same_candidate_required_for_phase11_11": True,
        "missing_or_ambiguous_evidence": "FAIL_CLOSED",
        "production_authorized": False,
    }


def main() -> None:
    print(json.dumps(build_contract(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
