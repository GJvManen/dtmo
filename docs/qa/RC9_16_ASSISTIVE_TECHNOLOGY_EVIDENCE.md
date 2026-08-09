# RC9.16 — Genuine Assistive-Technology Behavior Evidence

Status: `BLOCKED_EXTERNAL`

## Objective

Establish genuine screen-reader behavior evidence for the four accepted critical surfaces after the automated WCAG/keyboard gates.

## Required execution matrix

1. VoiceOver on supported macOS + Safari.
2. NVDA on supported Windows + Firefox or Chrome.
3. Surfaces: `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, `/ui/auditor`.

## Required observations per surface

- page title, landmarks and heading structure are announced coherently;
- reading/virtual-cursor order is meaningful;
- each interactive control has an appropriate announced name, role and state;
- keyboard focus changes are announced and remain consistent with the accepted focus-order evidence;
- asynchronous authenticated-principal/session status is announced without requiring focus movement;
- validation, result and operational status feedback is perceivable where the journey produces it;
- role-gated controls are exposed only for the authorized backend-derived session role;
- the share-approval surface preserves and announces a separate explicit human approval action before external sharing.

## Evidence record

For every host/browser/screen-reader combination retain:

- tester identity or accountable test owner;
- UTC timestamp;
- OS version;
- browser and version;
- screen reader and version;
- surface and tested journey;
- observation/result per checkpoint;
- defect ID, severity and reproduction steps for any failure;
- transcript, recording, screenshot, or other durable evidence reference where permitted by privacy policy.

Use synthetic/non-production identities and data. Do not include credentials, tokens, personal data, or sensitive production content in retained evidence.

## Acceptance gate

PASS requires completed retained evidence for both VoiceOver and NVDA matrices with no blocking accessibility defect. Missing, simulated, DOM-only, browser-only, or unexecuted screen-reader evidence is not PASS.

## Current blocker

The current automation environment does not provide a real macOS VoiceOver host or Windows NVDA host. Browser/DOM automation cannot truthfully substitute for actual assistive-technology announcements or interaction behavior. RC9.16 therefore remains `BLOCKED_EXTERNAL` until the manual/external matrix is executed and retained.

## Governance invariants

Backend-derived RBAC, separation of duties, privacy boundaries, auditability, and separate human share approval remain authoritative and must be observed during AT testing. No production credentials or production data are required.
