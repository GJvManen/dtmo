import { useEffect, useMemo, useState } from 'react';

type IocRecord = {
  record_id: string;
  item_id: string;
  item_title: string;
  source_id: string;
  severity: string;
  confidence_score: number;
  observable_type: string;
  observable_value: string;
  handling: string;
  status: string;
  analyzers: string[];
  created_at: string;
  external_share_authorized: boolean;
  local_compromise_proven: boolean;
};

type IocInventory = { records: IocRecord[]; evidence_boundary: string };

async function json<T>(url: string): Promise<T> {
  const response = await fetch(url, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
  let body: unknown = null;
  try { body = await response.json(); } catch { body = null; }
  if (!response.ok) {
    const detail = typeof body === 'object' && body !== null && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

function displayDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function analysisHref(record: IocRecord) {
  const params = new URLSearchParams({ item: record.item_id, observable_type: record.observable_type, observable_value: record.observable_value });
  return `/workbench/analysis?${params.toString()}`;
}

function intelligenceHref(record: IocRecord) {
  return `/workbench/intelligence?item=${encodeURIComponent(record.item_id)}`;
}

export function IocExplorerWorkspace() {
  const [inventory, setInventory] = useState<IocInventory | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [observableType, setObservableType] = useState('');
  const [severity, setSeverity] = useState('');
  const [source, setSource] = useState('');
  const [minimumConfidence, setMinimumConfidence] = useState(0);

  useEffect(() => {
    let active = true;
    void json<IocInventory>('/api/v1/iocs?size=500').then((data) => {
      if (active) setInventory(data);
    }).catch((reason) => {
      if (active) setError(reason instanceof Error ? reason.message : 'IOC inventory unavailable');
    }).finally(() => {
      if (active) setLoading(false);
    });
    return () => { active = false; };
  }, []);

  const types = useMemo(() => [...new Set((inventory?.records ?? []).map((record) => record.observable_type))].sort(), [inventory]);
  const sources = useMemo(() => [...new Set((inventory?.records ?? []).map((record) => record.source_id))].sort(), [inventory]);
  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return (inventory?.records ?? []).filter((record) => {
      if (observableType && record.observable_type !== observableType) return false;
      if (severity && record.severity.toLowerCase() !== severity) return false;
      if (source && record.source_id !== source) return false;
      if (record.confidence_score < minimumConfidence) return false;
      if (needle && !`${record.observable_value} ${record.item_title} ${record.source_id}`.toLowerCase().includes(needle)) return false;
      return true;
    });
  }, [inventory, minimumConfidence, observableType, query, severity, source]);

  return (
    <section className="unified-intelligence" aria-labelledby="workspace-title">
      <header className="workspace-heading intelligence-heading">
        <div><p className="eyebrow">Unified Operations Workbench</p><h1 id="workspace-title">IOC Explorer</h1><p>Persisted observables from governed enrichment runs, tied to canonical DTMO intelligence.</p></div>
        <div className="heading-statuses"><span className="phase-badge">11.10q Functional recovery</span><span className="phase-badge available">Canonical IOC inventory</span></div>
      </header>

      <article className="surface intelligence-search-surface">
        <div className="panel-heading"><div><p className="eyebrow">Inventory filters</p><h2>Filter persisted indicators</h2></div><span className="evidence-label">No text-derived or synthetic IOCs</span></div>
        <div className="intelligence-search-form">
          <label className="search-query-field"><span>Indicator or context</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="IP, domain, hash, item title or source…" /></label>
          <label><span>Type</span><select value={observableType} onChange={(event) => setObservableType(event.target.value)}><option value="">All types</option>{types.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
          <label><span>Severity</span><select value={severity} onChange={(event) => setSeverity(event.target.value)}><option value="">All severities</option>{['critical', 'high', 'medium', 'low', 'informational'].map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
          <label><span>Source</span><select value={source} onChange={(event) => setSource(event.target.value)}><option value="">All sources</option>{sources.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
          <label><span>Minimum confidence</span><input type="number" min={0} max={100} value={minimumConfidence} onChange={(event) => setMinimumConfidence(Number(event.target.value))} /></label>
        </div>
        <p className="boundary-copy">This inventory is read-only. Indicator presence is enrichment evidence, not a maliciousness verdict, proof of local compromise, or external-share authorization.</p>
      </article>

      <article className="surface intelligence-results-panel">
        <header className="panel-heading"><div><p className="eyebrow">Canonical observable inventory</p><h2>Indicators</h2></div><span className="evidence-label">{loading ? 'Loading…' : `${filtered.length} shown`}</span></header>
        {loading && <p className="panel-state">Loading persisted IOC inventory…</p>}
        {error && <div className="panel-state error-state"><strong>IOC inventory unavailable</strong><span>{error}. No zero-indicator or platform-health conclusion is inferred.</span></div>}
        {!loading && !error && !(inventory?.records.length) && <div className="intelligence-empty"><strong>No governed observables recorded yet</strong><span>Run an analyst-authorized enrichment from Analysis &amp; Enrichment. Only persisted observables become IOC inventory records.</span></div>}
        {!loading && !error && Boolean(inventory?.records.length) && filtered.length === 0 && <div className="intelligence-empty"><strong>No indicators match these filters</strong><span>Clear or broaden filters; this does not prove indicator absence upstream.</span></div>}
        {!loading && !error && filtered.length > 0 && <div className="intelligence-result-list" aria-label="IOC inventory">{filtered.map((record) => (
          <article className="intelligence-result" key={record.record_id}>
            <span className={`severity-dot severity-${record.severity.toLowerCase()}`} aria-hidden="true" />
            <span className="result-copy"><strong>{record.observable_value}</strong><small>{record.observable_type} · {record.source_id} · confidence {record.confidence_score}/100 · {record.handling}</small><span>{record.item_title}</span></span>
            <span className="result-meta"><b>{record.severity.toLowerCase()}</b><small>{displayDate(record.created_at)}</small></span>
            <span className="heading-statuses">
              <a className="button secondary" href={intelligenceHref(record)}>Open source intelligence</a>
              <a className="button secondary" href={analysisHref(record)}>Enrich / analyze selected IOC</a>
              <a className="button secondary" href={`/workbench/intelligence/graph?item=${encodeURIComponent(record.item_id)}`}>Graph</a>
              <a className="button secondary" href={`/workbench/investigations?item=${encodeURIComponent(record.item_id)}`}>Investigate</a>
            </span>
          </article>
        ))}</div>}
      </article>

      <article className="surface evidence-surface intelligence-evidence"><div><p className="eyebrow">Evidence boundary</p><h2>IOC inventory without inferred verdicts</h2></div><p>{inventory?.evidence_boundary ?? 'IOC records are exposed only from persisted governed enrichment evidence. Missing records remain visibly missing.'}</p></article>
    </section>
  );
}
