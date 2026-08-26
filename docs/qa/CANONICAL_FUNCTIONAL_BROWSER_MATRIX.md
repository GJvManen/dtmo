# Canonical Functional Browser Matrix

Status: **IN PROGRESS / OWNER FUNCTIONAL RECOVERY REOPENED**

This QA contract exists because repository-green route/source contracts did not by themselves demonstrate a workable canonical product. Candidate freeze and Phase 11.10p remain blocked until required canonical functions are re-exercised and owner-observed blockers are closed.

## Slice 1 — route coverage and Administration persistence

The dedicated exact-head same-origin browser workflow must now exercise the real built DTMO process without Playwright route interception and without external connector execution.

Required canonical routes in this slice:

- Command Center;
- Threat Intelligence;
- IOC Explorer;
- Knowledge Graph;
- Vulnerability & Exposure Center;
- Investigations;
- Analysis & Enrichment;
- Sharing & Exchange;
- Automation & Playbooks;
- Sources & Collection;
- Governance & Evidence;
- Operations;
- Administration.

Every route must render its canonical heading and must not depend on `/ui/*` navigation.

Administration additionally must prove a real browser mutation through the same-origin DTMO API and temporary repository-controlled persistence: change a disabled MISP endpoint, persist it, reload the page, observe the persisted value, and restore the original fixture state. The journey must use server-authorized `admin` permissions and must not execute the MISP connector.

## Evidence boundary

Passing this slice is repository-controlled browser evidence only. It is **not** owner acceptance, staging evidence, production-equivalent validation, penetration-test evidence, production authorization, or independent external assurance.

The following controls remain authoritative and must not be weakened by recovery work: server-side RBAC, provenance, fail-closed behavior, separate human review/share authority, responder/publication separation, and server-side credential boundaries.

## Remaining recovery

This first matrix slice does not claim that every function on every page has been proven. After it is exact-head green, recovery continues page-by-page with real read/mutation/filter/pivot/persistence/error-path journeys, fixing only verified failures one bounded change at a time.
