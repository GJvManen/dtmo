#!/usr/bin/env python3
"""Inventory remote branches for conservative repository hygiene.

This tool is intentionally read-only. It never deletes refs. A branch is only marked
DELETE_ELIGIBLE_REVIEW when its tip is already an ancestor of the selected base and
its name is not in a retained namespace. Operators must still verify that there is
no open PR or evidence/release reason to keep the ref before deletion.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass


RETAIN_PREFIXES = ("audit/", "candidate-", "release/", "releases/", "evidence/")


@dataclass(frozen=True)
class BranchRecord:
    branch: str
    tip: str
    merged_into_base: bool
    classification: str
    reason: str


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def is_ancestor(tip: str, base: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", tip, base],
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def inventory(base: str, remote: str) -> list[BranchRecord]:
    git("fetch", "--prune", remote)
    refs = git(
        "for-each-ref",
        "--format=%(refname:short) %(objectname)",
        f"refs/remotes/{remote}/",
    ).splitlines()
    records: list[BranchRecord] = []
    for line in refs:
        if not line:
            continue
        ref, tip = line.split(maxsplit=1)
        prefix = f"{remote}/"
        if not ref.startswith(prefix):
            continue
        branch = ref[len(prefix) :]
        if branch in {"HEAD", base}:
            records.append(BranchRecord(branch, tip, True, "RETAIN", "base/default ref"))
            continue
        if branch.startswith(RETAIN_PREFIXES):
            records.append(
                BranchRecord(branch, tip, is_ancestor(tip, f"{remote}/{base}"), "RETAIN", "release/evidence namespace")
            )
            continue
        merged = is_ancestor(tip, f"{remote}/{base}")
        if merged:
            records.append(
                BranchRecord(
                    branch,
                    tip,
                    True,
                    "DELETE_ELIGIBLE_REVIEW",
                    "tip is already contained in base; verify no open PR/evidence dependency before deletion",
                )
            )
        else:
            records.append(BranchRecord(branch, tip, False, "RETAIN_REVIEW", "tip is not contained in base"))
    return sorted(records, key=lambda item: item.branch)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="main")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    records = inventory(args.base, args.remote)
    if args.json:
        print(json.dumps([asdict(record) for record in records], indent=2, sort_keys=True))
    else:
        for record in records:
            print(f"{record.classification:24} {record.branch:70} {record.tip}  {record.reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
