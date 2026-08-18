# Phase 11.8g — Supply-chain governance mapping

## Purpose

This mapping records how the bounded DTMO software supply-chain controls relate to recognized secure-software and provenance practices. It is a traceability aid, not a certification claim.

| DTMO control | Governance / assurance intent | Repository evidence | Claim boundary |
|---|---|---|---|
| Exact-head build identity | Reproducible, attributable build input | exact-head checkout and build workflow | does not prove reproducibility across independent builders |
| CycloneDX SBOM | Component inventory and dependency transparency | Python and container SBOM artifacts | does not prove completeness outside the scanned build subject |
| Dependency/container vulnerability gate | Known-vulnerability risk reduction | pip-audit and container scan outputs | does not prove absence of unknown or unreported vulnerabilities |
| SHA-256 artifact identity | Immutable subject binding | wheel/image archive hashes | hash identity alone is not provenance |
| Signed provenance attestation | Build origin and workflow identity | release attestation mechanism | only actual release execution creates signed evidence |
| Signed SBOM attestation | Bind SBOM predicate to release subject | release attestation mechanism | attestation does not prove SBOM correctness by itself |
| Consumer verification | Prevent unverified artifact admission | administrator verification procedure | deployment enforcement remains later environment evidence |

## Framework relationship

The controls support the intent of secure software development and software supply-chain assurance practices, including NIST SSDF-style secure build/release governance, SLSA-style provenance, CycloneDX software component transparency and Sigstore/OIDC-backed keyless signing. DTMO does not claim formal conformance or certification merely because these mechanisms are present.

## Authority separation

Supply-chain metadata, vulnerability results and signatures are technical assurance evidence only. They do not grant external publication/share authority, TheHive case-handoff authority, Cortex responder authority or establish local compromise. Service and licensing boundaries for Taranis, IntelOwl, OpenCTI, MISP, TheHive and Cortex remain unchanged.

## Evidence transfer rule

Historical Phase 8/9 staging and assurance records are candidate-bound and cannot satisfy Phase 11.8g for a materially changed artifact. Missing exact-subject supply-chain evidence fails closed.
