# E8 MISP Governed Export Gate

## Objective

The E8 MISP Governed Export Gate proves the repository-controlled safety contract for E8.7 on the exact pull-request head.

## Required repository evidence

The dedicated workflow must:

- check out the exact PR head rather than a synthetic merge ref;
- run focused E8.7 export and pre-existing governed-decision tests;
- run Ruff, mypy and compile checks for the bounded implementation;
- fail closed if the primary evidence job is missing or unsuccessful.

The contract tests cover:

- no export before separate review and human share approval;
- no service-account export authority;
- outbound MISP feature flag separated from read integration;
- distribution/sharing-group validation;
- TLP and authoritative MISP-source restriction preservation;
- fail-closed treatment of MISP-origin records whose source restrictions are not canonically projected;
- unpublished MISP event creation only;
- runtime-only API-key use;
- deterministic event identity and replay evidence;
- successful-delivery audit evidence;
- uncertain-delivery state that blocks automatic replay.

## Acceptance rule

Repository status is `PASS` only when the dedicated gate and the complete applicable exact-head CI/regression matrix are `completed/success` on one final PR head.

Any commit after that evidence invalidates the prior exact-head acceptance.

## External-evidence boundary

A green gate is not evidence that a real MISP instance accepted an event. It is not evidence of production credentials, destination authorization, sharing-community permission, deployment, owner acceptance, pentest acceptance, or external publication. Live delivery and any later MISP publication/synchronization remain separate deployment/external evidence.