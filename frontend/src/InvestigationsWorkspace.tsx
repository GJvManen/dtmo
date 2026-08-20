import { useEffect, useMemo, useState } from 'react';
import type { FormEvent } from 'react';

import './investigations.css';

type InvestigationHandoff = {
  handoff_id: string;
  request_id: string;
  status: string;
  requested_by: string;
  organization: string;
  tlp: string;
  pap: string;
  thehive_case_id: string | null;
  thehive_case_number: string | null;
  error_detail: string | null;
  created_at: string;
  updated_at: string;
  external_share_authorized: boolean;
  local_compromise_proven: boolean;
};

type InvestigationState = {
  item_id: string;
  title: string;
  source_id: string;
  canonical_url: string;
  severity: string;
  review_status: string;
  provenance_count: number;
  authoritative_tlp_tags: string[];
  handoff_history: InvestigationHandoff[];
  handoff_blockers: string[];
  principal_actions: { can_handoff: boolean };
  feature_enabled: boolean;
  configured: boolean;
  runtime_health_claim: boolean;
  upstream_case_readback_supported: boolean;
  alerts_tasks_timeline_persisted: boolean;
  external_share_authority: boolean;
  local_compromise_proof: boolean;
  evidence_boundary: string;
};

type HandoffResponse = {
  handoff_id: string;
  request_id: string;
  item_id: string;
  status: string;
  organization: string;
  thehive_case_id: string | null;
  thehive_case_number: string | null;
  external_share_authorized: boolean;
  local_compromise_proven: boolean;
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

function displayTime(value: string) {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString();
}

function statusTone(status: string) {
  if (status === 'delivered') return 'success';
  if (status === 'ambiguous') return 'error';
  if (status === 'failed') return 'error';
  return 'neutral';
}

export function InvestigationsWorkspace() {
  const initialItem = useMemo(() => new URLSearchParams(window.location.search).get('item') ?? '', []);
  const [itemId, setItemId] = useState(initialItem);
  const [state, setState] = useState<InvestigationState | null>(null);
  const [summary, setSummary] = useState('');
  const [tlp, setTlp] = useState('amber');
  const [pap, setPap] = useState('amber');
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [actionResult, setActionResult] = useState<string | null>(null);

  useEffect(() => {
    if (initialItem) void loadState(initialItem);
    // initial deep-link load must run once only
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialItem]);

  async function loadState(id = itemId.trim()) {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const next = await requestJson<InvestigationState>(`/api/v1/thehive/items/${encodeURIComponent(id)}/investigation`);
      setState(next);
      setItemId(id);
      const url = new URL(window.location.href);
      url.searchParams.set('item', id);
      window.history.replaceState({}, '', url);
    } catch (loadError) {
      setState(null);
      setError(loadError instanceof Error ? loadError.message : 'Investigation state unavailable');
    } finally {
      setLoading(false);
    }
  }

  async function createCase() {
    if (!state || !summary.trim()) return;
    setCreating(true);
    setActionResult(null);
    setError(null);
    try {
      const result = await requestJson<HandoffResponse>(
        `/api/v1/thehive/items/${encodeURIComponent(state.item_id)}/cases`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            request_id: crypto.randomUUID(),
            summary: summary.trim(),
            tlp,
            pap,
          }),
        },
      );
      setActionResult(
        result.status === 'delivered'
          ? `TheHive case handoff delivered${result.thehive_case_number ? ` as case #${result.thehive_case_number}` : ''}.`
          : `TheHive handoff recorded with status ${result.status}.`,
      );
      setSummary('');
    } catch (actionError) {
      setActionResult(`Case handoff blocked: ${actionError instanceof Error ? actionError.message : 'unknown error'}`);
    } finally {
      setCreating(false);
      await loadState(state.item_id);
    }
  }

  function submitItem(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void loadState();
  }

  const reconciliationRequired = Boolean(
    state?.handoff_history.some((record) => record.status === 'reserved' || record.status === 'ambiguous'),
  );
  const canCreate = Boolean(
    state
    && state.principal_actions.can_handoff
    && state.feature_enabled
    && state.configured
    && state.provenance_count > 0
    && state.handoff_blockers.length === 0
    && !reconciliationRequired
    && summary.trim(),
  );

  return (
    <section className="investigations-workspace" aria-labelledby="workspace-title">
      <header className="workspace-heading investigations-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Investigations</h1>
          <p>Canonical DTMO investigation context with explicit human-authorized TheHive case handoff and durable reconciliation evidence.</p>
        </div>
        <div className="heading-statuses">
          <span className="phase-badge">11.10h TheHive Investigations</span>
          <span className="phase-badge available">Human case authority required</span>
        </div>
      </header>

      <article className="surface investigation-loader">
        <header className="panel-heading">
          <div><p className="eyebrow">Canonical object</p><h2>Open investigation context</h2></div>
          <span className="evidence-label">read:intelligence</span>
        </header>
        <form className="investigation-item-form" onSubmit={submitItem}>
          <label>
            <span>Canonical intelligence item UUID</span>
            <input value={itemId} onChange={(event) => setItemId(event.target.value)} placeholder="00000000-0000-0000-0000-000000000000" required />
          </label>
          <button className="button primary" type="submit" disabled={loading || !itemId.trim()}>{loading ? 'Loading…' : 'Load investigation'}</button>
        </form>
        <p className="boundary-copy">Opening an investigation grants no case-creation, responder, sharing or compromise authority. Mutation remains server-authorized by <code>handoff:case</code>.</p>
      </article>

      {error && <div className="surface panel-state error-state"><strong>Investigation state unavailable</strong><span>{error}. No case, TheHive-health or compromise conclusion is inferred.</span></div>}

      {state && (
        <>
          <section className="investigation-grid">
            <article className="surface canonical-investigation">
              <header className="panel-heading">
                <div><p className="eyebrow">Canonical evidence</p><h2>{state.title}</h2></div>
                <span className={`severity-pill severity-${state.severity}`}>{state.severity}</span>
              </header>
              <dl className="investigation-facts">
                <div><dt>Source</dt><dd>{state.source_id}</dd></div>
                <div><dt>Review state</dt><dd>{state.review_status}</dd></div>
                <div><dt>Provenance records</dt><dd>{state.provenance_count}</dd></div>
                <div><dt>Authoritative TLP</dt><dd>{state.authoritative_tlp_tags.join(', ') || 'not recorded'}</dd></div>
              </dl>
              <a className="text-link" href={state.canonical_url} target="_blank" rel="noreferrer">Open canonical source evidence →</a>
            </article>

            <article className="surface case-create-panel">
              <header className="panel-heading">
                <div><p className="eyebrow">TheHive case handoff</p><h2>Create one governed case request</h2></div>
                <span className={`status-chip ${state.feature_enabled && state.configured ? 'success' : 'neutral'}`}><span className="status-dot" />{state.feature_enabled ? (state.configured ? 'configured' : 'not configured') : 'disabled'}</span>
              </header>

              {state.handoff_blockers.length > 0 && (
                <div className="handoff-blockers" role="status">
                  <strong>Case handoff prerequisites are not satisfied</strong>
                  <ul>{state.handoff_blockers.map((blocker) => <li key={blocker}>{blocker}</li>)}</ul>
                </div>
              )}
              {reconciliationRequired && (
                <div className="handoff-blockers reconciliation" role="alert">
                  <strong>Manual reconciliation required</strong>
                  <span>A reserved or ambiguous prior handoff exists. This workspace will not issue another case request until that state is reconciled.</span>
                </div>
              )}

              <label className="summary-field">
                <span>Reviewed case summary</span>
                <textarea value={summary} onChange={(event) => setSummary(event.target.value)} maxLength={4000} rows={5} placeholder="Provide the minimized, reviewed context that TheHive needs for this case." />
              </label>
              <div className="handling-fields">
                <label><span>TLP</span><select value={tlp} onChange={(event) => setTlp(event.target.value)}><option value="clear">TLP:CLEAR</option><option value="green">TLP:GREEN</option><option value="amber">TLP:AMBER</option><option value="amber+strict">TLP:AMBER+STRICT</option><option value="red">TLP:RED</option></select></label>
                <label><span>PAP</span><select value={pap} onChange={(event) => setPap(event.target.value)}><option value="clear">PAP:CLEAR</option><option value="green">PAP:GREEN</option><option value="amber">PAP:AMBER</option><option value="red">PAP:RED</option></select></label>
              </div>
              <button className="button primary" type="button" disabled={!canCreate || creating} onClick={() => void createCase()}>{creating ? 'Creating governed handoff…' : 'Create TheHive case handoff'}</button>
              <p className="boundary-copy"><strong>Boundary:</strong> this action creates a minimized case through the DTMO server-side adapter only. It does not authorize responders, external sharing, publication or automatic incident response.</p>
              {actionResult && <p className="action-result" role="status">{actionResult}</p>}
            </article>
          </section>

          <section className="investigation-grid lower-investigation-grid">
            <article className="surface">
              <header className="panel-heading"><div><p className="eyebrow">Durable handoff evidence</p><h2>Case handoff history</h2></div><span className="evidence-label">reconciliation-aware</span></header>
              {!state.handoff_history.length && <p className="panel-state">No persisted TheHive handoff evidence exists for this canonical item.</p>}
              <div className="handoff-history">
                {state.handoff_history.map((record) => (
                  <article className="handoff-record" key={record.handoff_id}>
                    <span className={`status-chip ${statusTone(record.status)}`}><span className="status-dot" />{record.status}</span>
                    <div>
                      <strong>{record.thehive_case_number ? `TheHive case #${record.thehive_case_number}` : record.thehive_case_id ?? 'Case identity not confirmed'}</strong>
                      <small>{record.organization} · requested by {record.requested_by} · TLP {record.tlp} · PAP {record.pap}</small>
                      <small>{displayTime(record.updated_at)} · request {record.request_id}</small>
                      {record.error_detail && <span className="record-error">{record.error_detail}</span>}
                    </div>
                  </article>
                ))}
              </div>
            </article>

            <article className="surface">
              <header className="panel-heading"><div><p className="eyebrow">Scope boundary</p><h2>No fabricated case detail</h2></div><span className="evidence-label">accepted persistence only</span></header>
              <ul className="scope-boundary-list">
                <li><strong>Alerts:</strong> not persisted/read back by the accepted TheHive boundary.</li>
                <li><strong>Tasks:</strong> not persisted/read back by the accepted TheHive boundary.</li>
                <li><strong>Case timeline:</strong> not persisted/read back by the accepted TheHive boundary.</li>
                <li><strong>Responders:</strong> no execution authority is exposed in Phase 11.10h.</li>
              </ul>
              <p className="boundary-copy">A delivered handoff proves only the persisted DTMO handoff result and confirmed case identity returned at creation time. It does not prove subsequent upstream case state or action.</p>
            </article>
          </section>

          <article className="surface evidence-surface investigations-evidence">
            <div><p className="eyebrow">Evidence boundary</p><h2>Case context is evidence, not a compromise verdict</h2></div>
            <p>{state.evidence_boundary}</p>
            <div className="authority-strip"><span>Runtime health: not inferred</span><span>External share authority: no</span><span>Local compromise proof: no</span></div>
          </article>
        </>
      )}
    </section>
  );
}
