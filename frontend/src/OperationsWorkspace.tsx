import { useQuery } from '@tanstack/react-query';
import { NavLink } from 'react-router-dom';

type HealthSnapshot = {
  status: string;
  version: string;
  environment: string;
  scheduler?: { running?: boolean };
};

type OperationsSummary = {
  metric_source: string;
  request_count: number;
  average_latency_ms: number;
  active_alerts: number;
  trace_context_total: number;
  in_flight: number;
  queue_backlog_ratio: number;
  connector_runs_total: number;
  alerts: {
    api_error: boolean;
    connector: boolean;
    storage_integrity: boolean;
    search_health: boolean;
  };
};

type ConnectorCapability = {
  id: string;
  enabled: boolean;
};

type ConnectorRuntimeState = {
  connector_id: string;
  health_status: string;
  last_run_id: string | null;
  last_success_at: string | null;
  last_failure_at: string | null;
  consecutive_failures: number;
  circuit_open_until: string | null;
  updated_at: string | null;
};

type ConnectorRunEvidence = {
  connector_id: string;
  run_id: string;
  observed_at: string | null;
  status: string;
  duration_seconds: number;
  record_count: number;
  quarantine_count: number;
  error_code: string | null;
  publish_approved: boolean;
};

type RuntimeEvidence = {
  evidence_source: string;
  state_table: string;
  history_table: string;
  connector_states: ConnectorRuntimeState[];
  recent_runs: ConnectorRunEvidence[];
  claim_boundary: string;
};

async function readJson<T>(url: string): Promise<T> {
  const response = await fetch(url, {
    credentials: 'same-origin',
    headers: { Accept: 'application/json' },
  });
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof payload === 'object' && payload && 'detail' in payload
      ? String((payload as { detail: unknown }).detail)
      : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return payload as T;
}

function finite(value: number | undefined, suffix = '') {
  return typeof value === 'number' && Number.isFinite(value) ? `${value.toLocaleString()}${suffix}` : '—';
}

