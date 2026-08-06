#!/usr/bin/env python3
"""Verify that primary and observer CI evidence refer to the same successful run."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
RUN_URL_RE = re.compile(r"^https://github\.com/([^/]+/[^/]+)/actions/runs/([1-9][0-9]*)$")


class EvidenceError(ValueError):
    """Raised when release evidence is incomplete or inconsistent."""


def _load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"cannot read valid JSON evidence from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise EvidenceError(f"evidence in {path} must be a JSON object")
    return data


def verify(primary: dict[str, Any], observer: dict[str, Any]) -> dict[str, Any]:
    required_primary = {
        "schema_version",
        "workflow",
        "run_id",
        "head_sha",
        "repository",
        "conclusion",
        "run_url",
    }
    missing = sorted(required_primary - primary.keys())
    if missing:
        raise EvidenceError(f"primary evidence missing fields: {', '.join(missing)}")

    run_id = str(primary["run_id"])
    head_sha = str(primary["head_sha"]).lower()
    repository = str(primary["repository"])
    run_url = str(primary["run_url"])
    if primary["workflow"] != "RC4 Quality Gate":
        raise EvidenceError("primary evidence is not from RC4 Quality Gate")
    if primary["conclusion"] != "success":
        raise EvidenceError("primary quality gate did not conclude successfully")
    if not run_id.isdigit() or int(run_id) < 1:
        raise EvidenceError("primary run_id must be a positive integer")
    if not SHA_RE.fullmatch(head_sha):
        raise EvidenceError("primary head_sha must be a full lowercase commit SHA")
    match = RUN_URL_RE.fullmatch(run_url)
    if not match or match.group(1) != repository or match.group(2) != run_id:
        raise EvidenceError("primary run_url does not match repository and run_id")

    observed = {
        "run_id": str(observer.get("observed_run_id", observer.get("run_id", ""))),
        "head_sha": str(observer.get("observed_head_sha", observer.get("head_sha", ""))).lower(),
        "conclusion": observer.get("observed_conclusion", observer.get("conclusion")),
        "run_url": str(observer.get("observed_url", observer.get("run_url", ""))),
        "workflow": observer.get("observed_workflow", observer.get("workflow")),
    }
    expected = {
        "run_id": run_id,
        "head_sha": head_sha,
        "conclusion": "success",
        "run_url": run_url,
        "workflow": "RC4 Quality Gate",
    }
    mismatches = [key for key, value in expected.items() if observed[key] != value]
    if mismatches:
        raise EvidenceError(f"observer evidence mismatch: {', '.join(mismatches)}")

    return {
        "verified": True,
        "repository": repository,
        "workflow": "RC4 Quality Gate",
        "run_id": run_id,
        "head_sha": head_sha,
        "conclusion": "success",
        "run_url": run_url,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary", type=Path)
    parser.add_argument("observer", type=Path)
    args = parser.parse_args()
    try:
        result = verify(_load(args.primary), _load(args.observer))
    except EvidenceError as exc:
        print(f"CI evidence verification failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
