#!/usr/bin/env python3
"""Assess repository-side readiness for observable CI execution.

This preflight deliberately does not claim that GitHub Actions executed. It verifies
that the repository contains the minimum configuration needed for an external run
to produce release evidence and emits a machine-readable, non-gate-eligible report.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


class PreflightError(ValueError):
    """Raised when repository-side CI execution prerequisites are incomplete."""


def _load_workflow(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise PreflightError(f"cannot load workflow {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise PreflightError(f"workflow {path} must be a YAML mapping")
    return data


def assess(root: Path) -> dict[str, Any]:
    primary_path = root / ".github/workflows/ci.yml"
    observer_path = root / ".github/workflows/ci-observer.yml"
    verifier_path = root / "tools/verify_ci_evidence.py"

    primary = _load_workflow(primary_path)
    observer = _load_workflow(observer_path)
    triggers = primary.get("on", primary.get(True, {}))
    if not isinstance(triggers, dict):
        raise PreflightError("primary workflow triggers must be a mapping")

    required_triggers = {"push", "pull_request", "workflow_dispatch"}
    missing_triggers = sorted(required_triggers - set(triggers))
    if missing_triggers:
        raise PreflightError(f"primary workflow missing triggers: {', '.join(missing_triggers)}")

    jobs = primary.get("jobs")
    if not isinstance(jobs, dict) or "workflow-contracts" not in jobs:
        raise PreflightError("primary workflow missing workflow-contracts job")

    observer_triggers = observer.get("on", observer.get(True, {}))
    if not isinstance(observer_triggers, dict) or "workflow_run" not in observer_triggers:
        raise PreflightError("observer workflow missing workflow_run trigger")

    workflow_run = observer_triggers["workflow_run"]
    workflows = workflow_run.get("workflows", []) if isinstance(workflow_run, dict) else []
    if "RC4 Quality Gate" not in workflows:
        raise PreflightError("observer is not bound to RC4 Quality Gate")

    if not verifier_path.is_file():
        raise PreflightError("deterministic CI evidence verifier is missing")

    return {
        "schema_version": 1,
        "scope": "repository_ci_execution_preflight",
        "ready": True,
        "release_gate_eligible": False,
        "primary_workflow": str(primary_path.relative_to(root)),
        "observer_workflow": str(observer_path.relative_to(root)),
        "verifier": str(verifier_path.relative_to(root)),
        "required_external_evidence": [
            "successful RC4 Quality Gate workflow run",
            "workflow-contract-evidence artifact",
            "successful linked RC4 CI Observer run",
            "ci-observation-evidence artifact",
            "successful deterministic evidence-pair verification",
        ],
        "statement": (
            "Repository configuration is ready for execution validation; this report "
            "is not proof that GitHub Actions ran and cannot satisfy the release gate."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = assess(args.root.resolve())
    except PreflightError as exc:
        print(f"CI execution readiness preflight failed: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