function timestamp(value: string | null | undefined) {
  if (!value) return 'not observed';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

export function OperationsWorkspace() {
  const health = useQuery({
    queryKey: ['operations', 'health'],
    queryFn: () => readJson<HealthSnapshot>('/health'),
    retry: false,
    refetchInterval: 30_000,
  });
  const summary = useQuery({
    queryKey: ['operations', 'summary'],
    queryFn: () => readJson<OperationsSummary>('/api/v1/operations/summary'),
    retry: false,
    refetchInterval: 30_000,
  });
  const connectors = useQuery({
    queryKey: ['operations', 'connectors'],
    queryFn: () => readJson<ConnectorCapability[]>('/connectors'),
    retry: false,
    refetchInterval: 30_000,
  });
  const runtimeEvidence = useQuery({
    queryKey: ['operations', 'runtime-evidence'],
    queryFn: () => readJson<RuntimeEvidence>('/api/v1/operations/runtime-evidence'),
    retry: false,
    refetchInterval: 30_000,
  });

  const refresh = () => {
    void health.refetch();
    void summary.refetch();
    void connectors.refetch();
    void runtimeEvidence.refetch();
  };
  const data = summary.data;
  const healthObserved = !health.isError && Boolean(health.data);
  const summaryObserved = !summary.isError && Boolean(data);
  const connectorRows = connectors.data ?? [];
  const enabledConnectors = connectorRows.filter((connector) => connector.enabled).length;
  const stateRows = runtimeEvidence.data?.connector_states ?? [];
  const recentRuns = runtimeEvidence.data?.recent_runs ?? [];
  const alertRows = data ? [
    ['API errors', data.alerts.api_error],
    ['Connector failures', data.alerts.connector],
    ['Storage integrity', data.alerts.storage_integrity],
    ['Search health', data.alerts.search_health],
  ] as const : [];

  return (
    <section className="workspace-foundation" aria-labelledby="workspace-title">
      <header className="workspace-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Operations</h1>
          <p>Canonical runtime health, telemetry, persisted connector execution evidence and alert observation from same-origin DTMO contracts.</p>
        </div>
        <div className="heading-statuses">
          <span className="phase-badge">11.10m Operations · 11.10q recovery</span>
          <span className="evidence-label">Runtime observation ≠ production assurance</span>
        </div>
      </header>

      <article className="surface command-panel">
        <header className="panel-heading">
          <div><p className="eyebrow">Observation controls</p><h2>Operational snapshot</h2></div>
          <button type="button" onClick={refresh} disabled={health.isFetching || summary.isFetching || connectors.isFetching || runtimeEvidence.isFetching}>Refresh runtime observation</button>
        </header>
        <p className="boundary-copy">Values below are read-only observations from this DTMO process and its persisted connector state. Missing telemetry stays unavailable; it is never converted into a healthy or zero-risk claim.</p>
      </article>

      <section className="kpi-grid" aria-label="Runtime KPIs">
        <article className="kpi-card tone-neutral"><p>API</p><strong>{healthObserved ? health.data?.status : '—'}</strong><span>{healthObserved ? `v${health.data?.version ?? 'unknown'}` : 'Health unavailable'}</span></article>
        <article className="kpi-card tone-accent"><p>Requests</p><strong>{summaryObserved ? finite(data?.request_count) : '—'}</strong><span>Observed process total</span></article>
        <article className="kpi-card tone-neutral"><p>Average latency</p><strong>{summaryObserved && typeof data?.average_latency_ms === 'number' ? `${data.average_latency_ms.toFixed(1)} ms` : '—'}</strong><span>Observed HTTP requests</span></article>
        <article className={`kpi-card ${data?.active_alerts ? 'tone-critical' : 'tone-neutral'}`}><p>Active alerts</p><strong>{summaryObserved ? finite(data?.active_alerts) : '—'}</strong><span>Operational alert gauges</span></article>
      </section>

      <div className="command-grid">
        <article className="surface command-panel">
          <header className="panel-heading"><div><p className="eyebrow">Runtime</p><h2>Platform health</h2></div><span className={`status-chip ${health.data?.status === 'healthy' ? 'success' : health.isError ? 'error' : 'neutral'}`}>{health.isPending ? 'loading' : health.isError ? 'unavailable' : health.data?.status ?? 'unknown'}</span></header>
          {health.isError && <p className="panel-state error-state">Health observation unavailable: {health.error.message}</p>}
          {healthObserved && <div className="integration-list">
            <div className="integration-row"><div><strong>Environment</strong><span>{health.data?.environment ?? 'unknown'}</span></div></div>
            <div className="integration-row"><div><strong>Scheduler</strong><span>{health.data?.scheduler?.running ? 'running' : 'idle / not reported running'}</span></div></div>
            <div className="integration-row"><div><strong>Trace contexts</strong><span>{summaryObserved ? finite(data?.trace_context_total) : 'unavailable'}</span></div></div>
          </div>}
        </article>

        <article className="surface command-panel">
          <header className="panel-heading"><div><p className="eyebrow">Signals</p><h2>Alert state</h2></div><span className="evidence-label">{data?.metric_source ?? 'Prometheus registry'}</span></header>
          {summary.isError && <p className="panel-state error-state">Operational metrics unavailable: {summary.error.message}</p>}
          {summary.isPending && <p className="panel-state">Loading alert gauges…</p>}
          {summaryObserved && <div className="integration-list">{alertRows.map(([label, active]) => <div className="integration-row" key={label}><span className={`integration-state ${active ? 'state-configuration-required' : 'state-ready'}`} aria-hidden="true" /><div><strong>{label}</strong><span>{active ? 'active' : 'clear at observation time'}</span></div></div>)}</div>}
          <p className="boundary-copy">A clear gauge is only a point-in-time observation; it does not prove absence of incidents or vulnerabilities.</p>
        </article>

        <article className="surface command-panel">
          <header className="panel-heading"><div><p className="eyebrow">Telemetry</p><h2>Process workload</h2></div><NavLink className="text-link" to="/command-center">Command Center →</NavLink></header>
          {summaryObserved ? <div className="integration-list">
            <div className="integration-row"><div><strong>In flight</strong><span>{finite(data?.in_flight)}</span></div></div>
            <div className="integration-row"><div><strong>Queue backlog</strong><span>{typeof data?.queue_backlog_ratio === 'number' ? `${Math.round(data.queue_backlog_ratio * 100)}%` : '—'}</span></div></div>
            <div className="integration-row"><div><strong>Connector runs</strong><span>{finite(data?.connector_runs_total)}</span></div></div>
          </div> : <p className="panel-state">No attributable operational summary is currently available.</p>}
        </article>

        <article className="surface command-panel">
          <header className="panel-heading"><div><p className="eyebrow">Connectors</p><h2>{connectors.isError ? 'Capability unavailable' : `${enabledConnectors}/${connectorRows.length} enabled`}</h2></div><NavLink className="text-link" to="/collection">Manage collection →</NavLink></header>
          {connectors.isError && <p className="panel-state error-state">Connector capability unavailable: {connectors.error.message}</p>}
          {connectors.isPending && <p className="panel-state">Loading connector capability…</p>}
          {!connectors.isError && !connectors.isPending && !connectorRows.length && <p className="panel-state">No connector capability rows are currently exposed.</p>}
          {connectorRows.length > 0 && <div className="integration-list">{connectorRows.map((connector) => <div className="integration-row" key={connector.id}><span className={`integration-state ${connector.enabled ? 'state-ready' : 'state-disabled'}`} aria-hidden="true" /><div><strong>{connector.id}</strong><span>{connector.enabled ? 'enabled' : 'disabled'}</span></div><NavLink className="integration-pivot" to="/collection">Inspect</NavLink></div>)}</div>}
          <p className="boundary-copy">Connector enablement is capability state, not proof of successful collection or upstream health.</p>
        </article>
      </div>

      <article className="surface command-panel" data-operations-section="connector-runtime-evidence">
        <header className="panel-heading">
          <div><p className="eyebrow">Persisted execution evidence</p><h2>Connector runtime state</h2></div>
          <span className="evidence-label">{runtimeEvidence.data?.evidence_source ?? 'runtime evidence unavailable'}</span>
        </header>
        {runtimeEvidence.isError && <p className="panel-state error-state">Persisted connector runtime evidence unavailable: {runtimeEvidence.error.message}</p>}
        {runtimeEvidence.isPending && <p className="panel-state">Loading persisted connector runtime evidence…</p>}
        {!runtimeEvidence.isError && !runtimeEvidence.isPending && stateRows.length === 0 && <p className="panel-state">No connector runtime state has been persisted yet. This is not interpreted as healthy.</p>}
        {stateRows.length > 0 && <div className="integration-list">{stateRows.map((state) => <div className="integration-row" key={state.connector_id} data-connector-runtime={state.connector_id}>
          <span className={`integration-state ${state.health_status === 'healthy' ? 'state-ready' : state.health_status === 'unknown' ? 'state-disabled' : 'state-configuration-required'}`} aria-hidden="true" />
          <div>
            <strong>{state.connector_id} · {state.health_status}</strong>
            <span>last success {timestamp(state.last_success_at)} · last failure {timestamp(state.last_failure_at)} · consecutive failures {state.consecutive_failures}</span>
            <small>last run {state.last_run_id ?? 'not observed'} · state updated {timestamp(state.updated_at)}{state.circuit_open_until ? ` · isolated until ${timestamp(state.circuit_open_until)}` : ''}</small>
          </div>
        </div>)}</div>}
        <p className="boundary-copy">Source: {runtimeEvidence.data?.state_table ?? 'connector_runtime_states'} + {runtimeEvidence.data?.history_table ?? 'connector_health_events'}. {runtimeEvidence.data?.claim_boundary ?? 'Persisted runtime evidence does not establish live upstream availability or production assurance.'}</p>
      </article>

      <article className="surface command-panel" data-operations-section="recent-connector-runs">
        <header className="panel-heading"><div><p className="eyebrow">Durable history</p><h2>Recent connector runs</h2></div><span className="evidence-label">Latest 25 persisted observations</span></header>
        {recentRuns.length === 0 && !runtimeEvidence.isPending && <p className="panel-state">No persisted connector run history is currently available.</p>}
        {recentRuns.length > 0 && <div className="integration-list">{recentRuns.map((run) => <div className="integration-row" key={`${run.connector_id}-${run.run_id}`}>
          <span className={`integration-state ${run.status === 'success' ? 'state-ready' : 'state-configuration-required'}`} aria-hidden="true" />
          <div>
            <strong>{run.connector_id} · {run.status}</strong>
            <span>{timestamp(run.observed_at)} · {run.record_count} records · {run.quarantine_count} quarantined · {run.duration_seconds.toFixed(2)}s</span>
            <small>run {run.run_id}{run.error_code ? ` · error ${run.error_code}` : ''} · publication approved: {run.publish_approved ? 'yes' : 'no'}</small>
          </div>
        </div>)}</div>}
      </article>

      <article className="surface evidence-surface">
        <div><p className="eyebrow">Canonical pivots</p><h2>Act without legacy fallback</h2></div>
        <div className="quick-grid">
          <NavLink className="quick-action" to="/collection"><span aria-hidden="true">↓</span><div><strong>Sources & Collection</strong><small>Validate, test and explicitly run governed sources.</small></div></NavLink>
          <NavLink className="quick-action" to="/administration"><span aria-hidden="true">⚙</span><div><strong>Administration</strong><small>Inspect integration configuration and readiness.</small></div></NavLink>
          <NavLink className="quick-action" to="/automation"><span aria-hidden="true">↯</span><div><strong>Automation</strong><small>Observe governed execution and scheduler state.</small></div></NavLink>
        </div>
        <p className="boundary-copy">Operations is read-only. Connector execution, configuration, review, sharing and case mutation remain separate server-authorized actions in their canonical workspaces.</p>
      </article>
    </section>
  );
}
