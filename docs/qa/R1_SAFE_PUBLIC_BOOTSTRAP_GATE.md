# R1 Safe Public Bootstrap Gate

Status: **ACTIVE / repository-controlled**

## Purpose

Verify that the supported local/reference profile starts useful public collection without requiring upstream secrets while all credential-bearing external framework integrations remain fail-closed.

## Required local/reference defaults

- server-owned live connector scheduler enabled;
- built-in CISA KEV collection available through that scheduler;
- CIRCL Vulnerability-Lookup enabled against its public read endpoint without an API token;
- OpenCVE remains disabled until its organization token is configured;
- MISP, AIL, Taranis AI, IntelOwl, Cortex, OpenCTI and TheHive remain explicit external configuration tasks.

## Evidence boundary

A green repository gate proves the configuration and documentation contract only. It does not prove current upstream availability, source completeness, production-equivalent execution, local exposure, compromise, remediation, penetration-test results, independent assurance or production authorization.

## Security boundary

No secret is added to source control or returned to the browser. RBAC, provenance, fail-closed configuration and explicit human review/share/publication authority remain unchanged.
