# Storage Integrity Failure / Recovery Runbook

## Trigger

Use this runbook when `dtmo_storage_integrity_alert_active` is active, checksum/size verification fails, immutable evidence cannot be read, or recovery validation identifies provenance/integrity mismatch.

## Immediate checks

1. Assign Incident Commander; treat confirmed integrity failure as at least SEV-2 and escalate to SEV-1 when compromise or material evidence loss is suspected.
2. Record UTC time, bounded storage identifier, correlation ID, affected verification control and last known-good recovery/backup evidence.
3. Stop treating affected stored evidence as authoritative.
4. Preserve verification receipts, audit logs and relevant metadata before repair/deletion. Do not paste object contents, credentials, object keys or full checksums into broad incident channels.
5. Determine whether the failure is isolated corruption, storage/backend outage, credential/access issue, software defect, malicious modification or failed restoration.

## Containment

- Quarantine affected evidence from downstream processing/publication.
- Pause destructive cleanup, compaction or overwrite operations until provenance is preserved.
- Revoke/rotate storage credentials through approved secret-management processes if compromise is suspected.
- Do not regenerate evidence and label it as original. Maintain clear lineage between original, quarantined and restored artifacts.

## Recovery

1. Select a known-good immutable source/backup under the existing recovery procedure.
2. Restore into a controlled target rather than overwriting the only remaining evidence when possible.
3. Re-run size/checksum/integrity verification and validate provenance receipts.
4. Confirm `dtmo_storage_integrity_alert_active` clears after a trusted verification result.
5. Validate dependent database/search references and representative retrieval paths.
6. If reprocessing is required, use preserved provenance and deduplication controls; human share approval remains mandatory.
7. Maintain an observation period and record any residual RPO/RTO deviation for follow-up.

## Security / privacy branch

Escalate to SEV-1 for unexplained tampering, unauthorized storage access, evidence deletion, suspicious credential activity or exfiltration indicators. Preserve audit/security logs and coordinate forensic handling before destructive recovery.

## Communication

Describe the affected service/evidence class and confidence without exposing sensitive object contents or identifiers. Do not claim recovered evidence is trustworthy until integrity/provenance checks pass. External/broad communication requires the applicable human communications/privacy approval.

## Closure criteria

- restored/retrieved evidence passes integrity and provenance checks;
- dependent references are validated;
- no unresolved compromise indicator is masked by recovery;
- RPO/RTO outcome and deviations are recorded;
- incident evidence and follow-up ownership are retained.
