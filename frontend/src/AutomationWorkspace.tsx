import { useMemo, useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';

type Session = { subject: string; roles: string[]; permissions: string[] };
type SchedulerJob = { id: string; next_run_time: string };
type Health = {
  status: string;
  version: string;
  environment: string;
  scheduler?: { running: boolean; started_at: string | null; jobs: SchedulerJob[] };
};
type Connector = {
  id: string;
  enabled: boolean;
  reliability: string;
  schedule_seconds: number;
  manual_run_available: boolean;
  mode?: string;
};
type RunResult = {
  connector_id?: string;
  status?: string;
  records?: number;
  inserted?: number;
  indexed?: number;
  attempts?: number;
  error?: string | null;
  reason?: string;
  alert_state?: string;
  correlation_id?: string;
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

async function runConnector(id: string): Promise<RunResult> {
  const response = await fetch(`/connectors/${encodeURIComponent(id)}/run`, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { Accept: 'application/json', 'X-Request-ID': crypto.randomUUID() },
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === 'object' && body && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as RunResult;
}

export function AutomationWorkspace() {
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<RunResult | null>(null);
  const session = useQuery({ queryKey: ['automation', 'session'], queryFn: () => readJson<Session>('/api/v1/ui/session'), retry: false });
  const health = useQuery({ queryKey: ['automation', 'health'], queryFn: () => readJson<Health>('/health'), retry: false });
  const connectors = useQuery({ queryKey: ['automation', 'connectors'], queryFn: () => readJson<Connector[]>('/connectors'), retry: false });
  const allowed = session.data?.permissions.includes('manage:connectors') ?? false;
  const human = !(session.data?.roles ?? []).includes('service_account');
  const executable = allowed && human;
  const jobs = health.data?.scheduler?.jobs ?? [];
  const jobIds = useMemo(() => new Set(jobs.map((job) => job.id)), [jobs]);

  const execution = useMutation({
    mutationFn: (id: string) => runConnector(id),
    onSuccess: (data) => setResult(data),
  });

  return (
    <section className="workspace-foundation" aria-labelledby="workspace-title">
      <header className="workspace-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Automation & Playbooks</h1>
          <p>Governed scheduled jobs and explicit bounded collection playbooks through DTMO-owned control-plane APIs.</p>
        </div>
        <div className="heading-statuses"><span className="phase-badge">11.10k Automation & Playbooks</span><span className="evidence-label">Automation ≠ remediation authority</span></div>
      </header>

      {(session.isError || health.isError || connectors.isError) && <article className="surface panel-state error-state"><strong>Canonical automation state unavailable</strong><span>No runnable, healthy or production-ready automation state is inferred while DTMO control-plane data is unavailable.</span></article>}

      <div className="command-grid">
        <article className="surface command-panel">
          <header className="panel-heading"><div><p className="eyebrow">Scheduler</p><h2>Registered jobs</h2></div><span className="evidence-label">{health.data?.scheduler?.running ? 'runtime reports running' : 'not running / not observed'}</span></header>
          {!jobs.length && <p className="panel-state">No scheduled jobs are currently reported by the DTMO scheduler.</p>}
          <div className="integration-list">
            {jobs.map((job) => <div className="integration-row" key={job.id}><span className="integration-state state-enabled" aria-hidden="true" /><div><strong>{job.id}</strong><span>Server-owned schedule; browser cannot alter scheduler state.</span></div><time>{job.next_run_time}</time></div>)}
          </div>
        </article>

        <article className="surface command-panel">
          <header className="panel-heading"><div><p className="eyebrow">Playbook catalog</p><h2>Bounded collection runs</h2></div><span className="evidence-label">Human invocation only</span></header>
          <p className="boundary-copy">These playbooks reuse the accepted connector execution path. They collect and ingest attributable intelligence only; they cannot create cases, remediate assets, approve sharing or publish intelligence.</p>
          <div className="integration-list">
            {(connectors.data ?? []).map((connector) => <button type="button" className="integration-row" key={connector.id} onClick={() => { setSelected(connector.id); setResult(null); }} aria-pressed={selected === connector.id}>
              <span className={`integration-state state-${connector.enabled ? 'enabled' : 'disabled'}`} aria-hidden="true" />
              <div><strong>{connector.id}</strong><span>{connector.reliability} · {jobIds.has(connector.id) ? 'scheduled' : 'not scheduled'} · {connector.mode ?? 'bounded collection'}</span></div>
              <time>{connector.schedule_seconds}s</time>
            </button>)}
          </div>
        </article>

        <article className="surface command-panel">
          <header className="panel-heading"><div><p className="eyebrow">Execution authority</p><h2>{selected ?? 'Select a playbook'}</h2></div><span className="evidence-label">Server RBAC authoritative</span></header>
          {!session.isPending && !allowed && <p className="panel-state error-state">This principal lacks <code>manage:connectors</code>; execution is unavailable.</p>}
          {!session.isPending && allowed && !human && <p className="panel-state error-state">Service-account sessions are not exposed as human playbook execution authority in this workspace.</p>}
          {selected && <button type="button" disabled={!executable || execution.isPending} onClick={() => execution.mutate(selected)}>Run bounded collection playbook</button>}
          {execution.isError && <p className="panel-state error-state">{execution.error.message}</p>}
          {result && <div className="panel-state"><strong>Last bounded execution</strong><span>Status: {result.status ?? 'completed'} · records: {result.records ?? '—'} · inserted: {result.inserted ?? '—'} · indexed: {result.indexed ?? '—'}</span><span>{result.error ? `Error: ${result.error}` : result.reason ?? `Correlation: ${result.correlation_id ?? 'not returned'}`}</span></div>}
        </article>
      </div>

      <article className="surface evidence-surface"><div><p className="eyebrow">Evidence boundary</p><h2>Automation without autonomous decision authority</h2></div><p>A schedule or successful run proves only the recorded scheduler or connector action. It does not prove source truth, compromise, containment, remediation, review completion, case creation, external-share or publication authority, production readiness or production authorization. Credentials and execution remain server-side and RBAC-governed.</p></article>
    </section>
  );
}
