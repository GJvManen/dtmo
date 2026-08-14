# Phase 8.1 Staging Identity Collection Runbook

## Purpose

This runbook turns the Phase 8.1 deployment-identity requirement into a repeatable evidence collection step. It does **not** create or approve a staging environment and does not mark Phase 8 as passed.

## Preconditions

Before using the tooling, the project must have a real approved production-equivalent staging environment. The environment must have an accountable owner, an approved reachable HTTPS endpoint and a deployed DTMO release that can be tied to immutable image digests.

Repository CI, local Docker Compose and `infrastructure/staging-emulator/` are not acceptable substitutes.

## 1. Create a working manifest outside source control

Copy the template to an evidence workspace that is appropriate for the environment:

```bash
cp docs/staging/PHASE8_DEPLOYMENT_IDENTITY.example.json /secure/evidence/phase8-staging-identity.json
```

Do not commit the populated manifest if it contains restricted infrastructure identifiers. Never put passwords, tokens, private keys or secret values into the manifest.

## 2. Populate identity-bound evidence

Replace every placeholder with facts collected from the same deployed environment. Required evidence includes:

- environment identifier and accountable owner;
- approved HTTPS endpoint;
- exact deployed release and 40-character Git commit SHA;
- application and supporting image digests in `sha256:<64 hex>` form;
- runtime/infrastructure inventory;
- configuration-parity evidence;
- logical secret-manager and least-privilege identity references;
- TLS and network-control evidence;
- data classification/sanitization statement;
- explicit confirmation that production credentials are not reused;
- change and rollback records;
- deployment-time security review;
- explicit authorization to begin external validation.

`project_owner_staging_acceptance` remains `NOT_RECORDED` during identity intake and `phase8_pass` remains `false`.

## 3. Validate the manifest

Run:

```bash
python3 tools/phase8_staging_identity.py /secure/evidence/phase8-staging-identity.json
```

A valid intake prints:

```text
PHASE 8.1 IDENTITY INTAKE: PASS
Identity fields are syntactically coherent; external evidence still requires review.
manifest_fingerprint: sha256:...
phase8_pass: false
```

For machine-readable output:

```bash
python3 tools/phase8_staging_identity.py /secure/evidence/phase8-staging-identity.json --json
```

## 4. Record the manifest fingerprint

The validator canonicalizes the JSON and emits a SHA-256 fingerprint. Record that fingerprint with the controlled Phase 8 evidence package. If any field changes, rerun the validator and treat the result as a new evidence identity.

The fingerprint is an integrity reference for the manifest; it does not independently prove that the supplied environment facts are true.

## 5. Independent evidence review

Review the manifest and linked evidence against `PHASE8_DEPLOYMENT_IDENTITY_RECORD.md` and `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`.

Only after the identity is coherent should functional, operational, recovery and security acceptance suites be executed against the same deployment identity.

## Fail-closed rules

The intake fails when required fields remain placeholders, image or Git identities are not immutable, the endpoint is not HTTPS, production-credential separation is not confirmed, external validation is not authorized, or the manifest tries to predeclare Phase 8 success/owner acceptance.

Passing this validator means **identity intake is structurally ready for review**. It never means `Phase 8 = PASS`.
