# DTMO Supplier and Dependency Assurance

## Purpose

DTMO depends on open-source components, container images, external intelligence sources and deployment/platform capabilities. This document defines the assurance questions that must be answered without implying guarantees that repository CI cannot establish.

## Dependency classes

| Class | Examples of concern | Assurance focus |
|---|---|---|
| Application dependencies | libraries and frameworks | provenance, vulnerability exposure, maintenance |
| Container/runtime dependencies | base images and services | versioning, patching, integrity, supported lifecycle |
| Data services | database, search, object storage | supported configuration, recovery, access controls |
| Intelligence sources | public or credentialed feeds | provenance, legal/use constraints, availability |
| Platform services | ingress, DNS, certificates, secrets | environment configuration and operational ownership |
| External assessors/suppliers | assurance or operational providers | authorization, confidentiality, independence, deliverables |

## Assurance principles

1. Dependency presence does not transfer DTMO publication authority to a supplier or connector.
2. Open-source governance and vulnerability scanning are engineering controls, not warranties of absence of vulnerabilities.
3. Runtime/platform assurance must be tied to the deployed identity being assessed.
4. Credentials and contractual restricted material are referenced, not committed.
5. Unsupported or end-of-life critical dependencies require remediation or explicit risk treatment.

## Minimum supplier/dependency record

For material dependencies record, where applicable:

- name and function;
- owner/maintainer or supplier;
- version or immutable identity;
- source/provenance;
- license/use constraints;
- support/lifecycle position;
- vulnerability-management method;
- update/patch responsibility;
- data exchanged and classification;
- credential/secret dependency;
- failure impact and fallback;
- evidence reference.

## External intelligence sources

Source onboarding must additionally consider authenticity/provenance, permitted use, rate limits, credential handling, expected freshness, normalization behavior and failure isolation. Source content is untrusted input until processed under DTMO controls.

## Production gate interaction

Material supplier or dependency risks must be represented in the risk register. Phase 10 may not infer supplier assurance merely from successful CI. Production approval requires that material dependency risks for the actual target deployment are known and acceptably treated.
