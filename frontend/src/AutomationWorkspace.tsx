import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

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
type PersistedSourceStatus = {
  id: string;
  health_status: string;
  last_success_at: string | null;
  last_failure_at: string | null;
  consecutive_failures: number;
  isolated_until: string | null;
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

function displayTime(value: string | null | undefined) {
  if (!value) return 'not recorded';
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString();
}

export function AutomationWorkspace() {
  const queryClient = useQueryClient();
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<RunResult | null>(null);
  const [observedAt, setObservedAt] = useState<string | null>(null);
  const session = useQuery({ queryKey: ['automation', 'session'], queryFn: () => readJson<Session>('/api/v1/ui/session'), retry: false });
  const health = useQuery({ queryKey: ['automation', 'health'], queryFn: () => readJson<Health>('/health'), retry: false });
  const connectors = useQuery({ queryKey: ['automation', 'connectors'], queryFn: () => readJson<Connector[]>('/connectors'), retry: false });
  const allowed = session.data?.permissions.includes('manage:connectors') ?? false;
  const human = !(session.data?.roles ?? []).includes('service_account');
  const executable = allowed && human;
  const persisted = useQuery({
    queryKey: ['automation', 'persisted-source-status'],
    queryFn: () => readJson<PersistedSourceStatus[]>('/api/v1/source-center/status'),
    enabled: allowed && human,
    retry: false,
  });
  const jobs = health.data?.scheduler?.jobs ?? [];
  const jobIds = useMemo(() => new Set(jobs.map((job) => job.id)), [jobs]);
  const selectedConnector = (connectors.data ?? []).find((connector) => connector.id === selected) ?? null;
  const persistedById = useMemo(() => new Map((persisted.data ?? []).map((item) => [item.id, item])), [persisted.data]);
  const selectedPersisted = selected ? persistedById.get(selected) ?? null : null;

  async function refreshRuntimeObservation() {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ['automation', 'health'] }),
      queryClient.invalidateQueries({ queryKey: ['automation', 'connectors'] }),
      queryClient.invalidateQueries({ queryKey: ['automation', 'persisted-source-status'] }),
    ]);
    setObservedAt(new Date().toISOString());
  }

  const execution = useMutation({
    mutationFn: (id: string) => runConnector(id),
    onSuccess: async (data) => {
      setResult(data);
      await refreshRuntimeObservation();
    },
  });

  return (
    <section className="workspace-foundation" aria-labelledby="workspace-title">
      <header className="workspace-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Automation &amp; Playbooks</h1>
          <p>Governed scheduled jobs and explicit bounded collection playbooks through DTMO-owned control-plane APIs.</p>
        </div>
        <div className="heading-statuses"><span className="phase-badge">11.10k Automation &amp; Playbooks · 11.10q recovery</span><span className="evidence-label">Automation ≠ remediation authority</span></div>
      </header>

      {(session.isError || health.isError || connectors.isError) && <article className="surface panel-state error-state"><strong>Canonical automation state unavailable</strong><span>No runnable, healthy or production-ready automation state is inferred while DTMO control-plane data is unavailable.</span></article>}

      <article className="surface command-panel">
        <header className="panel-heading"><div><p className="eyebrow">Runtime observation</p><h2>Refresh scheduler and playbook state</h2></div><span className="evidence-label">same-origin control plane</span></header>
        <button type="button" className="button secondary" disabled={health.isFetching || connectors.isFetching || persisted.isFetching} onClick={() => void refreshRuntimeObservation()}>{health.isFetching || connectors.isFetching || persisted.isFetching ? 'Refreshing…' : 'Refresh runtime observation'}</button>
        <p className="boundary-copy">{observedAt ? `Last explicit browser refresh: ${observedAt}` : 'Runtime state is loaded on workspace entry. Refresh explicitly before operational decisions.'}</p>
      </article>

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
              <div><strong>{connector.id}</strong><span>{connector.reliability} · {jobIds.has(connector.id) ? 'scheduled' : 'not scheduled'} · {connector.manual_run_available ? 'manual run available' : 'manual run unavailable'} · {connector.mode ?? 'bounded collection'}</span></div>
              <time>{connector.schedule_seconds}s</time>
            </button>)}
          </div>
        </article>

        <article className="surface command-panel">
          <header className="panel-heading"><div><p className="eyebrow">Execution authority</p><h2>{selected ?? 'Select a playbook'}</h2></div><span className="evidence-label">Server RBAC authoritative</span></header>
          {!session.isPending && !allowed && <p className="panel-state error-state">This principal lacks <code>manage:connectors</code>; execution is unavailable.</p>}
          {!session.isPending && allowed && !human && <p className="panel-state error-state">Service-account sessions are not exposed as human playbook execution authority in this workspace.</p>}
          {selectedConnector && !selectedConnector.manual_run_available && <p className="panel-state error-state">This connector does not advertise manual-run availability. The browser fails closed and will not invoke it.</p>}
          {selected && <button type="button" disabled={!executable || !selectedConnector?.manual_run_available || execution.isPending} onClick={() => execution.mutate(selected)}>Run bounded collection playbook</button>}
          {execution.isError && <p className="panel-state error-state">{execution.error.message}</p>}
          {result && <div className="panel-state"><strong>Observed bounded execution result</strong><span>Connector: {result.connector_id ?? selected ?? 'not returned'} · status: {result.status ?? 'not returned'} · attempts: {result.attempts ?? '—'}</span><span>Records: {result.records ?? '—'} · inserted: {result.inserted ?? '—'} · indexed: {result.indexed ?? '—'} · alert: {result.alert_state ?? 'not returned'}</span><span>{result.error ? `Error: ${result.error}` : result.reason ?? `Correlation: ${result.correlation_id ?? 'not returned'}`}</span></div>}
        </article>

        <article className="surface command-panel" data-automation-section="persisted-execution-observation">
          <header className="panel-heading"><div><p className="eyebrow">Persisted connector state</p><h2>Latest durable execution observation</h2></div><span className="evidence-label">DTMO persistence · read-only</span></header>
          {!selected && <p className="panel-state">Select a playbook to inspect its latest persisted connector observation.</p>}
          {selected && persisted.isPending && <p className="panel-state">Loading persisted execution observation…</p>}
          {selected && persisted.isError && <p className="panel-state error-state">Persisted execution observation unavailable. No successful, failed or healthy run state is inferred.</p>}
          {selected && !persisted.isPending && !persisted.isError && !selectedPersisted && <p className="panel-state">No persisted Source Center observation is available for this playbook. This does not prove that no execution has occurred.</p>}
          {selectedPersisted && <dl className="investigation-facts">
            <div><dt>Persisted health state</dt><dd>{selectedPersisted.health_status}</dd></div>
            <div><dt>Last success</dt><dd>{displayTime(selectedPersisted.last_success_at)}</dd></div>
            <div><dt>Last failure</dt><dd>{displayTime(selectedPersisted.last_failure_at)}</dd></div>
            <div><dt>Consecutive failures</dt><dd>{selectedPersisted.consecutive_failures}</dd></div>
            <div><dt>Isolation until</dt><dd>{displayTime(selectedPersisted.isolated_until)}</dd></div>
          </dl>}
          <p className="boundary-copy">This panel re-reads persisted Source Center connector state after execution and explicit refresh. It is durable latest-state evidence, not a complete immutable run history. It does not prove source truth, upstream availability, production readiness or remediation success.</p>
        </article>
      </div>

      <article className="surface evidence-surface"><div><p className="eyebrow">Evidence boundary</p><h2>Automation without autonomous decision authority</h2></div><p>A schedule or successful run proves only the recorded scheduler or connector action. The immediate execution result is browser-observed; the Source Center panel separately exposes the latest persisted connector state when available. Neither is a complete immutable run history. They do not prove source truth, compromise, containment, remediation, review completion, case creation, external-share or publication authority, production readiness or production authorization. Credentials and execution remain server-side and RBAC-governed.</p></article>
    </section>
  );
}
