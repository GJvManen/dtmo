import { useEffect, useMemo, useState } from 'react';

type Session = { permissions: string[] };
type Source = { id: string; name: string; enabled: boolean; authentication_mode: string; reliability: string };
type SourceCenterStatus = {
  id: string;
  name: string;
  execution_status: string;
  registered: boolean;
  enabled: boolean;
  manual_run_available: boolean;
  health_status: string;
  provenance: { configured_reliability: string };
};
type RunResult = { id: string; status: string; records: number; inserted: number; indexed: number; error: string | null; publication_gate: string };

type PopulationProps = {
  onPopulated: () => void;
  title?: string;
  reloadLabel?: string;
  enabledSourcesLabel?: string;
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

async function runRegisteredSource(sourceId: string): Promise<RunResult> {
  const response = await fetch(`/api/v1/admin/sources/${encodeURIComponent(sourceId)}/run`, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json', 'X-Request-ID': crypto.randomUUID() },
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === 'object' && body && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as RunResult;
}

async function runBuiltInSource(sourceId: string): Promise<RunResult> {
  const response = await fetch(`/connectors/${encodeURIComponent(sourceId)}/run`, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json', 'X-Request-ID': crypto.randomUUID() },
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === 'object' && body && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as RunResult;
}

export function ThreatIntelligencePopulation({
  onPopulated,
  title = 'Populate canonical intelligence',
  reloadLabel = 'Reload recent intelligence',
  enabledSourcesLabel = 'Available intelligence sources',
}: PopulationProps) {
  const [allowed, setAllowed] = useState(false);
  const [sources, setSources] = useState<Source[]>([]);
  const [sourceCenter, setSourceCenter] = useState<SourceCenterStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningId, setRunningId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const enabledSources = useMemo(() => sources.filter((source) => source.enabled), [sources]);
  const builtInSources = useMemo(
    () => sourceCenter.filter((source) => source.execution_status === 'supported-built-in' && source.manual_run_available),
    [sourceCenter],
  );
  const availableCount = enabledSources.length + builtInSources.length;

  useEffect(() => {
    let active = true;
    void readJson<Session>('/api/v1/ui/session').then(async (session) => {
      if (!active) return;
      const canManage = session.permissions.includes('manage:connectors');
      setAllowed(canManage);
      if (!canManage) return;
      const [registered, runtime] = await Promise.all([
        readJson<Source[]>('/api/v1/admin/sources'),
        readJson<SourceCenterStatus[]>('/api/v1/source-center/status'),
      ]);
      if (active) {
        setSources(registered);
        setSourceCenter(runtime);
      }
    }).catch((reason) => {
      if (active) setError(reason instanceof Error ? reason.message : 'Source readiness unavailable');
    }).finally(() => {
      if (active) setLoading(false);
    });
    return () => { active = false; };
  }, []);

  async function executeRegistered(source: Source) {
    if (!source.enabled) return;
    await execute(source.id, source.name, () => runRegisteredSource(source.id));
  }

  async function executeBuiltIn(source: SourceCenterStatus) {
    if (!source.manual_run_available) return;
    await execute(source.id, source.name, () => runBuiltInSource(source.id));
  }

  async function execute(sourceId: string, sourceName: string, runner: () => Promise<RunResult>) {
    setRunningId(sourceId); setMessage(null); setError(null);
    try {
      const result = await runner();
      if (result.status !== 'completed') {
        setError(result.error || `Source ${sourceName} did not complete`);
        return;
      }
      setMessage(`${sourceName}: ${result.records} received, ${result.inserted} inserted, ${result.indexed} indexed. Review and sharing remain separately governed.`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Source execution failed');
    } finally {
      setRunningId(null);
    }
  }

  if (loading) return <p className="panel-state">Checking governed population paths…</p>;

  return (
    <section className="detail-section" aria-labelledby="population-title">
      <h3 id="population-title">{title}</h3>
      <p>Only already-enabled governed sources can be executed here. Registered sources must already be enabled. Supported built-in sources are treated as governed executable sources only when the Source Center reports <code>manual_run_available</code>; they are not auto-enabled registry entries. {'Activation, endpoint changes and credentials stay in Sources & Collection'}.</p>
      {!allowed && <p className="panel-state">This principal cannot execute sources. Open <a href="/workbench/collection">Sources &amp; Collection</a> to inspect available operator actions.</p>}
      {allowed && availableCount === 0 && <p className="panel-state">No governed population path is currently available. Open <a href="/workbench/collection">Sources &amp; Collection</a> to inspect built-in readiness or validate, test and explicitly activate a supported registry source.</p>}
      {allowed && availableCount > 0 && <div className="quick-grid" aria-label={enabledSourcesLabel}>
        {builtInSources.map((source) => <button type="button" className="quick-action" key={`built-in-${source.id}`} disabled={runningId !== null} onClick={() => void executeBuiltIn(source)}>
          <span aria-hidden="true">↻</span><div><strong>{runningId === source.id ? `Loading ${source.name}…` : `Load ${source.name} now`}</strong><small>built-in · {source.health_status} · {source.provenance.configured_reliability} reliability</small></div>
        </button>)}
        {enabledSources.map((source) => <button type="button" className="quick-action" key={source.id} disabled={runningId !== null} onClick={() => void executeRegistered(source)}>
          <span aria-hidden="true">↻</span><div><strong>{runningId === source.id ? `Running ${source.name}…` : `Run ${source.name}`}</strong><small>{source.reliability} reliability · {source.authentication_mode}</small></div>
        </button>)}
      </div>}
      {message && <div className="panel-state"><strong>Canonical ingestion completed</strong><span>{message}</span><button type="button" onClick={onPopulated}>{reloadLabel}</button></div>}
      {error && <div className="panel-state error-state"><strong>Population failed closed</strong><span>{error}. No success, source-health or data-absence conclusion is inferred.</span></div>}
      <p className="boundary-copy">Running a source invokes an existing audited same-origin execution contract. A successful collection only records attributable canonical data; it does not prove exploitation, local compromise, review approval, publication or external sharing authority.</p>
    </section>
  );
}
