# Canonical Functional Browser Matrix

Status: **IN PROGRESS / WHOLE-PRODUCT OWNER RETEST PREPARATION**

This QA contract exists because repository-green route/source contracts did not by themselves demonstrate a workable canonical product. Candidate freeze and Phase 11.10p remain blocked until required canonical functions are re-exercised from a clean supported installation and the external owner explicitly accepts the whole-product retest.

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

This slice must keep `external_share_authorized=false` and `local_compromise_proven=false`. IntelOwl enrichment is evidence, not a local-compromise verdict and not share authority. The emulator is repository-controlled integration evidence only and is not a live IntelOwl deployment, staging evidence, production-equivalent validation, penetration-test evidence or independent assurance.

## Slice 8 — Analysis & Enrichment governed Cortex analyzer-only execution

The canonical Analysis & Enrichment workspace must also prove an actual Cortex analyzer execution through the existing server-side adapter. A repository-controlled canonical intelligence item is opened by deep link with a bounded domain observable. A human-authorized `admin` principal must see Cortex enabled with exactly one configured analyzer and invoke `Run Cortex` through `/api/v1/analysis/items/{item_id}/cortex`.

The dedicated exact-head gate provides a loopback Cortex API emulator solely to exercise the real `CortexAdapter`. The emulator validates the server-side bearer token, approved observable type, explicit analyzer allowlist, TLP value and analyzer-only request shape, returns a stable job identity and exposes a deterministic terminal report. DTMO must persist the result as a `CortexAnalysisRecord`; the browser must show the job, analyzer, TLP and persisted report immediately and again after a full page reload.

Cortex responders, analyzer discovery and other side-effect actions remain outside this approved boundary. `external_share_authorized=false` and `local_compromise_proven=false` remain authoritative. Passing the emulator-backed journey does not prove live Cortex deployment health, upstream truth, compromise, owner acceptance, staging, production-equivalent validation or independent assurance.

## Slice 9 — Sharing & Exchange separate-human approval and unpublished MISP delivery

The canonical Sharing & Exchange workspace must prove the complete governed browser decision chain rather than only mocked API rendering. One repository-controlled canonical intelligence item begins as an unreviewed, unapproved candidate. A first human-authorized browser principal records the review through the real same-origin API and must then be blocked from approving sharing for that same item. A second human-authorized principal performs the separate share approval.

Only after both durable decisions are present may the second principal invoke the real server-side MISP export path. The dedicated exact-head gate supplies a loopback MISP API emulator that validates the server-side API key and the bounded event payload, including `published=false`, distribution, TLP, deterministic UUID and non-IDS canonical evidence link. DTMO must persist successful delivery evidence and replay protection; after a full page reload the export history must remain visible and the same canonical revision must no longer be exportable automatically.

This slice grants no MISP publication or synchronization authority. It does not prove live MISP health or upstream truth, and the emulator is not owner acceptance, staging evidence, production-equivalent validation, penetration-test evidence or independent assurance. Server-side RBAC, separate human review/share authority and replay protection remain authoritative.

## Slice 10 — Automation & Playbooks real trigger and reversible control-plane rollback

The canonical Automation & Playbooks workspace must prove a real bounded trigger rather than the existing route-intercepted browser fixture. A human-authorized `admin` principal selects the built-in CISA KEV playbook and invokes the existing same-origin `/connectors/cisa-kev/run` path. The exact-head gate supplies a repository-controlled loopback CISA KEV payload while DTMO executes its real connector, canonical ingestion and persistence path. The trigger must create attributable canonical intelligence and record the built-in connector's latest durable runtime state so Source Center observation reports the successful run after the browser refreshes state.

The same workspace must expose supported governed registered sources from Source Center without creating a second orchestration plane. For one enabled repository-controlled registered source, the browser must use the existing server-authorized source update API to pause its `enabled` state and then expose a bounded rollback for that pause. Rollback restores only the enabled state changed by the current browser session. Only one unresolved rollback may exist in the workspace at a time, and the rollback token must not disappear merely because the operator selects another playbook.

The rollback is intentionally narrow: it cannot delete canonical intelligence, immutable/raw evidence, audit records or connector health history, cannot reverse an upstream side effect that already happened, and cannot mutate the scheduler. Trigger or rollback success grants no remediation, case-creation, review, external-share, publication or production authority. The loopback source and ephemeral repository-controlled raw store are exact-head integration evidence only and are not live upstream, staging, production-equivalent, penetration-test or independent-assurance evidence.

## Slice 11 — Governance & Evidence deep traceability

The canonical Governance & Evidence workspace must expose repository-backed framework provenance, explicit typed DTMO control mappings and implementation references through the same-origin governance contract. The browser journey must prove a framework → DTMO control → repository evidence drill-down including Normenkader IBP, MITRE ATT&CK and CVSS context where explicit mappings exist.

No missing relationship may be inferred. CVSS remains context-only, and framework visibility must not be rendered as certification, blanket compliance, control effectiveness or production assurance. Governance visibility grants no review, case, connector, sharing, publication, administration or production authority.

## Slice 12 — Operations deep persisted runtime evidence

The canonical Operations workspace must distinguish connector capability from actual DTMO-observed runtime evidence. A PostgreSQL-backed browser journey must render persisted connector runtime state and recent connector health events, including last run identity, success/failure timing, degraded/isolated state, record counts and quarantine counts.

Raw quarantined evidence, credentials and execution payloads must not be exposed. Operations remains read-only and grants no connector execution, configuration, review, sharing, publication or responder authority. Persisted DTMO runtime state is operational evidence only; it is not proof of live upstream health or production readiness.

## Slice 13 — composed whole-product owner retest preparation

The central same-origin workflow must execute the route matrix and all deep recovery journeys together on one exact PR head, including the Governance and Operations journeys added after the earlier owner rejection. The composed run must use real same-origin DTMO HTTP, temporary PostgreSQL/object-store state and only bounded repository-controlled integration emulators where live external services are deliberately outside repository CI.

This composed run is a regression-prevention prerequisite for the **whole-product owner retest**. It does not replace that retest. The external owner retest must still start from a clean supported installation and explicitly determine whether the integrated product is professionally usable.

## Evidence boundary

Passing these slices is repository-controlled browser evidence only. It is **not** owner acceptance, clean external installation evidence, staging evidence, production-equivalent validation, penetration-test evidence, production authorization, or independent external assurance.

The following controls remain authoritative and must not be weakened by recovery work: server-side RBAC, provenance, fail-closed behavior, separate human review/share authority, responder/publication separation, and server-side credential boundaries.

## Remaining recovery

Governance & Evidence and Operations deep journeys are now part of the required composed repository gate. The next lifecycle step after that exact-head gate is green is the **whole-product owner retest from a clean supported installation**. Candidate freeze and Phase 11.10p production-equivalent validation remain blocked until that external owner retest is explicitly accepted. Any defect found by the retest must be fixed as a bounded root-cause slice and requires fresh exact-head repository evidence before repeating the retest.
