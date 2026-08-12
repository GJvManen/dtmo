# DTMO Lessons Learned

Last updated: **2026-08-12**

## CI and release integrity

- Exact-head evidence prevents accidental reuse of stale successful CI after documentation or lifecycle-state changes.
- Workflow presence is not evidence of successful execution.
- Lifecycle regression tests must advance with evidence-backed state transitions without weakening non-overclaim assertions.
- Documentation changes can invalidate a previously green exact head and therefore require fresh CI when they are part of a gated PR.

## Security and governance

- RBAC is insufficient without separation of duties and explicit human approval boundaries.
- Review and human external-share approval must remain distinct actions.
- Technical success must never imply publication authority.
- Secret values, credentials and tokens should never be embedded in retained repository evidence.
- Framework/control/technique mappings require explicit provenance and review; semantic similarity is not evidence of equivalence.

## Evidence and provenance

- Machine-readable evidence improves independent verification, but human-readable claim boundaries remain essential.
- Provenance and confidence are first-class properties of threat intelligence and must survive ingestion, transformation and reporting.
- Public threat/CVE/vendor-advisory reviews are meaningful only when tied to an applicable immutable target and a recorded review time.
- Search/index success and raw-evidence persistence are useful supporting evidence but do not replace the canonical application persistence boundary.

## Functional acceptance

- Component/API/CI success does not necessarily prove a usable end-to-end product.
- Accountable owner testing can reveal interaction and lifecycle defects that synthetic component tests miss.
- Once a functional product gate is accepted, later owner observations should be classified carefully: regressions may reopen the gate; desired enhancements should enter the product backlog without rewriting accepted history.

## Recovery and operations

- Repository-controlled recovery tests establish engineering confidence but do not replace a full production-equivalent restoration exercise.
- Alerting gates should prove detection, correlation and actionable guidance without leaking raw sensitive payloads.
- Operational runbooks require exercised behavior and ownership, not just written procedures.

## Staging and production readiness

- An emulator can prove configuration/topology contracts without proving a real environment.
- A bounded application-container runtime smoke can prove application startup/behavior without proving dependency or infrastructure parity.
- Real staging acceptance requires one immutable deployment identity that binds environment, release, configuration, secret-management, network/TLS, data handling, change control, rollback and security-review evidence.
- Local development credential compatibility exceptions must never silently become staging/production identity architecture.

## Documentation architecture

- Continuous release reconciliation can accidentally turn professional product/architecture documents into operational run logs.
- Architecture, security, governance, executive and readiness documents must retain their durable building blocks even while status changes frequently.
- Exact PR/workflow/SHA/incident chronology belongs in the operational evidence layer (`docs/development/`, GitHub and CI artifacts), not in the project homepage or architecture narrative.
- A formal documentation standard and automated documentation contract are necessary to prevent gradual erosion of professional documentation quality.
- Current lifecycle status must be reconciled consistently across the professional document set without rewriting immutable historical evidence.

## Accessibility and UX

- Browser automation is valuable regression protection, but UX acceptance also depends on truthful state, clear task architecture and accountable real-user/operator behavior.
- Semantic status must not rely on colour alone; labels, hierarchy and accessible cues remain required.

## Program governance

- External-only blockers should remain explicit without unnecessarily preventing the next internally executable roadmap task.
- A run should leave one clear next priority to avoid parallel unbounded development.
- Missing evidence should be recorded as a blocker, not converted into an assumed or conditional pass.
- Product enhancement work and production-readiness evidence are parallel tracks and should not be conflated.
