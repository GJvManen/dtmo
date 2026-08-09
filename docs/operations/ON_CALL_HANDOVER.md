# DTMO On-call Ownership and Escalation Handover

## Purpose

This document defines the minimum operational handover contract for DTMO. It assigns responsibilities to roles, defines escalation paths and specifies the evidence required before human operational ownership can be accepted.

This document does **not** assign named production responders, approve contact details, establish a staffed rota, or claim that human handover has occurred.

## Ownership roles

- **Primary on-call responder** — acknowledges alerts, establishes scope, preserves evidence, starts the relevant runbook and maintains the incident timeline.
- **Secondary on-call responder** — provides backup coverage and assumes primary responsibility when the primary is unavailable or overloaded.
- **Incident Commander** — owns incident coordination, severity, decision logging, cross-team prioritization and closure authority.
- **Security lead** — owns security/privacy escalation, credential-compromise decisions, evidence-preservation requirements and breach-assessment coordination.
- **Service owner** — owns service-specific recovery decisions and residual-risk acceptance recommendations.
- **Communications approver** — authorizes external or broad internal communications. Technical responders cannot self-approve publication.
- **Business/stakeholder owner** — accepts business-impact trade-offs and residual service risk where required.

## Separation of duties

Operational response does not change DTMO RBAC or publication authority. Human share approval remains a separate human action. Connectors, service accounts, observability components and responders do not gain publication approval by being on-call or participating in an incident.

## Coverage contract

Before production acceptance, the operating organization must record and approve:

1. primary and secondary coverage windows;
2. timezone and holiday coverage;
3. maximum acknowledgement target per severity;
4. escalation timeout from primary to secondary;
5. escalation timeout to Incident Commander/security lead;
6. authoritative contact mechanism for each role;
7. fallback mechanism when the primary channel is unavailable;
8. handover overlap expectations between shifts;
9. ownership of alert-routing configuration and periodic validation.

Named people, telephone numbers, email addresses, paging-system identifiers and vendor support contacts belong in the approved operational contact system, not in this repository.

## Severity escalation matrix

| Severity | Initial owner | Required escalation | Closure authority |
|---|---|---|---|
| SEV-1 | Primary on-call | Secondary, Incident Commander, security lead and service owner immediately | Incident Commander with service/security input |
| SEV-2 | Primary on-call | Secondary/service owner; Incident Commander or security lead when impact/risk requires | Primary or Incident Commander per impact |
| SEV-3 | Primary on-call | Service owner when unresolved or recurring | Primary/service owner |

Any suspected credential compromise, material confidentiality impact, integrity loss, unsafe recovery condition, or uncontrolled publication path escalates to the security lead regardless of initial severity.

## Shift handover checklist

Outgoing and incoming responders must review and record:

- open incidents and current severity;
- active alerts and suppressed/acknowledged alerts;
- degraded connectors or stale-source conditions;
- queue/storage/search health concerns;
- recent changes, deployments or mitigations;
- outstanding evidence collection or recovery validation;
- residual risks and time-bounded workarounds;
- pending security/privacy decisions;
- pending communications that require human approval;
- vendor/external dependencies and next escalation time;
- the next explicit owner for every unresolved action.

The incoming responder acknowledges receipt. Silent transfer is not accepted evidence of handover.

## Incident evidence and privacy

Handover records use incident IDs, correlation/trace IDs, timestamps, bounded service state and approved ticket references. Do not copy credentials, raw request/payload content, unnecessary personal data, authentication tokens or secrets into handover notes.

## Acceptance record required for human handover

Human operational handover is accepted only when an authorized approver records all of the following outside CI and links the evidence in the applicable production-assurance record:

- named primary and secondary owners exist for the agreed coverage window;
- authoritative paging/contact paths are tested;
- escalation contacts are tested;
- acknowledgement/escalation targets are approved;
- the shift-handover checklist has been executed by real participants;
- at least one human exercise or supervised operational walkthrough has verified the routing and escalation path;
- unresolved gaps have owners and due dates;
- security/privacy escalation and human share approval boundaries are understood;
- the service owner and operational owner sign off the handover.

CI can validate that this contract exists and preserves governance boundaries. CI cannot prove that people are actually staffed, reachable, trained or approved.

## Claim boundary

Until the acceptance record above exists, DTMO must not claim that on-call coverage, production contact paths, operational ownership or escalation acceptance is complete.
