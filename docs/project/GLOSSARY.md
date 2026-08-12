# DTMO Glossary

This glossary defines terminology used in the professional DTMO documentation. Where implementation-specific names differ, the authoritative API, schema or architecture document takes precedence for that implementation detail.

| Term | Definition |
|---|---|
| **Acceptance** | Explicit determination that defined criteria for a capability, gate, release or environment have been satisfied by attributable evidence. |
| **Canonical console** | The unified DTMO web application used for the normal operator journey across Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance. |
| **Canonical state** | Durable application state treated as authoritative by the application. For normalized intelligence records, PostgreSQL is the canonical application persistence layer; supporting search and object stores do not replace it. |
| **Connector** | Governed integration component that obtains intelligence from an approved source and submits it into the DTMO ingestion pipeline. |
| **CTI** | Cyber Threat Intelligence: information about threats, actors, vulnerabilities, campaigns, indicators, techniques and related context used to support security decisions. |
| **Deployment identity** | Immutable identifier or set of identifiers that unambiguously binds evidence to one deployed version in one environment. |
| **Engineering evidence** | Evidence produced through source inspection, automated tests, CI, local/reference runtime validation or controlled engineering fixtures. |
| **Environment evidence** | Evidence obtained from an identified deployed environment and attributable to its deployment identity. |
| **Exact-head CI** | Verification discipline requiring all applicable checks to apply to the exact commit SHA being accepted. A subsequent commit invalidates earlier exact-head evidence. |
| **External assurance** | Security, performance or other assurance performed with the required independence from the implementation team. |
| **External-share approval** | Separate human authorization permitting intelligence or derived material to be shared outside its governed boundary. It is not granted by ingestion, analytics, Administration, CI or deployment access. |
| **Fail closed** | Governance principle under which missing, ambiguous, invalid or incomplete evidence results in non-acceptance rather than assumed success. |
| **First-class mapping** | Explicit structured mapping between a DTMO object/evidence item and an external framework control, technique or scoring construct. Free-text similarity does not qualify. |
| **Governance** | Policies, authority boundaries, mappings, evidence rules and decision mechanisms controlling how DTMO is developed, operated and used. |
| **Human review** | Explicit review performed by an authorized human. Automated analysis may support but does not silently replace required human authority. |
| **Immutable evidence** | Evidence retained in a form that preserves its point-in-time identity and attribution to the relevant commit, release or deployment. |
| **Intelligence record** | Normalized CTI object persisted by DTMO with source/provenance and relevant analytical metadata. |
| **Least privilege** | Principle that identities receive only the permissions required for their defined responsibilities. |
| **Normenkader IBP** | Dutch information-security and privacy framework used in education. DTMO documentation does not claim a first-class control mapping unless explicit mapping evidence exists. |
| **Production-equivalent staging** | Approved non-production environment sufficiently representative of the intended production architecture, controls and deployment configuration to support Phase 8 acceptance. |
| **Production readiness** | Evidence-based state indicating whether DTMO has satisfied all required engineering, staging, independent assurance and formal go/no-go gates. It is distinct from software feature completeness. |
| **Provenance** | Traceable information describing the origin and processing history of intelligence or evidence. |
| **RBAC** | Role-Based Access Control: authorization model in which permissions are assigned through governed roles and principals. |
| **RC13** | Functional acceptance cycle that established the repaired canonical product journey and accountable owner acceptance. |
| **Release gate** | Defined acceptance boundary that must be satisfied before progressing to the next release/readiness state. |
| **Repository-controlled evidence** | Evidence whose generation and validation can be performed and reviewed from the repository and its CI processes. |
| **Service account** | Non-human identity used by an application or automation. Service-account permissions remain distinct from human authority. |
| **Source** | External or internal origin from which CTI may be collected under defined legal, technical and governance conditions. |
| **Source Catalog** | Governed DTMO inventory describing supported or known intelligence sources and their connection characteristics. |
| **Staging emulator** | Synthetic or controlled engineering environment used to test staging-related contracts. It is not evidence that a real production-equivalent staging deployment exists. |
| **Traceability** | Ability to connect requirements, decisions, implementation, controls, tests, evidence and acceptance outcomes. |
| **Trust boundary** | Architectural boundary across which identity, authorization, data sensitivity or control assumptions change. |
| **UNMAPPED** | Explicit state indicating that no accepted first-class mapping currently exists. |
| **CONTEXT_ONLY** | State indicating that a framework or scoring concept is presented as context but is not represented as an authoritative first-class mapping. |
