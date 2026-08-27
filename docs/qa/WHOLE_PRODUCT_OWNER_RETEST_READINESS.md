# Whole-product owner retest readiness

## Status

`REPOSITORY PREPARATION IN PROGRESS / EXTERNAL OWNER RETEST REQUIRED`

The 2026-08-26 external owner functional rejection remains authoritative until the complete product is exercised again from a **clean supported installation** and the owner explicitly accepts that retest. Repository CI cannot manufacture that acceptance.

## Purpose

This readiness gate composes the previously bounded functional-recovery journeys into one exact-head repository-controlled browser run. The run is intended to catch regressions before the external owner retest and to ensure the recently deepened Governance & Evidence and Operations journeys are not omitted from the whole-product candidate.

A green repository run **does not constitute owner acceptance**. It is preparation evidence only.

## Required canonical coverage

The composed same-origin gate must cover the canonical Command Center, Threat Intelligence, IOC Explorer, Knowledge Graph, Vulnerability & Exposure Center, Investigations, Analysis & Enrichment, Sharing & Exchange, Automation & Playbooks, Sources & Collection, Governance & Evidence, Operations and Administration surfaces.

The browser must use the built exact-head DTMO workbench and same-origin DTMO APIs. No required journey may depend on a `/ui/*` compatibility route. Browser route interception is prohibited for the composed gate.

Deep journeys remain required where the historical owner rejection identified empty, inert or disconnected behavior. The composed gate therefore includes persistence-backed discovery, filters, pivots and durable state; governed TheHive and IntelOwl adapter execution through bounded loopback emulators; explicit Governance framework/control/provenance drill-down; and persisted Operations connector runtime/run evidence.

## Clean-install boundary

The repository-controlled gate uses ephemeral CI services and bounded emulators. It is not a clean external installation and does not prove that Docker Desktop, Compose topology, external licensed prerequisites, local credentials, networking, browser environment or operator bootstrap behave correctly on an independently provisioned workstation.

The external owner retest must therefore start from a clean supported installation using the authoritative installation procedure. It must verify at minimum:

1. startup/preflight completes with all required prerequisites and actionable blockers;
2. the canonical application is reachable without legacy-primary navigation;
3. bundled core services and visual analytics are reachable through the supported product path;
4. supported bootstrap/source flows produce meaningful attributable content;
5. every canonical workspace exposes a usable read/action/result loop appropriate to its authority boundary;
6. persistence survives normal reload/revisit flows;
7. fail-closed missing external integrations remain clear and actionable rather than blank or falsely healthy;
8. RBAC, server-side credentials, provenance and separate human review/share/publication authority remain enforced.

## Release boundary

Until that external owner retest is explicitly accepted, **candidate freeze remains blocked** and **production-equivalent validation remains blocked**. A green exact-head whole-product repository gate is not staging evidence, production-equivalent evidence, penetration-test evidence, independent assurance or production authorization.

If the external owner retest identifies a defect, only the verified root cause should be repaired. Any repository change creates a new candidate identity and requires fresh exact-head repository evidence before the owner retest is repeated.
