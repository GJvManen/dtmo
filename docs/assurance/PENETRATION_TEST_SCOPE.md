# DTMO Penetration Test Scope and Rules of Engagement

## Purpose

This document defines the controlled preparation framework for an independent DTMO penetration test. It is a planning and authorization template only. It does not assert that testing has been commissioned, executed or accepted.

## Preconditions

Testing may begin only after the accountable parties have recorded:

- approved production-equivalent staging environment;
- immutable deployment identity;
- target URLs, addresses and exposed services;
- test window and emergency contacts;
- assessor organization and named lead;
- authorization to test;
- data-handling and evidence-transfer method;
- explicit exclusions and prohibited techniques.

Until those fields are completed, external penetration testing is `NOT STARTED`.

## Scope domains

The final engagement should consider, where present in the approved target identity:

1. canonical DTMO web console and authentication flows;
2. API endpoints and authorization boundaries;
3. source/connector registration and execution surfaces;
4. Administration and RBAC functions;
5. Governance and external-share approval boundaries;
6. Visual Analytics and same-origin integrations;
7. storage/search interfaces exposed through application trust boundaries;
8. deployment ingress, TLS and security headers;
9. session, token and service-account controls;
10. abuse resistance, input validation and error handling.

## Required test perspectives

The assessor should include unauthenticated, least-privileged authenticated and appropriately authorized privileged perspectives. Privileged credentials must be purpose-created, time-bounded and removed or rotated after the engagement.

## Rules of engagement

Unless explicitly authorized otherwise, the engagement must prohibit:

- destructive denial-of-service or uncontrolled stress testing;
- attacks against systems outside the recorded target identity;
- social engineering of unrelated personnel;
- persistence beyond what is required to demonstrate a finding;
- uncontrolled extraction of sensitive or personal data;
- modification or deletion of production-equivalent evidence without recovery coordination;
- external publication of findings without accountable authorization.

Proofs should demonstrate impact using the minimum data and system modification necessary.

## Finding severity

The assessor should provide severity, exploitability, affected asset, prerequisites, impact, reproducibility and remediation guidance. CVSS may be supplied as context when appropriate, but DTMO must not claim an internal first-class CVSS mapping unless the project mapping model explicitly supports it.

## Evidence requirements

Every finding must identify the assessed deployment identity and sufficient reproducibility evidence. Evidence must avoid unnecessary credentials, tokens and personal data. Sensitive artifacts should be transferred using the approved restricted channel rather than committed to the repository.

## Stop conditions

Testing must stop and the emergency contact must be engaged if the assessment causes unexpected loss of availability, integrity risk to canonical state, uncontrolled data disclosure, impact outside the approved target or another condition defined in the signed rules of engagement.

## Acceptance boundary

Completion of testing is not equivalent to Phase 9 acceptance. Material findings require triage, remediation or explicit accountable treatment, retesting where required, and final disposition under the Phase 9 gate.
