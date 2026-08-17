# Phase 11.7A Cortex Analyzer Connector Gate

State: **`IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`**

## Acceptance objective

Accept the operator-requested Cortex re-entry only when DTMO provides a bounded analyzer-only connector without responder or autonomous-response authority.

## Required checks

- connector uses service/API separation and does not vendor Cortex source;
- only explicitly allowlisted analyzers can run;
- observable type and TLP are validated before disclosure;
- missing token, unknown analyzer/type/TLP, unstable identity and oversized reports fail closed;
- imported results remain read-only enrichment evidence;
- responder execution, external share authority and local-compromise proof remain false;
- professional documentation identifies the new operator requirement as the re-entry trigger without rewriting historical Phase 11.7 evidence;
- Phase 11.8 remains the next bounded priority after protected acceptance.

## Evidence boundary

Synthetic repository tests prove connector policy and request/response normalization only. They do not establish live Cortex connectivity, analyzer quality, upstream-provider entitlement, production permissions, legal authority to disclose observables, production-equivalent validation or production authorization.
