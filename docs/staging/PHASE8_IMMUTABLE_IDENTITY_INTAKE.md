# Phase 8 Immutable Staging Identity Intake

**Status:** `READY FOR EXTERNAL FACT CAPTURE`  
**Evidence class:** external production-equivalent staging identity binding  
**Current Phase 8 decision:** owner-verified external deployment and approved staging exist; immutable technical identity remains to be bound.

## Purpose

This procedure converts externally observed deployment facts into a reviewable Phase 8 identity manifest without treating repository state, CI, Docker Compose or staging emulators as deployment proof.

The authoritative staging facts must be observed from the approved deployment platform/environment. Do not infer the deployed commit from `main`, a PR head, a local checkout or the repository reference recorded at the earlier owner update.

## Required observed facts

Capture all of the following from the same accepted deployment identity:

1. approved environment identifier;
2. accountable staging owner reference;
3. approved reachable endpoint/access path;
4. deployed release identifier;
5. exact full deployed Git commit SHA;
6. immutable application image digest;
7. immutable supporting container image digests;
8. infrastructure/runtime inventory reference;
9. configuration parity/deviation record reference;
10. secret-manager and identity references — identifiers only, never secret values;
11. least-privilege human/service identity evidence reference;
12. TLS/network-control evidence reference;
13. data-class/sanitization statement reference;
14. no-production-credentials confirmation reference;
15. deployment/change record reference;
16. rollback target/procedure record reference;
17. deployment-time security/dependency review reference.

Any missing, inferred, stale or contradictory field blocks formal immutable-identity binding.

## Collector

Use `tools/phase8_identity_manifest.py` only after the above facts have been observed externally.

Example shape:

```bash
python3 tools/phase8_identity_manifest.py \
  --environment-id '<observed environment id>' \
  --owner '<accountable owner reference>' \
  --endpoint '<approved staging endpoint>' \
  --release '<observed deployed release>' \
  --commit '<40-character deployed git sha>' \
  --application-digest 'sha256:<64 hex>' \
  --supporting-digest 'sha256:<64 hex>' \
  --runtime-inventory-ref '<evidence reference>' \
  --configuration-parity-ref '<evidence reference>' \
  --secrets-identity-ref '<logical identity/secret-manager reference>' \
  --least-privilege-ref '<evidence reference>' \
  --tls-network-ref '<evidence reference>' \
  --data-sanitization-ref '<evidence reference>' \
  --no-prod-credentials-ref '<evidence reference>' \
  --change-record-ref '<change reference>' \
  --rollback-record-ref '<rollback reference>' \
  --security-review-ref '<security review reference>' \
  --output phase8-immutable-identity.json
```

The collector rejects placeholder values such as `NOT_PROVIDED`, `UNKNOWN` and `TBD`, rejects mutable image tags such as `latest`, requires a full Git SHA and requires immutable `sha256:` image digests.

## Review rules

The generated manifest is an intake artifact, not automatic acceptance. Review must confirm that all referenced evidence belongs to one immutable deployment identity and that no secret values or unnecessary personal data are present.

The manifest deliberately records `phase8_pass: false`. Immutable identity binding alone does not close Phase 8. Formal progression still requires accepted Phase 8.2, Phase 8.3 and Phase 8.4 evidence against the same identity followed by the accountable Phase 8.5 owner decision.

## Evidence boundary

A successful collector run proves only that the supplied values satisfy the repository's identity-manifest format and fail-closed completeness rules. It does not independently prove that those values are true. Their truth must come from the external approved staging environment/deployment platform and accountable evidence review.
