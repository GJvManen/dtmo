# Repository branch hygiene

## Purpose

DTMO retains a large historical branch set. Cleanup must reduce obsolete working refs without deleting release, evidence, candidate, current-development or otherwise unreviewed history.

Branch age alone is never a deletion criterion.

## Read-only inventory

Run from a current clone:

```bash
python3 tools/branch_hygiene_inventory.py --base main
```

Use `--json` when a machine-readable review record is needed.

The tool is intentionally read-only and produces three classifications:

- `RETAIN`: default/base refs and release/evidence namespaces that must not be proposed for deletion by this tool;
- `RETAIN_REVIEW`: the branch tip is not contained in `main` and therefore must be retained pending explicit disposition;
- `DELETE_ELIGIBLE_REVIEW`: the branch tip is already an ancestor of `main`, but deletion is still prohibited until a human verifies there is no open PR, release/candidate purpose, audit/evidence dependency or other retention reason.

The namespaces `audit/`, `candidate-`, `release/`, `releases/` and `evidence/` are retained by default even when their tips are already contained in `main`.

## Deletion gate

A remote branch may be deleted only when all of the following are true:

1. the exact branch tip is already contained in the current `main` history, or an explicit accountable decision documents why an unmerged ref is obsolete;
2. the branch is not the default branch and is not protected;
3. no open pull request uses the branch as its head;
4. the branch is not required for an active release, frozen candidate, rollback, audit or evidence record;
5. the deletion target and tip SHA are recorded before mutation.

If any condition cannot be verified, retain the branch.

## Scope boundary

This hygiene process changes Git refs only. It does not rewrite `main`, squash historical evidence, reinterpret old CI as current evidence, or change product/security behavior. Candidate-bound, production-equivalent, staging, penetration-test and independent-assurance evidence retain their original identity boundaries.
