# Phase 11.10h — TheHive Investigations Workspace Gate

## Status

`IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`

## Acceptance objective

Accept the canonical `/workbench/investigations` workspace only when one exact PR head proves the repository-controlled investigation/read projection, explicit human case handoff, durable reconciliation behavior and professional documentation together.

## Required evidence on the final exact head

1. Frontend dependency graph installed with `npm ci` and manifests unchanged.
2. React/TypeScript workbench typechecks and builds.
3. Phase 11.10h repository contract passes.
4. Phase 11.10h investigation-state API tests pass.
5. Existing Phase 11.6 TheHive adapter/state/contract regressions pass.
6. Current Phase 11.10 professional lifecycle documentation contract passes.
7. Chromium browser acceptance proves:
   - canonical deep-link investigation loading;
   - attributable canonical/provenance/handoff evidence;
   - explicit human case-handoff action through DTMO API;
   - durable result reload after mutation;
   - `reserved`/`ambiguous` state blocks blind UI replay;
   - unavailable state is not converted into case/health/compromise claims;
   - no browser publish/share/responder authority.
8. Non-sensitive exact-head repository evidence artifact is produced.
9. Professional current-state, architecture, user, security, QA, evidence-index, roadmap and portal documentation is synchronized.

## Dedicated workflow

`.github/workflows/phase11-thehive-investigations.yml`

Workflow name: `Phase 11 TheHive Investigations Workspace Gate`.

## Security and authority invariants

Acceptance must preserve all of the following:

- `read:intelligence` for investigation-state reads;
- `handoff:case` for case mutation;
- service accounts cannot authorize human case handoff;
- canonical provenance required;
- TLP/PAP and authoritative handling fail closed;
- server-side TheHive token and organization context only;
- durable request reservation before mutation;
- ambiguous delivery requires reconciliation rather than blind replay;
- no external-share authority;
- no local-compromise inference;
- no responders or automatic remediation;
- no synthetic alerts/tasks/timeline/upstream case readback.

## Evidence boundary

A green repository/browser gate does not prove live TheHive health, license entitlement, production credentials/RBAC, organization membership, real-data handling approval, upstream case completeness, responder/remediation execution, production-equivalent continuity, independent assurance or production authorization.

Phase 10 remains `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`. Phase 11.10p remains the later candidate-bound production-equivalent validation step after 11.10a–o completion and immutable candidate freeze.

## Merge rule

Do not merge while any workflow registered for the final exact head is queued, in progress, failed, skipped, cancelled or otherwise not `completed/success`. The PR must be mergeable, documentation synchronized, ready for review and the verified head unchanged. Merge only with expected-head protection.

## Next priority after acceptance

**Phase 11.10i — Vulnerability & Exposure**.
