import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { NavLink } from 'react-router-dom';

type Session = { subject: string; roles: string[]; permissions: string[] };
type IntegrationRow = {
  id: string;
  name: string;
  enabled: boolean;
  api_base: string;
  credential_configured: boolean;
  state: 'ready' | 'credential-required' | 'configuration-required' | 'disabled';
  credential_boundary: string;
};

type DraftState = Record<string, { enabled: boolean; apiBase: string }>;

async function readJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === 'object' && body && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

async function patchJson<T>(url: string, body: object): Promise<T> {
  const response = await fetch(url, {
    method: 'PATCH',
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

export function AdministrationWorkspace() {
  const client = useQueryClient();
  const [drafts, setDrafts] = useState<DraftState>({});
  const [lastSaved, setLastSaved] = useState<string | null>(null);

  const session = useQuery({ queryKey: ['administration', 'session'], queryFn: () => readJson<Session>('/api/v1/ui/session'), retry: false });
  const allowed = session.data?.permissions.includes('manage:connectors') ?? false;
  const integrations = useQuery({
    queryKey: ['administration', 'integrations'],
    queryFn: () => readJson<IntegrationRow[]>('/api/v1/admin/integrations'),
    enabled: allowed,
    retry: false,
  });

  const rows = useMemo(() => integrations.data ?? [], [integrations.data]);
  const mutation = useMutation({
    mutationFn: ({ id, enabled, apiBase }: { id: string; enabled: boolean; apiBase: string }) => patchJson<IntegrationRow>(`/api/v1/admin/integrations/${encodeURIComponent(id)}`, { enabled, api_base: apiBase }),
    onSuccess: (row) => {
      setLastSaved(row.id);
      void client.invalidateQueries({ queryKey: ['administration', 'integrations'] });
    },
  });

  return (
    <section className="workspace-foundation" aria-labelledby="workspace-title">
      <header className="workspace-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Administration</h1>
          <p>Governed integration configuration from the canonical console. Endpoint and enablement are mutable; credentials remain server-side.</p>
        </div>
        <div className="heading-statuses"><span className="phase-badge">11.10q functional recovery</span><span className="evidence-label">Configuration ≠ runtime health</span></div>
      </header>

      <article className="surface command-panel">
        <header className="panel-heading"><div><p className="eyebrow">Framework integrations</p><h2>Runtime configuration</h2></div><button type="button" onClick={() => integrations.refetch()} disabled={!allowed || integrations.isFetching}>Refresh</button></header>
        <p className="boundary-copy">Changes are authorized by the server, persisted by DTMO and never return credential values to the browser. Enabling an integration does not by itself prove connectivity or healthy upstream operation.</p>
      </article>

      {!session.isPending && !allowed && <article className="surface panel-state error-state"><strong>Administration controls unavailable</strong><span>This workspace requires server-authorized <code>manage:connectors</code>. No browser-side bypass is provided.</span></article>}
      {allowed && integrations.isPending && <p className="panel-state">Loading governed integration settings…</p>}
      {allowed && integrations.isError && <article className="surface panel-state error-state"><strong>Integration configuration unavailable</strong><span>{integrations.error.message}</span></article>}

      {allowed && rows.length > 0 && <div className="command-grid">
        {rows.map((row) => {
          const draft = drafts[row.id] ?? { enabled: row.enabled, apiBase: row.api_base };
          const dirty = draft.enabled !== row.enabled || draft.apiBase !== row.api_base;
          return <article className="surface command-panel" key={row.id} data-integration={row.id}>
            <header className="panel-heading"><div><p className="eyebrow">{row.id}</p><h2>{row.name}</h2></div><span className={`status-chip ${row.state === 'ready' ? 'success' : 'neutral'}`}>{row.state.replaceAll('-', ' ')}</span></header>
            <label><span>API endpoint</span><input value={draft.apiBase} placeholder="https://platform.example/api" onChange={(event) => setDrafts((current) => ({ ...current, [row.id]: { ...draft, apiBase: event.target.value } }))} /></label>
            <label><input type="checkbox" checked={draft.enabled} onChange={(event) => setDrafts((current) => ({ ...current, [row.id]: { ...draft, enabled: event.target.checked } }))} /> Enabled</label>
            <p className="boundary-copy">Credential: {row.credential_configured ? 'configured server-side' : 'not configured'}. {row.credential_boundary}</p>
            <div className="quick-grid"><button type="button" className="quick-action" disabled={!dirty || mutation.isPending} onClick={() => mutation.mutate({ id: row.id, enabled: draft.enabled, apiBase: draft.apiBase })}><span aria-hidden="true">✓</span><div><strong>Save configuration</strong><small>Persist endpoint and enablement through the governed DTMO API.</small></div></button></div>
            {lastSaved === row.id && !mutation.isError && <p className="panel-state">Configuration saved and reloaded.</p>}
            {mutation.isError && <p className="panel-state error-state">{mutation.error.message}</p>}
          </article>;
        })}
      </div>}

      <article className="surface evidence-surface"><div><p className="eyebrow">Next operator step</p><h2>Configuration to collection</h2></div><p>After configuring an integration or source, continue to <NavLink to="/collection">Sources & Collection</NavLink> to bootstrap, enable, validate, test and explicitly run governed collection. Configuration alone never grants review, sharing, publication or external-assurance authority.</p></article>
    </section>
  );
}
