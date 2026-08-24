import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

type Session = { permissions: string[] };
type IntegrationRow = {
  id: string;
  name: string;
  enabled: boolean;
  api_base: string;
  credential_configured: boolean;
  can_activate: boolean;
  activation_blockers: string[];
  state: 'ready' | 'credential-required' | 'configuration-required' | 'disabled';
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

async function enableIntegration(row: IntegrationRow): Promise<IntegrationRow> {
  const response = await fetch(`/api/v1/admin/integrations/${encodeURIComponent(row.id)}`, {
    method: 'PATCH',
    credentials: 'same-origin',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json', 'X-Request-ID': crypto.randomUUID() },
    body: JSON.stringify({ enabled: true, api_base: row.api_base }),
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === 'object' && body && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as IntegrationRow;
}

export function FrameworkIntegrationReadiness() {
  const client = useQueryClient();
  const session = useQuery({ queryKey: ['framework-readiness', 'session'], queryFn: () => readJson<Session>('/api/v1/ui/session'), retry: false });
  const allowed = session.data?.permissions.includes('manage:connectors') ?? false;
  const integrations = useQuery({
    queryKey: ['administration', 'integrations'],
    queryFn: () => readJson<IntegrationRow[]>('/api/v1/admin/integrations'),
    enabled: allowed,
    retry: false,
  });
  const activation = useMutation({
    mutationFn: enableIntegration,
    onSuccess: () => void client.invalidateQueries({ queryKey: ['administration', 'integrations'] }),
  });

  if (session.isPending) return <p className="panel-state">Checking framework activation readiness…</p>;
  if (!allowed) return null;

  const rows = integrations.data ?? [];
  const actionable = rows.filter((row) => row.can_activate);

  return (
    <section className="workspace-foundation" aria-labelledby="framework-readiness-title" data-admin-section="framework-activation-readiness">
      <article className="surface command-panel">
        <header className="panel-heading"><div><p className="eyebrow">Framework integrations</p><h2 id="framework-readiness-title">Activation readiness</h2></div><span className="evidence-label">Server-derived blockers · no auto-enable</span></header>
        <p className="boundary-copy">Activation readiness is derived by the server. Endpoint and credential presence are necessary but not sufficient: required object scopes, analyzer allowlists, organization scope and durable checkpoint configuration are evaluated before enablement. Runtime health remains a separate observation.</p>
        {integrations.isPending && <p className="panel-state">Loading integration readiness…</p>}
        {integrations.isError && <p className="panel-state error-state">Integration readiness unavailable: {integrations.error.message}</p>}
        {!integrations.isPending && !integrations.isError && rows.length > 0 && <div className="quick-grid">
          {rows.map((row) => {
            const status = row.enabled ? row.state : row.can_activate ? 'configured · activation required' : 'configuration blocked';
            return <article className="quick-action" key={row.id} data-framework-readiness={row.id}>
              <span aria-hidden="true">◇</span><div><strong>{row.name}</strong><small>{status}</small><small>{row.activation_blockers.length > 0 ? `Required before activation: ${row.activation_blockers.join(', ')}.` : row.enabled ? 'Required configuration is present; runtime health is not implied.' : 'All activation prerequisites are present; explicit enablement remains required.'}</small></div>
              {row.can_activate && <button type="button" disabled={activation.isPending} onClick={() => activation.mutate(row)}>Enable {row.name}</button>}
            </article>;
          })}
        </div>}
        {!integrations.isPending && !integrations.isError && actionable.length === 0 && <p className="panel-state">No fully configured, disabled framework integration is currently awaiting activation.</p>}
        {activation.isError && <p className="panel-state error-state">Activation failed closed: {activation.error.message}</p>}
        {activation.isSuccess && <p className="panel-state">Integration enablement persisted through the governed Administration API. Verify runtime observation separately.</p>}
      </article>
    </section>
  );
}
