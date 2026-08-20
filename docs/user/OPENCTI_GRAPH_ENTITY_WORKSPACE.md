# OpenCTI Graph / Entity Workspace

Status: **Phase 11.10f / IN PROGRESS**

## What this workspace shows

Open **Intelligence → Knowledge Graph** or `/workbench/intelligence/graph` and provide a canonical DTMO intelligence-item UUID.

The workspace shows only OpenCTI/STIX context that DTMO has already persisted for that item. The central node is the canonical DTMO intelligence object. Each surrounding node is a persisted OpenCTI mapping. Selecting an entity opens its attributable identity, STIX type, confidence, markings, references and immutable DTMO revision history.

## What the graph does not claim

The current persistence boundary does not store OpenCTI entity-to-entity topology. For that reason, DTMO draws only `canonical-mapping` edges between the DTMO item and persisted OpenCTI entities. It does not guess relationships between OpenCTI objects.

A blank mapping graph means **no persisted mapping evidence for this DTMO item**. It does not mean OpenCTI has no relevant data.

## Capability status

The status strip separates:

- feature enabled/disabled;
- configuration present/not established;
- runtime health — deliberately **not inferred** from configuration;
- relationship topology — `not persisted` unless a future accepted persistence boundary proves otherwise.

## Authority

This workspace is read-only and requires `read:intelligence`. It grants no publication/share approval, case mutation, connector execution or administrative authority.

OpenCTI graph/entity presence, confidence or markings do not prove local exposure, exploitability, compromise, attribution certainty or remediation state.

## Failure behavior

If canonical graph data cannot be loaded, the workspace reports **Graph context unavailable**. It does not convert a dependency failure into an empty graph.

If entity detail cannot be loaded, the selected entity remains unavailable rather than being reconstructed from incomplete display data.

## Evidence classification

Screenshots, browser fixtures and repository CI for this workspace are engineering evidence only. They do not prove live OpenCTI health, production-equivalent operation, independent assurance or production authorization.
