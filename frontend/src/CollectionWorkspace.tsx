import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

type Session = { subject: string; roles: string[]; permissions: string[] };
type Source = {
  id: string;
  name: string;
  source_type: string;
  endpoint_url: string;
  enabled: boolean;
  interval_seconds: number;
  reliability: string;
  secret_ref: string | null;
  authentication_mode: string;
  owner: string;
};
type CatalogEntry = {
  id: string;
  name: string;
  endpoint_url: string;
  execution_status: string;
  execution_profile: string;
  reliability: string;
  recommended_interval_seconds: number;
};
type ActionResult = {
  id?: string;
  valid?: boolean;
  status?: string;
  records?: number;
  inserted?: number;
  indexed?: number;
  error?: string | null;
  alert_state?: string;
  ingested?: boolean;
  publication_gate?: string;
  note?: string;
};

async function readJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === 'object' && body && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

async function writeJson<T>(url: string, method: 'POST' | 'PATCH', body?: object): Promise<T> {
  const response = await fetch(url, {
    method,
    credentials: 'same-origin',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json', 'X-Request-ID': crypto.randomUUID() },
    body: body ? JSON.stringify(body) : undefined,
  });
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof payload === 'object' && payload && 'detail' in payload ? String((payload as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return payload as T;
}

export function CollectionWorkspace() {
  const client = useQueryClient();
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<ActionResult | null>(null);

  const session = useQuery({ queryKey: ['collection', 'session'], queryFn: () => readJson<Session>('/api/v1/ui/session'), retry: false });
  const allowed = session.data?.permissions.includes('manage:connectors') ?? false;
  const catalog = useQuery({ queryKey: ['collection', 'catalog'], queryFn: () => readJson<CatalogEntry[]>('/api/v1/admin/sources/catalog'), enabled: allowed, retry: false });
  const sources = useQuery({ queryKey: ['collection', 'sources'], queryFn: () => readJson<Source[]>('/api/v1/admin/sources'), enabled: allowed, retry: false });

  const action = useMutation({
    mutationFn: async ({ sourceId, verb }: { sourceId: string; verb: 'validate' | 'test' | 'run' }) => writeJson<ActionResult>(`/api/v1/admin/sources/${encodeURIComponent(sourceId)}/${verb}`, 'POST'),
    onSuccess: (data) => {
      setResult(data);
      void client.invalidateQueries({ queryKey: ['collection', 'sources'] });
    },
  });
  const bootstrap = useMutation({
    mutationFn: () => writeJson<Source[]>('/api/v1/admin/sources/catalog/bootstrap', 'POST'),
    onSuccess: (data) => {
      setResult({ status: 'bootstrap-completed', records: data.length, ingested: false, publication_gate: 'human-review-and-separate-share-approval-required' });
      void client.invalidateQueries({ queryKey: ['collection', 'sources'] });
    },
  });
  const activation = useMutation({
    mutationFn: ({ sourceId, enabled }: { sourceId: string; enabled: boolean }) => writeJson<Source>(`/api/v1/admin/sources/${encodeURIComponent(sourceId)}`, 'PATCH', { enabled }),
    onSuccess: (source) => {
      setResult({ id: source.id, status: source.enabled ? 'enabled' : 'disabled', note: 'Source registry state updated and audited.' });
      void client.invalidateQueries({ queryKey: ['collection', 'sources'] });
    },
  });

  const registered = useMemo(() => new Map((sources.data ?? []).map((source) => [source.id, source])), [sources.data]);
  const activeSource = selected ? registered.get(selected) : undefined;

  return (
    <section className="workspace-foundation" aria-labelledby="workspace-title">
      <header className="workspace-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Sources & Collection</h1>
          <p>Governed source catalog, activation, validation, testing and explicit collection execution through DTMO-owned APIs.</p>
        </div>
        <div className="heading-statuses"><span className="phase-badge">11.10q functional recovery</span><span className="evidence-label">Collection ≠ publication</span></div>
      </header>

      {!session.isPending && !allowed && <article className="surface panel-state error-state"><strong>Collection controls unavailable</strong><span>This workspace requires server-authorized <code>manage:connectors</code>. No browser-side bypass or upstream credential is available.</span></article>}
      {allowed && (
        <>
          <article className="surface command-panel">
            <header className="panel-heading"><div><p className="eyebrow">Control plane</p><h2>Registered sources</h2></div><button type="button" onClick={() => bootstrap.mutate()} disabled={bootstrap.isPending}>Bootstrap supported catalog</button></header>
            <p className="boundary-copy">Bootstrap is idempotent and registers supported adapters disabled by default. An administrator can then explicitly enable or disable a registered source, validate it, run a non-ingesting test, and perform an attributable collection run.</p>
            {(sources.isError || catalog.isError) && <p className="panel-state error-state">Canonical source state is unavailable. No healthy or zero-source state is inferred.</p>}
          </article>

          <div className="command-grid">
            <article className="surface command-panel">
              <header className="panel-heading"><div><p className="eyebrow">Catalog</p><h2>Code-reviewed source profiles</h2></div><span className="evidence-label">{catalog.data?.length ?? 0} entries</span></header>
              <div className="integration-list">
                {(catalog.data ?? []).map((entry) => {
                  const source = registered.get(entry.id);
                  return <button className="integration-row" type="button" key={entry.id} onClick={() => { setSelected(entry.id); setResult(null); }} aria-pressed={selected === entry.id}>
                    <span className={`integration-state state-${source?.enabled ? 'enabled' : 'disabled'}`} aria-hidden="true" />
                    <div><strong>{entry.name}</strong><span>{entry.execution_status} · {source ? (source.enabled ? 'enabled' : 'registered disabled') : 'not registered'}</span></div>
                    <time>{entry.reliability}</time>
                  </button>;
                })}
              </div>
            </article>

            <article className="surface command-panel">
              <header className="panel-heading"><div><p className="eyebrow">Execution</p><h2>{selected ? activeSource?.name ?? selected : 'Select a source'}</h2></div><span className="evidence-label">Human admin only</span></header>
              {!selected && <p className="panel-state">Select a catalog source to inspect registered state and bounded actions.</p>}
              {selected && !activeSource && <p className="panel-state">This catalog entry is not registered. Bootstrap supported catalog sources first.</p>}
              {selected && activeSource && <>
                <p className="boundary-copy">{activeSource.endpoint_url}<br />Auth mode: {activeSource.authentication_mode}; credential values remain server-side.</p>
                <div className="quick-grid">
                  <button type="button" className="quick-action" disabled={activation.isPending} onClick={() => activation.mutate({ sourceId: selected, enabled: !activeSource.enabled })}><span aria-hidden="true">{activeSource.enabled ? '■' : '▶'}</span><div><strong>{activeSource.enabled ? 'Disable source' : 'Enable source'}</strong><small>Persist and audit source activation state.</small></div></button>
                  {(['validate', 'test', 'run'] as const).map((verb) => <button key={verb} type="button" className="quick-action" disabled={action.isPending} onClick={() => action.mutate({ sourceId: selected, verb })}><span aria-hidden="true">{verb === 'run' ? '▶' : '✓'}</span><div><strong>{verb}</strong><small>{verb === 'validate' ? 'Validate governed endpoint policy.' : verb === 'test' ? 'Execute without ingestion.' : 'Explicitly collect and ingest attributable records.'}</small></div></button>)}
                </div>
              </>}
              {action.isError && <p className="panel-state error-state">{action.error.message}</p>}
              {activation.isError && <p className="panel-state error-state">{activation.error.message}</p>}
              {bootstrap.isError && <p className="panel-state error-state">{bootstrap.error.message}</p>}
              {result && <div className="panel-state"><strong>Last bounded action</strong><span>Status: {result.status ?? (result.valid === true ? 'valid' : result.valid === false ? 'invalid' : 'completed')} · records: {result.records ?? '—'} · inserted: {result.inserted ?? '—'} · indexed: {result.indexed ?? '—'}</span><span>{result.error ? `Error: ${result.error}` : result.publication_gate ?? result.note ?? 'No publication authority granted.'}</span></div>}
            </article>
          </div>

          <article className="surface evidence-surface"><div><p className="eyebrow">Evidence boundary</p><h2>Attributable collection without inferred trust</h2></div><p>Activation, connectivity, successful testing or ingestion proves only the recorded administrative or collection action. It does not prove source truth, compromise, review completion, external-share authority, production readiness or publication authorization. Connector isolation and server-side RBAC remain fail closed.</p></article>
        </>
      )}
    </section>
  );
}
