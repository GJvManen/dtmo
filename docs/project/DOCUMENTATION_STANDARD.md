# DTMO Documentation Standard

Version: **1.0**  
Effective: **2026-08-12**

## Purpose

DTMO documentation must remain useful as professional product, architecture, security, governance and assurance documentation throughout continuous development.

Operational implementation history is valuable evidence, but it must not overwrite the stable documentation layers that explain what DTMO is, how it works, what its trust boundaries are and what remains before production.

This standard defines that separation.

## Documentation classes

### Class A — stable professional documentation

Examples:

- root `README.md`;
- `docs/README.md`;
- System Architecture;
- Frontend UX Architecture;
- Security Overview;
- Governance Mapping Registry;
- Source Catalog;
- Executive Status;
- Current State;
- Production Readiness Report;
- Production Checklist;
- QA and Release Gates;
- formal phase acceptance gates;
- release notes;
- roadmap.

These documents must primarily describe:

- platform purpose and scope;
- capabilities and architecture;
- data and trust boundaries;
- security/privacy/governance controls;
- accepted current state;
- formal limitations and known gaps;
- formal next-phase requirements;
- stable links to deeper evidence.

They must **not** become chronological PR/incident logs.

### Class B — operational and immutable evidence

Examples:

- `docs/development/RUN_LOG.md`;
- `docs/development/runs/`;
- CI artifacts;
- GitHub issues;
- pull-request descriptions/comments;
- test/evidence artifacts;
- point-in-time investigation records.

These may contain:

- exact PR/commit/workflow identifiers;
- failed checks;
- root-cause findings;
- temporary blockers;
- incident chronology;
- owner retest transcripts;
- release-gate evidence state at a point in time.

**Historical immutable run records** are point-in-time audit evidence and must never be rewritten to make a later state appear green. New evidence is recorded in a new run/evidence record.

### Class C — operational procedures

Examples:

- Operations Manual;
- runbooks;
- backup/restore procedures;
- deployment procedures;
- incident-response procedures.

These contain actionable procedures but should remain written as durable instructions, not as incident diaries.

## Content separation rules

### Rule 1 — no PR chronology in project homepage

The root README may state release/phase status, but should not list repair PRs or transient CI state. Detailed history belongs in release notes/run evidence.

### Rule 2 — architecture is architecture

System Architecture must preserve:

- logical components;
- data flows;
- persistence responsibilities;
- identity/authorization model;
- trust boundaries;
- deployment boundaries;
- security invariants;
- planned architectural extensions where relevant.

Temporary implementation defects may justify an architecture correction, but the document must not be replaced by defect chronology.

### Rule 3 — current state is decision-oriented

`CURRENT_STATE.md` may describe current accepted capabilities, known limitations and active workstreams. It should avoid detailed workflow IDs, test logs and incident timelines.

### Rule 4 — executive documentation is concise and decision-focused

Executive Status should answer:

- what is accepted;
- what is not accepted;
- what can happen next;
- what remains before production;
- what the principal risks/control boundaries are.

### Rule 5 — exact evidence belongs in evidence records

Exact SHAs, workflow IDs, job logs and point-in-time release decisions belong in immutable run/evidence records unless they are necessary to identify a formal release baseline.

### Rule 6 — framework claims remain truthful

Professional documentation may summarize framework coverage, but mappings must come from the authoritative mapping model/registry. Missing mappings remain `UNMAPPED` or `CONTEXT_ONLY`; documentation must not infer equivalence.

### Rule 7 — security boundaries may not be simplified away

Professional revisions must preserve authoritative statements on:

- RBAC and least privilege;
- service-account/human separation;
- separation of duties;
- provenance;
- privacy/data minimization;
- secret handling;
- human review and separate external-share approval;
- no publication authority from technical execution;
- evidence/claim boundaries.

### Rule 8 — current phase state must be consistent

The following documents must agree on the formal lifecycle:

- root README;
- docs README;
- Current State;
- Executive Status;
- Production Readiness Report;
- Production Checklist;
- QA and Release Gates;
- relevant phase gate;
- Roadmap;
- current release notes.

A status reconciliation must update this set as one controlled documentation change where applicable.

## Change process

Professional documentation changes follow the same protected workflow as code:

1. create a branch from current `main`;
2. update the professional documentation set consistently;
3. preserve immutable run records;
4. add a new run/evidence record when a lifecycle transition requires audit evidence;
5. run the complete exact-head CI matrix;
6. merge only after every returned required workflow is `completed/success`;
7. use expected-head merge protection.

## Documentation quality checklist

Before merge, verify:

- [ ] root README is product-oriented rather than operational;
- [ ] docs portal links to all major building blocks;
- [ ] architecture retains full layered design and trust boundaries;
- [ ] current lifecycle is consistent across professional docs;
- [ ] production limitations are explicit;
- [ ] security/governance invariants remain explicit;
- [ ] operational chronology is confined to the evidence layer;
- [ ] no raw secrets/personal data are introduced;
- [ ] framework mapping claims are evidence-backed;
- [ ] immutable run records were not rewritten;
- [ ] links/file names are valid;
- [ ] open-source governance entry points remain present.

## Current application of this standard

The 2026-08-12 documentation restoration re-establishes the professional structure after repeated release-status reconciliations had shortened several high-level documents and mixed transient operational state into the project-facing documentation.

Future status updates must use this standard to prevent that regression from recurring.
