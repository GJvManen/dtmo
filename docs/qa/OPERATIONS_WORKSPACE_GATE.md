# RC10 Operations Workspace QA Gate

Release candidate: 16.0.0rc10

Status: `CI_VALIDATION_PENDING`

## Scope

This gate covers only the RC10.1 professional Operations Workspace shell and its repository-controlled contracts.

## Required evidence

- `/ui/operations` is wired into the application router;
- package and API versions agree on `16.0.0rc10`;
- command-center navigation exposes intelligence, source management, governance, audit and role workspaces without bypassing their existing server-side authorization;
- runtime status is read from the existing `/health` endpoint;
- connector summary is read from the existing `/connectors` endpoint;
- the shell performs no privileged connector, review, share-approval, token-revocation or admin write action;
- command palette is keyboard accessible through Ctrl/Cmd+K and a visible dialog;
- skip navigation, labelled navigation/tabs, responsive layout and reduced-motion contracts are present;
- dashboard placeholders are clearly labelled and are not claimed as live telemetry;
- all registered GitHub workflows succeed on one final exact PR head.

## Claim boundary

A green gate proves the repository implementation and regression contracts for the shell only. It does not prove real staging parity, genuine VoiceOver/NVDA execution, independent penetration testing, live enterprise data quality or production go/no-go readiness.
