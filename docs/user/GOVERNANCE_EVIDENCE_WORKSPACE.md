# Governance & Evidence Workspace

The canonical **Governance & Evidence** workspace is available at `/workbench/governance`. It shows repository-backed framework coverage, explicit mappings, provenance and separation-of-duties boundaries through DTMO-owned APIs.

## Reading framework status

A framework labelled **unmapped** is intentionally not treated as implemented, compliant or equivalent to another framework. Normenkader IBP and MITRE ATT&CK therefore remain explicit gaps until governed repository-backed control or technique mappings exist. CVSS may appear as context-only where no first-class score/vector mapping exists.

## Reading mappings and evidence

Mappings are shown with their source document and section. A displayed mapping proves only that DTMO has an explicit repository-backed statement at that provenance location. It does not prove operational effectiveness, external assurance, audit acceptance, production readiness or production authorization.

## Authority boundaries

Governance visibility is read-only. It does not grant review, case-creation, connector execution, remediation, external sharing, publication or administrative authority. Human review/share/publication decisions remain governed by their separate server-side permissions and workflows.

If governance knowledge cannot be loaded, the workspace fails closed and does not synthesize a healthy or compliant state.
