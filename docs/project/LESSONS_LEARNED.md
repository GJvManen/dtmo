# DTMO Lessons Learned

Last updated: 2026-08-10

## CI and release integrity

- Exact-head evidence prevents accidental reuse of stale successful CI after documentation or lifecycle-state changes.
- Workflow presence is not evidence of successful execution.
- Lifecycle regression tests must advance with evidence-backed state transitions without weakening non-overclaim assertions.
- Documentation changes can invalidate a previously green exact head and therefore require fresh CI when they are part of a gated PR.

## Security and governance

- RBAC is insufficient without separation of duties and explicit human approval boundaries.
- Review and human share approval must remain distinct actions.
- Technical success must never imply publication authority.
- Secret values, credentials and tokens should never be embedded in retained repository evidence.

## Evidence and provenance

- Machine-readable evidence improves independent verification, but human-readable claim boundaries remain essential.
- Provenance and confidence are first-class properties of threat intelligence and must survive ingestion, transformation and reporting.
- Public threat/CVE/vendor-advisory reviews are meaningful only when tied to an applicable immutable target and a recorded review time.

## Recovery and operations

- Repository-controlled recovery tests establish engineering confidence but do not replace a full production-equivalent restoration exercise.
- Alerting gates should prove detection, correlation and actionable guidance without leaking raw sensitive payloads.
- Operational runbooks require exercised behavior and ownership, not just written procedures.

## Staging and production readiness

- An emulator can prove configuration/topology contracts without proving a real environment.
- A bounded application-container runtime smoke can prove application startup/behavior without proving dependency or infrastructure parity.
- Real staging acceptance requires one immutable deployment identity that binds environment, release, configuration, secret-management, network/TLS, data handling, change control, rollback and security review evidence.

## Accessibility

- Browser and DOM automation are valuable regression controls but cannot substitute for genuine screen-reader behavior on supported real combinations.

## Program governance

- External-only blockers should remain explicit without unnecessarily preventing the next internally executable roadmap task.
- A run must leave one clear next priority to avoid parallel unbounded development.
- Missing evidence should be recorded as a blocker, not converted into an assumed or conditional pass.
