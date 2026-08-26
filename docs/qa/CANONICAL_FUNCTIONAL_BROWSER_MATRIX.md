# Canonical Functional Browser Matrix

Status: **IN PROGRESS / OWNER FUNCTIONAL RECOVERY REOPENED**

This QA contract exists because repository-green route/source contracts did not by themselves demonstrate a workable canonical product. Candidate freeze and Phase 11.10p remain blocked until required canonical functions are re-exercised and owner-observed blockers are closed.

## Slice 1 — route coverage and Administration persistence

The dedicated exact-head same-origin browser workflow must exercise the real built DTMO process without Playwright route interception and without external connector execution.

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

## Slice 2 — Threat Intelligence real read/search/filter/detail

The canonical Threat Intelligence workspace must prove both recent/default discovery from temporary PostgreSQL persistence and text/severity/relevance search through the real repository-controlled OpenSearch projection. Search failure must stay explicit and must not be converted into a false empty result. Canonical detail and Analysis/Sharing pivots must remain available without `/ui/*` compatibility paths.

## Slice 3 — IOC Explorer real inventory/filter/pivot

The canonical IOC Explorer must read a real persisted `IntelOwlEnrichmentRecord` joined to its canonical intelligence item through `/api/v1/iocs`. The browser journey must exercise indicator/context, observable type, severity, source and minimum-confidence filters against that persisted record and must prove canonical pivots to source intelligence, Analysis & Enrichment, Knowledge Graph and Investigations.

This slice must not execute IntelOwl or any other external connector. Its fixture is repository-controlled persistence only. `external_share_authorized` and `local_compromise_proven` remain false; the test must not infer maliciousness, local compromise, upstream truth or share authority from IOC presence.

## Slice 4 — Knowledge Graph persisted mapping/entity journey

The canonical Knowledge Graph must prove a deep-link from one real temporary PostgreSQL intelligence item to DTMO-persisted OpenCTI/STIX mapping context. The browser journey must load the graph through `/api/v1/opencti/items/{item_id}/graph`, render the persisted mapping node, open its entity detail through `/api/v1/opencti/entities/{mapping_id}`, and expose its persisted revision, markings, confidence and authority boundaries.

This slice deliberately runs with the live OpenCTI connector feature disabled. It must not query OpenCTI upstream, infer missing upstream relationship topology, or promote graph presence into evidence of compromise, attribution or external-share authority. `external_share_authorized` and `local_compromise_proven` remain false.

## Slice 5 — Vulnerability & Exposure verified raw-evidence journey

The canonical Vulnerability & Exposure Center must prove its real three-store read path rather than a UI-only projection. Repository-controlled vulnerability fixtures are ingested through the same-origin DTMO API so PostgreSQL receives canonical intelligence, the configured object store receives immutable raw evidence and OpenSearch receives the normal indexing attempt. The browser must then read `/api/v1/console/vulnerability-analytics?window=30d`, which verifies the raw-object SHA before projecting vulnerability attributes.

The journey must prove CVSS/EPSS/KEV plus vendor, product, CWE and minimum-EPSS filtering, and it must render the backend's canonical nested provenance fields (`source_id`, `canonical_url`, `raw_sha256`) as attributable source identity, source pivot and raw-evidence binding. The workspace must not infer local asset exposure, reachability, exploitability, compromise or remediation from vulnerability-intelligence presence.

The object store in this gate is repository-controlled and ephemeral. No OpenCVE, Vulnerability-Lookup or other external connector is executed. Passing this slice is not proof of upstream truth or production object-store readiness.

## Slice 6 — Investigations governed case-handoff journey

The canonical Investigations workspace must prove more than discovery. A repository-controlled canonical intelligence fixture with immutable raw evidence and provenance is opened through the normal deep-link path. A human-authorized `admin` browser principal must see the source, review state, provenance count and authoritative TLP restriction, provide a minimized reviewed summary and submit a case handoff through `/api/v1/thehive/items/{item_id}/cases`.

The CI job provides a repository-controlled TheHive API emulator on loopback only so the real DTMO server-side `TheHiveCaseAdapter` can exercise authorization headers, organization scoping, payload minimization, confirmed case identity and durable handoff persistence. The browser must then display the delivered case identity in handoff history while `external_share_authorized` and `local_compromise_proven` remain false. No responder execution, publication authority, upstream alerts/tasks/timeline state or subsequent live case state may be inferred.

The emulator is not a live TheHive deployment and its success is not staging, production-equivalent, penetration-test, production or independent-assurance evidence. Live TheHive health and real deployment credentials remain separate external validation requirements.

## Slice 7 — Analysis & Enrichment governed IntelOwl execution

The canonical Analysis & Enrichment workspace must prove an actual allowlisted enrichment execution rather than only rendering controls or reading pre-seeded history. A repository-controlled canonical intelligence fixture is opened through `/workbench/analysis?item=...` with a bounded domain observable. A human-authorized `admin` principal must see IntelOwl enabled with exactly the configured analyzer allowlist and invoke `Run IntelOwl` through the same-origin DTMO API.

The exact-head CI job provides a loopback IntelOwl API emulator solely to exercise the real DTMO server-side `IntelOwlAdapter`. The emulator validates the server-side bearer token, observable classification, explicit analyzer allowlist and empty connector list, returns a stable job identity, and exposes a deterministic terminal analyzer report. DTMO must persist that result as an `IntelOwlEnrichmentRecord`; the canonical browser must show the job/analyzer history both immediately and after page reload.

This slice must keep `external_share_authorized=false` and `local_compromise_proven=false`. IntelOwl enrichment is evidence, not a local-compromise verdict and not share authority. The emulator is repository-controlled integration evidence only and is not a live IntelOwl deployment, staging evidence, production-equivalent validation, penetration-test evidence or independent assurance. Cortex remains disabled in this slice and will require its own bounded analyzer-only execution proof.

## Evidence boundary

Passing these slices is repository-controlled browser evidence only. It is **not** owner acceptance, staging evidence, production-equivalent validation, penetration-test evidence, production authorization, or independent external assurance.

The following controls remain authoritative and must not be weakened by recovery work: server-side RBAC, provenance, fail-closed behavior, separate human review/share authority, responder/publication separation, and server-side credential boundaries.

## Remaining recovery

These slices do not claim that every function on every page has been proven. Recovery continues page-by-page with real read/mutation/filter/pivot/persistence/error-path journeys, fixing only verified failures one bounded change at a time. After the IntelOwl Analysis & Enrichment slice, the next bounded Analysis recovery is Cortex analyzer-only execution unless exact-head CI exposes an earlier blocker.
