import { useEffect, useMemo, useState } from 'react';
import type { FormEvent } from 'react';

import './misp-sharing.css';

type Session = {
  subject: string;
  roles: string[];
  permissions: string[];
};

type MispRestrictions = {
  restriction_authoritative: boolean;
  distribution: unknown;
  sharing_group_id: unknown;
  tlp_tags: string[];
};

type MispExportRecord = {
  status: string;
  event_uuid: string;
  misp_event_id: string | null;
  distribution: string | null;
  sharing_group_id: string | null;
  tlp: string | null;
  requested_by: string | null;
};

type SharingState = {
  item_id: string;
  title: string;
  source_id: string;
  canonical_url: string;
  review_status: string;
  reviewed_by: string | null;
  share_approved: boolean;
  share_approved_by: string | null;
  misp_restrictions: MispRestrictions | null;
  misp_exports: MispExportRecord[];
  current_event_uuid: string;
  export_eligible: boolean;
  export_blockers: string[];
  principal_actions: {
    can_review: boolean;
    can_approve_share: boolean;
  };
  misp_export_enabled: boolean;
  misp_export_configured: boolean;
  runtime_health_claim: boolean;
  publication_authority: boolean;
  synchronization_authority: boolean;
  evidence_boundary: string;
};

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...init,
    credentials: 'same-origin',
    headers: {
      Accept: 'application/json',
      ...(init?.headers ?? {}),
    },
  });
  let body: unknown = null;
  try {
    body = await response.json();
  } catch {
    body = null;
  }
  if (!response.ok) {
    const detail = typeof body === 'object' && body !== null && 'detail' in body
      ? String((body as { detail: unknown }).detail)
      : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

function displayRestriction(value: unknown) {
  if (value === null || value === undefined || value === '') return 'not recorded';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

function newRequestId() {
  return crypto.randomUUID();
}

export function MispSharingWorkspace() {
  const initialItem = useMemo(() => new URLSearchParams(window.location.search).get('item') ?? '', []);
  const [itemId, setItemId] = useState(initialItem);
  const [session, setSession] = useState<Session | null>(null);
  const [state, setState] = useState<SharingState | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [action, setAction] = useState<string | null>(null);
  const [actionResult, setActionResult] = useState<string | null>(null);
  const [distribution, setDistribution] = useState('0');
  const [tlp, setTlp] = useState('tlp:amber');
  const [sharingGroup, setSharingGroup] = useState('');

  useEffect(() => {
    void requestJson<Session>('/api/v1/ui/session')
      .then(setSession)
      .catch(() => setSession(null));
  }, []);

  useEffect(() => {
    if (initialItem) void loadState(initialItem);
    // initial deep-link load must run once only
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialItem]);

  async function loadState(id = itemId.trim()) {
    if (!id) return;
    setLoading(true);
    setError(null);
    setActionResult(null);
    try {
      const next = await requestJson<SharingState>(`/api/v1/sharing/items/${encodeURIComponent(id)}`);
      setState(next);
      setItemId(id);
      const url = new URL(window.location.href);
      url.searchParams.set('item', id);
      window.history.replaceState({}, '', url);
    } catch (loadError) {
      setState(null);
      setError(loadError instanceof Error ? loadError.message : 'Sharing state unavailable');
    } finally {
      setLoading(false);
    }
  }

  async function runAction(label: string, url: string) {
    if (!state) return;
    setAction(label);
    setActionResult(null);
    setError(null);
    try {
      await requestJson(url, {
        method: 'POST',
        headers: { 'X-Request-ID': newRequestId() },
      });
      setActionResult(`${label} recorded in canonical DTMO governance state.`);
      await loadState(state.item_id);
    } catch (actionError) {
      setActionResult(`${label} blocked: ${actionError instanceof Error ? actionError.message : 'unknown error'}`);
    } finally {
      setAction(null);
    }
  }

  async function exportToMisp() {
    if (!state) return;
    const params = new URLSearchParams({ distribution, tlp });
    if (sharingGroup.trim()) params.set('sharing_group_id', sharingGroup.trim());
    await runAction('MISP export', `/api/v1/intelligence/${encodeURIComponent(state.item_id)}/misp-export?${params}`);
  }

  function submitItem(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void loadState();
  }

  const approvalSeparationBlocked = Boolean(
    state?.reviewed_by && session?.subject && state.reviewed_by === session.subject,
  );
  const canReview = Boolean(state && state.review_status !== 'reviewed' && state.principal_actions.can_review);
  const canApprove = Boolean(
    state
    && state.review_status === 'reviewed'
    && !state.share_approved
    && state.principal_actions.can_approve_share
    && !approvalSeparationBlocked,
  );
  const canExport = Boolean(
    state
    && state.export_eligible
    && state.misp_export_enabled
    && state.misp_export_configured
    && state.principal_actions.can_approve_share,
  );

  return (
    <section className="misp-sharing-workspace" aria-labelledby="workspace-title">
      <header className="workspace-heading sharing-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Sharing &amp; Exchange</h1>
          <p>Human-governed MISP exchange over canonical DTMO review, approval, handling restrictions and replay evidence.</p>
        </div>
        <div className="heading-statuses">
          <span className="phase-badge">11.10g MISP Sharing</span>
          <span className="phase-badge available">Human authority required</span>
        </div>
      </header>

      <article className="surface sharing-loader">
        <div className="panel-heading">
          <div><p className="eyebrow">Canonical object</p><h2>Open sharing state</h2></div>
          <span className="evidence-label">read:intelligence</span>
        </div>
        <form onSubmit={submitItem} className="sharing-item-form">
          <label>
            <span>Canonical intelligence item UUID</span>
            <input value={itemId} onChange={(event) => setItemId(event.target.value)} placeholder="00000000-0000-0000-0000-000000000000" required />
          </label>
          <button type="submit" className="button primary" disabled={loading || !itemId.trim()}>{loading ? 'Loading…' : 'Load sharing state'}</button>
        </form>
        <p className="boundary-copy">Opening an item does not grant review, sharing or publication authority. All mutation decisions remain server-authorized and audited.</p>
      </article>

      {error && <div className="surface panel-state error-state"><strong>Sharing state unavailable</strong><span>{error}. No approval, export or MISP-health conclusion is inferred.</span></div>}

      {state && (
        <>
          <section className="sharing-grid">
            <article className="surface sharing-governance">
              <header className="panel-heading">
                <div><p className="eyebrow">Decision chain</p><h2>{state.title}</h2></div>
                <span className="evidence-label">{state.source_id}</span>
              </header>

              <ol className="decision-chain">
                <li className={state.review_status === 'reviewed' ? 'complete' : 'pending'}>
                  <span>1</span><div><strong>Independent review</strong><small>{state.review_status === 'reviewed' ? `Reviewed by ${state.reviewed_by ?? 'attribution missing'}` : 'Human review required before sharing approval'}</small></div>
                </li>
                <li className={state.share_approved ? 'complete' : 'pending'}>
                  <span>2</span><div><strong>Separate share approval</strong><small>{state.share_approved ? `Approved by ${state.share_approved_by ?? 'attribution missing'}` : 'Approver must be a different human principal from the reviewer'}</small></div>
                </li>
                <li className={state.export_eligible ? 'complete' : 'pending'}>
                  <span>3</span><div><strong>Export eligibility</strong><small>{state.export_eligible ? 'Canonical revision is eligible for an unpublished MISP export' : state.export_blockers.join(' · ')}</small></div>
                </li>
                <li>
                  <span>4</span><div><strong>Publication / synchronization</strong><small>Not authorized or implemented in this workspace. Exported MISP events remain unpublished.</small></div>
                </li>
              </ol>

              <div className="sharing-actions" aria-label="Governed sharing actions">
                <button className="button secondary" type="button" disabled={!canReview || action !== null} onClick={() => void runAction('Review', `/api/v1/intelligence/${encodeURIComponent(state.item_id)}/review`)}>Record review</button>
                <button className="button secondary" type="button" disabled={!canApprove || action !== null} onClick={() => void runAction('Share approval', `/api/v1/intelligence/${encodeURIComponent(state.item_id)}/share-approval`)}>Approve sharing</button>
              </div>
              {approvalSeparationBlocked && <p className="separation-warning">This principal performed the review and therefore cannot approve sharing for the same item.</p>}
              {actionResult && <p className="action-result" role="status">{actionResult}</p>}
            </article>

            <article className="surface sharing-export">
              <header className="panel-heading">
                <div><p className="eyebrow">MISP export</p><h2>Create unpublished event</h2></div>
                <span className={`status-chip ${state.misp_export_enabled && state.misp_export_configured ? 'success' : 'neutral'}`}><span className="status-dot" />{state.misp_export_enabled ? (state.misp_export_configured ? 'configured' : 'not configured') : 'disabled'}</span>
              </header>
              <div className="export-fields">
                <label><span>Distribution</span><select value={distribution} onChange={(event) => setDistribution(event.target.value)}><option value="0">0 — Your organisation only</option><option value="1">1 — This community only</option><option value="2">2 — Connected communities</option><option value="3">3 — All communities</option><option value="4">4 — Sharing group</option></select></label>
                <label><span>TLP</span><select value={tlp} onChange={(event) => setTlp(event.target.value)}><option value="tlp:amber">TLP:AMBER</option><option value="tlp:amber+strict">TLP:AMBER+STRICT</option><option value="tlp:green">TLP:GREEN</option><option value="tlp:clear">TLP:CLEAR</option><option value="tlp:red">TLP:RED</option></select></label>
                <label><span>Sharing group</span><input value={sharingGroup} onChange={(event) => setSharingGroup(event.target.value)} disabled={distribution !== '4'} placeholder="required only for distribution 4" /></label>
              </div>
              <button className="button primary export-button" type="button" disabled={!canExport || action !== null || (distribution === '4' && !sharingGroup.trim())} onClick={() => void exportToMisp()}>{action === 'MISP export' ? 'Exporting…' : 'Export approved intelligence'}</button>
              <p className="boundary-copy"><strong>Boundary:</strong> this creates a MISP event with <code>published=false</code>. There is no publish or synchronize control in Phase 11.10g.</p>
            </article>
          </section>

          <section className="sharing-grid lower-grid">
            <article className="surface">
              <header className="panel-heading"><div><p className="eyebrow">Handling restrictions</p><h2>Authoritative source constraints</h2></div><span className="evidence-label">fail closed</span></header>
              {!state.misp_restrictions && <p className="panel-state">No authoritative MISP source restriction projection is attached to this canonical item.</p>}
              {state.misp_restrictions && (
                <dl className="sharing-facts">
                  <div><dt>Authoritative</dt><dd>{state.misp_restrictions.restriction_authoritative ? 'yes' : 'no'}</dd></div>
                  <div><dt>Distribution</dt><dd>{displayRestriction(state.misp_restrictions.distribution)}</dd></div>
                  <div><dt>Sharing group</dt><dd>{displayRestriction(state.misp_restrictions.sharing_group_id)}</dd></div>
                  <div><dt>TLP tags</dt><dd>{state.misp_restrictions.tlp_tags.join(', ') || 'not recorded'}</dd></div>
                </dl>
              )}
              <a className="text-link" href={state.canonical_url} target="_blank" rel="noreferrer">Open canonical source evidence →</a>
            </article>

            <article className="surface">
              <header className="panel-heading"><div><p className="eyebrow">Delivery evidence</p><h2>MISP export history</h2></div><span className="evidence-label">replay protected</span></header>
              {!state.misp_exports.length && <p className="panel-state">No persisted MISP export evidence exists for this item.</p>}
              <div className="export-history">
                {state.misp_exports.map((record, index) => (
                  <div className="export-record" key={`${record.event_uuid}-${index}`}>
                    <span className={`status-chip ${record.status === 'success' ? 'success' : record.status === 'uncertain' ? 'error' : 'neutral'}`}><span className="status-dot" />{record.status}</span>
                    <div><strong>{record.event_uuid || 'event UUID unavailable'}</strong><small>MISP event {record.misp_event_id ?? 'not confirmed'} · distribution {record.distribution ?? '—'} · {record.tlp ?? 'TLP not recorded'}</small></div>
                  </div>
                ))}
              </div>
            </article>
          </section>

          <article className="surface evidence-surface sharing-evidence">
            <div><p className="eyebrow">Evidence boundary</p><h2>Configuration and transfer evidence are not publication authority</h2></div>
            <p>{state.evidence_boundary}</p>
            <div className="authority-strip"><span>Runtime health: not inferred</span><span>Publication authority: no</span><span>Synchronization authority: no</span></div>
          </article>
        </>
      )}
    </section>
  );
}
