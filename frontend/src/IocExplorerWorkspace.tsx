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
type AilCorrelation = {
  source_id: string;
  external_id: string;
  item_type: string;
  title: string;
  relation: string;
  matched_value: string;
  context: Record<string, unknown>;
};
type AilCorrelationResponse = {
  status: string;
  indicator: { type: string; value: string };
  investigation_references: Array<{ id: string }>;
  raw_content_exposed: boolean;
  analysis_only: boolean;
  degraded_reasons: string[];
  claim_boundary: string;
  correlations: AilCorrelation[];
};

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
  const [ailTarget, setAilTarget] = useState<IocRecord | null>(null);
  const [ailCorrelation, setAilCorrelation] = useState<AilCorrelationResponse | null>(null);
  const [ailLoading, setAilLoading] = useState(false);
  const [ailError, setAilError] = useState<string | null>(null);

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

  async function inspectAil(record: IocRecord) {
    setAilTarget(record);
    setAilCorrelation(null);
    setAilError(null);
    setAilLoading(true);
    try {
      const result = await json<AilCorrelationResponse>(`/api/v1/intelligence/${encodeURIComponent(record.item_id)}/ail-correlations`);
      setAilCorrelation(result);
    } catch (reason) {
      setAilError(reason instanceof Error ? reason.message : 'AIL correlation unavailable');
    } finally {
      setAilLoading(false);
    }
  }

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
              <button className="button secondary" type="button" onClick={() => void inspectAil(record)}>Inspect AIL correlation</button>
              <a className="button secondary" href={analysisHref(record)}>Enrich / analyze selected IOC</a>
              <a className="button secondary" href={`/workbench/intelligence/graph?item=${encodeURIComponent(record.item_id)}`}>Graph</a>
              <a className="button secondary" href={`/workbench/investigations?item=${encodeURIComponent(record.item_id)}`}>Investigate</a>
            </span>
          </article>
        ))}</div>}
      </article>

      {ailTarget && <article className="surface intelligence-detail-panel" aria-label="AIL correlation context">
        <header className="panel-heading"><div><p className="eyebrow">AIL · read-only correlation</p><h2>Correlation context for {ailTarget.observable_value}</h2></div><span className="evidence-label">Same-origin DTMO API</span></header>
        {ailLoading && <p className="panel-state">Loading bounded AIL correlation…</p>}
        {ailError && <div className="panel-state error-state"><strong>AIL correlation unavailable</strong><span>{ailError}. No zero-correlation, source-health or local-compromise conclusion is inferred.</span></div>}
        {ailCorrelation && <>
          <dl className="intelligence-facts"><div><dt>Status</dt><dd>{ailCorrelation.status}</dd></div><div><dt>Indicator</dt><dd>{ailCorrelation.indicator.type}: {ailCorrelation.indicator.value}</dd></div><div><dt>Correlations</dt><dd>{ailCorrelation.correlations.length}</dd></div><div><dt>Investigation references</dt><dd>{ailCorrelation.investigation_references.length}</dd></div><div><dt>Raw content exposed</dt><dd>{ailCorrelation.raw_content_exposed ? 'yes' : 'no'}</dd></div><div><dt>Analysis only</dt><dd>{ailCorrelation.analysis_only ? 'yes' : 'no'}</dd></div></dl>
          {ailCorrelation.degraded_reasons.length > 0 && <div className="panel-state"><strong>Degraded correlation context</strong><span>{ailCorrelation.degraded_reasons.join(' · ')}</span></div>}
          {!ailCorrelation.correlations.length && <div className="intelligence-empty"><strong>No bounded AIL correlations recorded</strong><span>This does not prove absence in AIL or any upstream source.</span></div>}
          {ailCorrelation.correlations.length > 0 && <div className="provenance-list">{ailCorrelation.correlations.map((correlation, index) => <div className="provenance-row" key={`${correlation.source_id}-${correlation.external_id}-${index}`}><span><strong>{correlation.title}</strong><small>{correlation.source_id} · {correlation.item_type} · {correlation.relation}</small></span><span><b>{correlation.matched_value}</b><small>Attributable correlation context</small></span></div>)}</div>}
          {ailCorrelation.investigation_references.length > 0 && <p className="boundary-copy">AIL investigation references: {ailCorrelation.investigation_references.map((reference) => reference.id).join(', ')}. These identifiers are context only and do not import AIL case ownership or authority into DTMO.</p>}
          <p className="boundary-copy"><strong>Claim boundary:</strong> {ailCorrelation.claim_boundary}</p>
        </>}
        <p className="boundary-copy">This surface is read-only. It never exposes the AIL API key, raw AIL bodies, review/share/case/publication authority, or proof of live-source completeness or local compromise.</p>
      </article>}

      <article className="surface evidence-surface intelligence-evidence"><div><p className="eyebrow">Evidence boundary</p><h2>IOC inventory without inferred verdicts</h2></div><p>{inventory?.evidence_boundary ?? 'IOC records are exposed only from persisted governed enrichment evidence. Missing records remain visibly missing.'}</p></article>
    </section>
  );
}
