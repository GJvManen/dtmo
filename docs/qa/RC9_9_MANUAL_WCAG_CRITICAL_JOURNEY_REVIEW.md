# RC9.9 — Manual / Non-Automatable WCAG 2.2 AA Critical-Journey Review

Status: `BLOCKED`

## Objective

Perform one bounded manual/source-level review of the four accepted Phase-6 critical browser journeys against WCAG 2.2 AA criteria that are not fully evidenced by RC9.5–RC9.8. Do not convert absence of assistive-technology or rendered visual evidence into PASS.

Covered surfaces:

- governed share approval (`/ui/share-approval`);
- analyst intelligence search (`/ui/analyst-search`);
- CISO token revocation (`/ui/ciso-security`);
- auditor read-only evidence (`/ui/auditor`).

## Evidence and provenance

Primary standard source: W3C WCAG 2.2 Recommendation and WAI Understanding documents:

- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/WAI/WCAG22/Understanding/
- https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html

Repository evidence inspected:

- `backend/dtmo/ui.py`;
- `backend/dtmo/ciso_ui.py`;
- `backend/dtmo/auditor_ui.py`;
- accepted RC9.5 keyboard evidence;
- accepted RC9.6 responsive/target-size evidence;
- accepted RC9.7 Chromium/Firefox/WebKit compatibility evidence;
- accepted RC9.8 automated accessibility evidence.

Confidence is `HIGH` for source-level findings and previously retained CI evidence. Confidence is `NONE/NOT EVIDENCED` for genuine VoiceOver/NVDA behavior because no real assistive-technology session was executed in this run.

## Criterion-level review

| WCAG 2.2 criterion | Decision | Evidence / rationale |
| --- | --- | --- |
| 1.3.1 Info and Relationships | PASS (bounded surfaces) | Native `main`, headings, `fieldset`/`legend`, labels, forms, lists and status regions are present; RC9.8 also verified landmark/heading/accessibility-name basics. |
| 1.3.2 Meaningful Sequence | PASS (source-level) | DOM order is linear and no CSS visual reordering is used on the four surfaces. |
| 1.4.1 Use of Color | PASS (source-level) | Loading, error, empty, forbidden and success states are communicated by text, not color alone. |
| 1.4.3 Contrast (Minimum) | NOT EVIDENCED | No retained measured computed-color contrast evidence was produced for every rendered state. Default system text is not accepted as a formal measured PASS. |
| 1.4.4 Resize Text | NOT EVIDENCED | No retained 200% text-resize/manual inspection evidence. |
| 1.4.10 Reflow | PARTIAL | RC9.6 proved 360 px, 768 px and 1440 px viewports without blocking horizontal overflow; WCAG reflow evidence at the required 320 CSS px equivalent remains unproven. |
| 1.4.11 Non-text Contrast | NOT EVIDENCED | No retained measurement of focus indicators, form boundaries and other required graphical/UI boundaries. |
| 1.4.12 Text Spacing | NOT EVIDENCED | No retained manual text-spacing override evidence. |
| 2.1.1 Keyboard | PASS (bounded surfaces) | Accepted RC9.5 used keyboard-only operation across all four critical surfaces. |
| 2.1.2 No Keyboard Trap | PASS (bounded journeys) | Accepted keyboard journeys completed and exited controls without a recorded trap. |
| 2.4.2 Page Titled | PASS | RC9.8 verified non-empty titles and source inspection confirms specific titles per surface. |
| 2.4.3 Focus Order | PARTIAL | Source order is logical and RC9.5 reaches required controls, but a complete retained tab-order transcript for every focusable element is absent. |
| 2.4.6 Headings and Labels | PASS (bounded surfaces) | Specific H1s and visible input/control labels are present. |
| 2.4.7 Focus Visible | PASS (bounded tested controls) | RC9.5/RC9.8 verified visible browser focus on critical controls. |
| 2.4.11 Focus Not Obscured (Minimum) | PASS (source-level) | No author-created sticky/overlay content is present on the reviewed surfaces. |
| 2.5.3 Label in Name | PASS (source-level) | Visible button text is the accessible name; visible field labels identify the associated inputs. |
| 2.5.8 Target Size (Minimum) | PASS (bounded controls) | RC9.6 retained evidence required interactive controls to be at least 24 px in both dimensions. |
| 3.1.1 Language of Page | PASS | `lang="en"` is present on all four pages and RC9.8 verified a declared language. |
| 3.2.1 On Focus | PASS (source-level) | No focus handler changes context or submits operations. |
| 3.2.2 On Input | PASS (source-level) | Data entry alone does not trigger context changes or privileged actions. |
| 3.3.1 Error Identification | PARTIAL | Visible/native/custom error messages exist, but AT announcement and field-error association have not been verified with a real screen reader. |
| 3.3.2 Labels or Instructions | PASS (bounded forms) | Item ID, search, JTI, expiry and reason fields have visible labels/instructions. |
| 4.1.2 Name, Role, Value | PARTIAL | Native controls and accessible names are present; genuine AT interpretation remains unexecuted. |
| 4.1.3 Status Messages | **BLOCKED — A11Y-001** | Each page starts with `Resolving authenticated principal…`; JavaScript later replaces that text with subject/roles and reveals RBAC-governed controls. The principal element is not a `role="status"`/live region. A screen-reader user may therefore not be notified that session resolution completed or that privileged controls became available without moving focus. |

## Blocking finding A11Y-001 — asynchronous session state is not announced

Affected source:

- `backend/dtmo/ui.py`: `#principal` and `#analyst-principal`;
- `backend/dtmo/ciso_ui.py`: `#ciso-principal`;
- `backend/dtmo/auditor_ui.py`: `#auditor-principal`.

Observed pattern:

1. page renders `Resolving authenticated principal…`;
2. `/api/v1/ui/session` resolves asynchronously;
3. JavaScript replaces principal text and reveals/hides RBAC-governed controls;
4. the changed principal/session state has no live/status semantics.

Impact: users relying on assistive technology may not receive programmatic notification of the resolved identity/roles and resulting availability of privileged controls. This is material on governed security workflows because understanding current role/capability state is operationally significant.

Required remediation: expose session-resolution state through an appropriate polite status mechanism without changing backend-derived RBAC, separation of duties or human share approval. Add regression evidence that the status semantics exist on all four surfaces. Genuine VoiceOver/NVDA confirmation remains separate evidence after remediation.

## Other evidence gaps

The following are not recorded as defects in this run, but they remain unevidenced and therefore block a product-wide WCAG 2.2 AA claim: measured contrast, 200% text resize, 320 CSS px reflow, text spacing overrides, full tab-order transcript, and genuine assistive-technology behavior.

## Security/governance invariants

This review changes no authentication, RBAC, data, connector, publication or audit behavior. Backend-derived permissions, separation of duties, privacy, provenance, auditability and separate human share approval remain mandatory.

## Threat / CVE / vendor context

No production dependency, provider or connector is introduced by this documentation review. Threat intelligence, education-sector incident history, CVE data and vendor advisories do not alter the accessibility finding. Existing security/dependency gates remain authoritative.

## Decision

`BLOCKED`. Phase 6 cannot be completed while `A11Y-001` is unresolved and while the explicitly listed WCAG evidence gaps remain unverified.

Exactly one next priority: remediate `A11Y-001` by making asynchronous principal/session resolution programmatically announced on all four critical surfaces, add bounded regression evidence, and preserve backend-derived RBAC and separate human share approval.