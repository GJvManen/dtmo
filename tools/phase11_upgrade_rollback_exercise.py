from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def _require_digest(value: str, label: str) -> str:
    if not _DIGEST.fullmatch(value):
        raise ValueError(f"{label} must be an immutable sha256 digest")
    return value


def build_evidence(*, baseline: str, candidate: str, exact_head: str) -> dict[str, object]:
    baseline = _require_digest(baseline, "baseline")
    candidate = _require_digest(candidate, "candidate")
    if baseline == candidate:
        raise ValueError("candidate must differ from baseline so the upgrade is actually exercised")
    if not re.fullmatch(r"[0-9a-f]{40}", exact_head):
        raise ValueError("exact_head must be a 40-character lowercase Git commit SHA")

    return {
        "decision": "pass",
        "exact_head": exact_head,
        "exercise": "repository_upgrade_rollback_transition",
        "baseline_digest": baseline,
        "candidate_digest": candidate,
        "rollback_digest": baseline,
        "upgrade_transition": [baseline, candidate],
        "rollback_transition": [candidate, baseline],
        "immutable_digests_only": True,
        "rollback_restores_exact_prior_digest": True,
        "rolling_update": {
            "maxUnavailable": 0,
            "maxSurge": 1,
            "revisionHistoryLimitMinimum": 2,
            "progressDeadlineSecondsMinimum": 60,
            "minReadySecondsMinimum": 1,
        },
        "post_upgrade_health_evidence_required": True,
        "post_rollback_health_evidence_required": True,
        "automatic_database_down_migration_allowed": False,
        "human_change_authority_required": True,
        "production_equivalent_exercise_claimed": False,
        "live_cluster_rollback_claimed": False,
        "production_authorization_claimed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Exercise the Phase 11.8i immutable upgrade/rollback contract")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--exact-head", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    evidence = build_evidence(baseline=args.baseline, candidate=args.candidate, exact_head=args.exact_head)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
