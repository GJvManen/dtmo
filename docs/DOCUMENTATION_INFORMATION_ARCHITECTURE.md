# DTMO Documentation Information Architecture

## Purpose

DTMO documentation is split into stable product/operator documentation and transient lifecycle/evidence records. The portal must help readers find current supported behavior without treating historical delivery chronology as product truth.

This classification is organizational only. It does not delete or rewrite historical evidence, and it does not upgrade repository evidence into staging, production-equivalent, penetration-test, independent-assurance or production evidence.

## Stable product and operator domains

The following domains describe current supported behavior, interfaces, controls or operating procedures and are suitable for primary product-facing navigation:

- `installation/` — supported installation and bootstrap procedures;
- `product/` and `user/` — product concepts and canonical operator workflows;
- `administration/` and `operations/` — administrative and operational procedures;
- `architecture/` and `integrations/` — architecture, trust boundaries and integration contracts;
- `security/` — security model, controls and threat/risk documentation;
- `governance/` and `legal/` — governance mappings, retention and legal constraints;
- `api/` and `development/` — supported engineering/API guidance.

Stable documents must describe the current supported state. When behavior changes, the stable document and its contract tests are updated in the same bounded change. Stable documentation must preserve RBAC, provenance, fail-closed behavior, explicit human review/share/publication authority and server-side credential boundaries.

## Lifecycle, quality and evidence domains

The following domains record project state, delivery sequencing, quality contracts or candidate/run evidence and must not be presented as timeless product behavior:

- `project/` — authoritative current lifecycle state and readiness decisions;
- `roadmap/` — planned and historical delivery sequencing;
- `qa/` — repository-controlled quality and acceptance contracts;
- `evidence/` — evidence indexes, templates and candidate/run records;
- `assurance/` — assurance planning, boundaries and externally supplied assurance records where explicitly present;
- `production/` — production-readiness/candidate material whose claims remain identity- and environment-bound;
- `performance/` — benchmark/performance evidence whose validity is bound to its tested context.

A file in these domains may be important and authoritative for its bounded lifecycle purpose, but it is not automatically proof of current operator usability or production behavior.

## Portal rules

1. `docs/README.md` remains the primary navigation portal and starts with stable task-oriented entry points.
2. Lifecycle and evidence material is linked from clearly labelled QA/release/current-state sections rather than mixed into normal operator workflow descriptions.
3. Historical evidence is preserved; it is not rewritten to support a newer candidate.
4. Repository CI is repository evidence only. Missing external owner acceptance, production-equivalent validation, penetration-test evidence or independent assurance remains missing.
5. Product-facing pages may link to bounded evidence, but must not convert successful connector, enrichment, graph, automation or test execution into source truth, compromise, remediation, compliance or production authorization.

## Maintenance gate

A documentation change is incomplete when it introduces a new primary stable domain without adding it to the portal, or when it places run-specific/lifecycle chronology in the stable product navigation as if it were current product behavior.

The contract test `backend/tests/test_documentation_information_architecture_contract.py` protects the high-level separation and portal discoverability. It intentionally does not delete or move historical files: migration of any specific document must be a separate reviewable change with link preservation and evidence-boundary review.