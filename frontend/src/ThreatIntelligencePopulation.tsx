import { useEffect, useMemo, useState } from 'react';

type Session = { permissions: string[] };
type Source = { id: string; name: string; enabled: boolean; authentication_mode: string; reliability: string };
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

async function runSource(sourceId: string): Promise<RunResult> {
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

export function ThreatIntelligencePopulation({
  onPopulated,
  title = 'Populate canonical intelligence',
  reloadLabel = 'Reload recent intelligence',
  enabledSourcesLabel = 'Enabled intelligence sources',
}: PopulationProps) {
  const [allowed, setAllowed] = useState(false);
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningId, setRunningId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const enabledSources = useMemo(() => sources.filter((source) => source.enabled), [sources]);

  useEffect(() => {
    let active = true;
    void readJson<Session>('/api/v1/ui/session').then(async (session) => {
      if (!active) return;
      const canManage = session.permissions.includes('manage:connectors');
      setAllowed(canManage);
      if (!canManage) return;
      const registered = await readJson<Source[]>('/api/v1/admin/sources');
      if (active) setSources(registered);
    }).catch((reason) => {
      if (active) setError(reason instanceof Error ? reason.message : 'Source readiness unavailable');
    }).finally(() => {
      if (active) setLoading(false);
    });
    return () => { active = false; };
  }, []);

  async function execute(source: Source) {
    if (!source.enabled) return;
    setRunningId(source.id); setMessage(null); setError(null);
    try {
      const result = await runSource(source.id);
      if (result.status !== 'completed') {
        setError(result.error || `Source ${source.name} did not complete`);
        return;
      }
      setMessage(`${source.name}: ${result.records} received, ${result.inserted} inserted, ${result.indexed} indexed. Review and sharing remain separately governed.`);
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
      <p>{'Only already-enabled governed sources can be executed here. Activation, endpoint changes and credentials stay in Sources & Collection and remain server-authorized.'}</p>
      {!allowed && <p className="panel-state">This principal cannot execute sources. Open <a href="/workbench/collection">Sources &amp; Collection</a> to inspect available operator actions.</p>}
      {allowed && enabledSources.length === 0 && <p className="panel-state">No governed source is currently enabled. Open <a href="/workbench/collection">Sources &amp; Collection</a> to validate, test and explicitly activate a supported source.</p>}
      {allowed && enabledSources.length > 0 && <div className="quick-grid" aria-label={enabledSourcesLabel}>
        {enabledSources.map((source) => <button type="button" className="quick-action" key={source.id} disabled={runningId !== null} onClick={() => void execute(source)}>
          <span aria-hidden="true">↻</span><div><strong>{runningId === source.id ? `Running ${source.name}…` : `Run ${source.name}`}</strong><small>{source.reliability} reliability · {source.authentication_mode}</small></div>
        </button>)}
      </div>}
      {message && <div className="panel-state"><strong>Canonical ingestion completed</strong><span>{message}</span><button type="button" onClick={onPopulated}>{reloadLabel}</button></div>}
      {error && <div className="panel-state error-state"><strong>Population failed closed</strong><span>{error}. No success, source-health or data-absence conclusion is inferred.</span></div>}
      <p className="boundary-copy">Running an enabled source invokes the existing audited same-origin source execution contract. It does not approve intelligence for review, publication or external sharing.</p>
    </section>
  );
}
