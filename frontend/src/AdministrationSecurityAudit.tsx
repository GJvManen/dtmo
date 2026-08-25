import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

type Session = { subject: string; roles: string[]; permissions: string[]; service_account?: boolean };
type AuditEvent = {
  sequence_number: number;
  event_id: string;
  occurred_at: string;
  principal: string;
  principal_type: string;
  action: string;
  resource: string;
  decision: string;
  request_id: string;
  provenance_reference: string | null;
  event_hash: string;
};
type AuditResponse = { count: number; read_only: boolean; events: AuditEvent[] };
type RevocationResponse = { jti: string; expires_at: string; audit_event_id: string };

async function readJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof payload === 'object' && payload && 'detail' in payload ? String((payload as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return payload as T;
}

async function postJson<T>(url: string, body: object): Promise<T> {
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json', 'X-Request-ID': crypto.randomUUID() },
    body: JSON.stringify(body),
  });
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof payload === 'object' && payload && 'detail' in payload ? String((payload as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return payload as T;
}

export function AdministrationSecurityAudit() {
  const queryClient = useQueryClient();
  const [jti, setJti] = useState('');
  const [expiresAt, setExpiresAt] = useState('');
  const [reason, setReason] = useState('');
  const [lastRevocation, setLastRevocation] = useState<RevocationResponse | null>(null);

  const session = useQuery({ queryKey: ['administration', 'security', 'session'], queryFn: () => readJson<Session>('/api/v1/ui/session'), retry: false });
  const auditAllowed = session.data?.permissions.includes('read:audit') ?? false;
  const revokeAllowed = (session.data?.permissions.includes('revoke:tokens') ?? false) && !session.data?.service_account;
  const audit = useQuery({
    queryKey: ['administration', 'audit', 'recent'],
    queryFn: () => readJson<AuditResponse>('/api/v1/audit/events?limit=50'),
    enabled: auditAllowed,
    retry: false,
  });
  const revoke = useMutation({
    mutationFn: () => postJson<RevocationResponse>('/api/v1/security/tokens/revoke', { jti: jti.trim(), expires_at: expiresAt.trim(), reason: reason.trim() }),
    onSuccess: (result) => {
      setLastRevocation(result);
      setJti('');
      setExpiresAt('');
      setReason('');
      void queryClient.invalidateQueries({ queryKey: ['administration', 'audit', 'recent'] });
    },
  });

  return (
    <section className="workspace-foundation" aria-labelledby="administration-security-title" data-admin-section="security-audit">
      <header className="workspace-heading">
        <div>
          <p className="eyebrow">Administration control plane</p>
          <h2 id="administration-security-title">Security & audit</h2>
          <p>Privileged token revocation and read-only append-only audit evidence are available from the canonical Administration route.</p>
        </div>
        <div className="heading-statuses"><span className="phase-badge">11.10q functional recovery</span><span className="evidence-label">Server-authorized only</span></div>
      </header>

      <article className="surface command-panel" data-admin-security="token-revocation">
        <header className="panel-heading"><div><p className="eyebrow">Security administration</p><h2>Bearer token revocation</h2></div><span className="evidence-label">revoke:tokens</span></header>
        <p className="boundary-copy">Revocation is a privileged server-side operation. The browser submits only the token JTI, declared expiry and an explicit reason; DTMO performs authorization, revocation-state mutation and persistent audit recording. Service accounts are not offered this human administrative control.</p>
        {!session.isPending && !revokeAllowed && <p className="panel-state error-state">Token revocation unavailable for this principal. No browser-side bypass is provided.</p>}
        {revokeAllowed && <div className="command-grid">
          <label><span>Token identifier (JTI)</span><input value={jti} autoComplete="off" onChange={(event) => setJti(event.target.value)} placeholder="Token JTI" /></label>
          <label><span>Token expiry (ISO 8601)</span><input value={expiresAt} autoComplete="off" onChange={(event) => setExpiresAt(event.target.value)} placeholder="2026-08-24T16:00:00Z" /></label>
          <label><span>Revocation reason</span><textarea value={reason} minLength={3} maxLength={500} onChange={(event) => setReason(event.target.value)} placeholder="Why must this bearer token be revoked?" /></label>
          <button type="button" disabled={!jti.trim() || !expiresAt.trim() || reason.trim().length < 3 || revoke.isPending} onClick={() => revoke.mutate()}>Revoke bearer token</button>
        </div>}
        {revoke.isError && <p className="panel-state error-state">Revocation failed: {revoke.error.message}</p>}
        {lastRevocation && !revoke.isError && <p className="panel-state">Token revoked through the governed API. Audit event: <code>{lastRevocation.audit_event_id}</code>.</p>}
      </article>

      <article className="surface command-panel" data-admin-security="audit-evidence">
        <header className="panel-heading"><div><p className="eyebrow">Audit navigation</p><h2>Recent append-only audit evidence</h2></div><div className="heading-statuses"><span className="evidence-label">read:audit</span>{auditAllowed && <button type="button" onClick={() => audit.refetch()} disabled={audit.isFetching}>Refresh evidence</button>}</div></header>
        <p className="boundary-copy">This is a read-only projection of persisted audit events. Event hashes, request IDs and provenance references are evidence attributes; viewing them grants no mutation, review, sharing or publication authority.</p>
        {!session.isPending && !auditAllowed && <p className="panel-state error-state">Audit evidence unavailable for this principal.</p>}
        {auditAllowed && audit.isPending && <p className="panel-state">Loading recent audit evidence…</p>}
        {auditAllowed && audit.isError && <p className="panel-state error-state">Audit evidence unavailable: {audit.error.message}</p>}
        {auditAllowed && audit.data && <div className="table-wrap"><table><thead><tr><th>Time</th><th>Action</th><th>Principal</th><th>Decision</th><th>Resource</th><th>Request</th><th>Event hash</th></tr></thead><tbody>{audit.data.events.map((event) => <tr key={event.event_id} data-audit-event={event.event_id}><td>{event.occurred_at}</td><td>{event.action}</td><td>{event.principal}</td><td>{event.decision}</td><td>{event.resource}</td><td><code>{event.request_id}</code></td><td><code>{event.event_hash}</code></td></tr>)}{audit.data.count === 0 && <tr><td colSpan={7}>No persisted audit evidence is currently available. This is not proof that no auditable activity has occurred outside the accessible store.</td></tr>}</tbody></table></div>}
      </article>

      <article className="surface evidence-surface"><div><p className="eyebrow">Security boundary</p><h2>No legacy security administration dependency</h2></div><p>The canonical Administration route now exposes governed token revocation and read-only audit evidence through same-origin APIs. Authentication policy, token-state storage, permissions and audit persistence remain server-side; this UI does not expose secrets or create independent security authority.</p></article>
    </section>
  );
}
