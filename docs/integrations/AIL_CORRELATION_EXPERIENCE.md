# AIL investigation and correlation experience

## Scope

E8.9 correlates data-minimized AIL-derived indicators with canonical DTMO intelligence. E8.9a introduces the deterministic server-side correlation contract; E8.9b will expose that contract in the governed investigation workspace.

The contract accepts an AIL-derived indicator type/value and candidate DTMO records. It emits bounded correlation evidence only. It does not expose AIL paste bodies, raw leak content, investigation notes or other unrestricted source material.

## Correlation semantics

The first accepted relations are deliberately deterministic:

- `canonical_exact_match` — exact case-insensitive equality against a canonical DTMO title, summary or tag;
- `misp_attribute` — exact match against a provenance-preserved MISP event attribute;
- `misp_object_attribute` — exact match against an attribute of a provenance-preserved MISP object;
- `vulnerability_identifier` — exact CVE/alias match with bounded vendor/product context where already present in canonical metadata.

No fuzzy, embedding or semantic similarity is used. A correlation is evidence that two stored values match; it is not evidence of compromise, exposure, affected-version presence, exploitability or attribution.

## Privacy and governance boundaries

AIL remains the specialist collection/analysis system. DTMO consumes governed extracted indicators and references. Raw AIL item/paste content is not a correlation input or response field in this slice. AIL items are excluded from self-correlation.

MISP restrictions remain authoritative. Correlation does not change TLP/distribution restrictions and does not grant publication or external-share authority. Vulnerability/product context is descriptive only and does not create an organizational risk score.

## Evidence boundary

Repository tests use synthetic candidate records and MISP projections. They demonstrate deterministic normalization/correlation behavior only. They do not prove live AIL or MISP connectivity, source completeness, owner acceptance, production deployment, pentest acceptance or legal authority to collect or redistribute source material.

## Delivery sequence

- **E8.9a:** deterministic correlation contract and exact-head repository gate.
- **E8.9b:** authenticated investigation API/workspace projection, truthful empty/degraded states and browser E2E while preserving the same privacy and authority boundaries.
