# Phase 8 Ephemeral Self-Test Environment — 2026-08-15

## Purpose

This run intentionally creates a repository-controlled, ephemeral production-mode DTMO runtime for self-testing the Phase 8 staging-identity and runtime contracts after PR #261. It is **not** the owner-approved external staging environment and must never be used as external staging acceptance evidence.

## Environment model

The GitHub Actions `Phase 8 Staging Emulator Runtime Gate` builds exact-head DTMO on a fresh Ubuntu 24.04 runner and starts the application container with:

- `DTMO_ENVIRONMENT=production`;
- read-only container filesystem plus tmpfs `/tmp`;
- `no-new-privileges` and all Linux capabilities dropped;
- synthetic non-production credentials/identity markers;
- live connectors and AI analyst disabled;
- bounded localhost exposure only.

The run records the exact PR head, local immutable Docker image ID, runtime smoke checks and explicit claim-boundary booleans. Synthetic secret markers must not appear in captured runtime logs.

## Acceptance for this self-test

The self-test is successful only when:

1. Phase 8 staging emulator runtime contract tests pass;
2. exact-head runtime image build/start succeeds;
3. bounded runtime smoke passes;
4. local image identity is recorded as `sha256:*`;
5. all runtime checks are true;
6. all external-evidence claim-boundary flags remain false;
7. synthetic secret-leak scan passes;
8. Phase 8.1 immutable identity intake tests from PR #261 pass in the normal exact-head matrix.

## Evidence boundary

A successful result proves that DTMO can construct and exercise the repository-controlled production-mode emulator and that the Phase 8 identity-intake contract remains executable. It does **not** prove external TLS, PostgreSQL, Redis, OpenSearch, object storage, production-equivalent network controls, live-source connectivity, owner staging acceptance or Phase 8 PASS.
