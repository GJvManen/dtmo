import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';

import { IocExplorerWorkspace } from './IocExplorerWorkspace';
import { ThreatIntelligencePopulation } from './ThreatIntelligencePopulation';

type IntelligenceSearchResult = {
  id: string;
  title: string;
  summary?: string;
  item_type?: string;
  source_id?: string;
  severity?: string;
  confidence_score?: number;
  confidence_level?: string;
  education_relevance?: number;
  published_at?: string | null;
  canonical_url?: string;
  tags?: string[];
};

type IntelligenceSearchResponse = { query: string; count: number; results: IntelligenceSearchResult[] };
type RecentIntelligence = { id: string; title: string; source_id: string; severity: string; education_relevance: number; review_status: string; discovered_at: string };
type CommandCenterSnapshot = { data_state: 'available' | 'unavailable'; recent_intelligence: RecentIntelligence[] };
type IntelligenceProvenance = { source_url: string; source_title: string | null; publisher: string | null; retrieved_at: string; source_reliability: string | null; is_primary_source: boolean; content_integrity_verified: boolean; confidence_score: number };
type IntelligenceContext = { cve_ids: string[]; known_exploited: boolean; vendor: string | null; product: string | null };
type IntelligenceWorkspaceDetail = {
  id: string; source_id: string; external_id: string | null; item_type: string; title: string; summary: string; canonical_url: string;
  published_at: string | null; discovered_at: string; severity: string; confidence_score: number; confidence_level: string;
  confidence_rationale: string; education_relevance: number; review_status: string; share_approved: boolean; tags: string[];
  context: IntelligenceContext; provenance: IntelligenceProvenance[];
};
type Mode = 'intelligence' | 'ioc';

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
  let body: unknown = null;
  try { body = await response.json(); } catch { body = null; }
  if (!response.ok) {
    const detail = typeof body === 'object' && body !== null && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

function displaySeverity(value?: string) { return value ? value.toLowerCase() : 'informational'; }
function displayDate(value?: string | null) {
  if (!value) return 'Not recorded';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

export function UnifiedIntelligenceWorkspace({ mode = 'intelligence' }: { mode?: Mode }) {
  const [initialItem] = useState(() => new URLSearchParams(window.location.search).get('item') ?? '');
  const [query, setQuery] = useState('');
  const [severity, setSeverity] = useState('');
  const [minimumRelevance, setMinimumRelevance] = useState(0);
  const [size, setSize] = useState(50);
  const [results, setResults] = useState<IntelligenceSearchResult[]>([]);
  const [discoveryMode, setDiscoveryMode] = useState<'loading' | 'recent' | 'search' | 'empty' | 'error'>(mode === 'intelligence' ? 'loading' : 'empty');
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(initialItem || null);
  const [detail, setDetail] = useState<IntelligenceWorkspaceDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<string | null>(null);
  const [populationRefresh, setPopulationRefresh] = useState(0);
  const isIoc = mode === 'ioc';

  useEffect(() => {
    if (isIoc) return;
    let active = true;
    setDiscoveryMode('loading');
    setSearchError(null);
    void getJson<CommandCenterSnapshot>('/api/v1/command-center').then((snapshot) => {
      if (!active) return;
      if (snapshot.data_state !== 'available') {
        setResults([]); setDiscoveryMode('error'); setSearchError('Canonical DTMO persistence is unavailable'); return;
      }
      setResults(snapshot.recent_intelligence.map((item) => ({ ...item, published_at: item.discovered_at })));
      setDiscoveryMode(snapshot.recent_intelligence.length ? 'recent' : 'empty');
    }).catch((error) => {
      if (!active) return;
      setResults([]); setDiscoveryMode('error'); setSearchError(error instanceof Error ? error.message : 'Canonical intelligence unavailable');
    });
    return () => { active = false; };
  }, [isIoc, populationRefresh]);

  useEffect(() => {
    if (isIoc || !initialItem) return;
    let active = true;
    setDetail(null); setDetailError(null); setDetailLoading(true);
    void getJson<IntelligenceWorkspaceDetail>(`/api/v1/intelligence/${encodeURIComponent(initialItem)}/workspace`).then((item) => {
      if (!active) return;
      setSelectedId(item.id); setDetail(item);
    }).catch((error) => {
      if (!active) return;
      setDetailError(error instanceof Error ? error.message : 'Canonical intelligence detail unavailable');
    }).finally(() => {
      if (active) setDetailLoading(false);
    });
    return () => { active = false; };
  }, [initialItem, isIoc]);

  async function runSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const normalizedQuery = query.trim();
    if (normalizedQuery.length < 2) return;
    setSearching(true); setSearchError(null); setDiscoveryMode('search'); setSelectedId(null); setDetail(null); setDetailError(null);
    const params = new URLSearchParams({ q: normalizedQuery, minimum_relevance: String(minimumRelevance), size: String(size) });
    if (severity) params.set('severity', severity);
    try {
      const response = await getJson<IntelligenceSearchResponse>(`/api/v1/intelligence/search?${params.toString()}`);
      setResults(response.results);
    } catch (error) {
      setResults([]); setDiscoveryMode('error'); setSearchError(error instanceof Error ? error.message : 'Search backend unavailable');
    } finally { setSearching(false); }
  }

  async function selectResult(result: IntelligenceSearchResult) {
    setSelectedId(result.id); setDetail(null); setDetailError(null); setDetailLoading(true);
    try {
      const item = await getJson<IntelligenceWorkspaceDetail>(`/api/v1/intelligence/${encodeURIComponent(result.id)}/workspace`);
      setDetail(item);
      const params = new URLSearchParams({ item: item.id });
      window.history.replaceState(null, '', `/workbench/intelligence?${params.toString()}`);
    }
    catch (error) { setDetailError(error instanceof Error ? error.message : 'Canonical intelligence detail unavailable'); }
    finally { setDetailLoading(false); }
  }

  if (isIoc) return <IocExplorerWorkspace />;

  return (
    <section className="unified-intelligence" aria-labelledby="workspace-title">
      <header className="workspace-heading intelligence-heading">
        <div><p className="eyebrow">Unified Operations Workbench</p><h1 id="workspace-title">Threat Intelligence</h1><p>Recent canonical intelligence, search, triage and attributable investigation in one workspace.</p></div>
        <div className="heading-statuses"><span className="phase-badge">11.10q Functional recovery</span><span className="phase-badge available">Read-only investigation</span></div>
      </header>

      <article className="surface intelligence-search-surface">
        <div className="panel-heading"><div><p className="eyebrow">Governed discovery</p><h2>Search canonical intelligence</h2></div><span className="evidence-label">Canonical data · no synthetic results</span></div>
        <form className="intelligence-search-form" onSubmit={runSearch}>
          <label className="search-query-field"><span>Search canonical intelligence</span><input value={query} onChange={(event) => setQuery(event.target.value)} minLength={2} maxLength={300} required placeholder="Threat, campaign, actor, CVE, technology…" autoComplete="off" /></label>
          <label><span>Severity</span><select value={severity} onChange={(event) => setSeverity(event.target.value)}><option value="">All severities</option><option value="critical">Critical</option><option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option><option value="informational">Informational</option></select></label>
          <label><span>Minimum education relevance</span><input type="number" min={0} max={100} value={minimumRelevance} onChange={(event) => setMinimumRelevance(Number(event.target.value))} /></label>
          <label><span>Maximum results</span><input type="number" min={1} max={200} value={size} onChange={(event) => setSize(Number(event.target.value))} /></label>
          <button className="button primary intelligence-search-button" type="submit" disabled={searching || query.trim().length < 2}>{searching ? 'Searching…' : 'Search intelligence'}</button>
        </form>
        <p className="boundary-copy">Recent intelligence is read from canonical DTMO persistence. Search uses the governed search projection. Neither path grants review, publication, sharing, connector-execution or case-mutation authority.</p>
      </article>

      <div className="intelligence-workspace-grid">
        <article className="surface intelligence-results-panel">
          <header className="panel-heading"><div><p className="eyebrow">Discovery</p><h2>{discoveryMode === 'recent' ? 'Recent canonical intelligence' : 'Intelligence results'}</h2></div><span className="evidence-label">{discoveryMode === 'loading' ? 'Loading…' : `${results.length} available`}</span></header>
          {discoveryMode === 'loading' && <p className="panel-state">Loading recent canonical intelligence…</p>}
          {discoveryMode === 'empty' && <>
            <div className="intelligence-empty"><strong>No canonical intelligence recorded yet</strong><span>Use an already-enabled governed source below, or open Sources &amp; Collection to validate, test and activate one explicitly.</span></div>
            <ThreatIntelligencePopulation onPopulated={() => setPopulationRefresh((current) => current + 1)} />
          </>}
          {searching && <p className="panel-state">Searching the governed intelligence index…</p>}
          {searchError && <div className="panel-state error-state"><strong>Intelligence discovery unavailable</strong><span>{searchError}. No empty-result or platform-health conclusion is inferred.</span></div>}
          {!searching && !searchError && discoveryMode === 'search' && results.length === 0 && <div className="intelligence-empty"><strong>No intelligence matched this query</strong><span>This describes the queried DTMO search index only; it does not prove absence from upstream sources.</span></div>}
          {!searching && !searchError && results.length > 0 && <div className="intelligence-result-list" aria-label="Intelligence results">{results.map((result) => (
            <button type="button" key={result.id} aria-label={`Open ${result.title}`} aria-pressed={selectedId === result.id} className={`intelligence-result ${selectedId === result.id ? 'selected' : ''}`} onClick={() => void selectResult(result)}>
              <span className={`severity-dot severity-${displaySeverity(result.severity)}`} aria-hidden="true" /><span className="result-copy"><strong>{result.title}</strong><small>{result.source_id ?? 'source unavailable'} · relevance {result.education_relevance ?? '—'} · confidence {result.confidence_score ?? 'open detail'}</small>{result.summary && <span>{result.summary}</span>}</span><span className="result-meta"><b>{displaySeverity(result.severity)}</b><small>{displayDate(result.published_at)}</small></span>
            </button>
          ))}</div>}
        </article>

        <article className="surface intelligence-detail-panel">
          <header className="panel-heading"><div><p className="eyebrow">Canonical DTMO persistence</p><h2>Object investigation</h2></div><span className="evidence-label">Canonical detail</span></header>
          {!selectedId && <div className="intelligence-empty"><strong>No intelligence object selected</strong><span>Select a recent item or search hit to retrieve canonical detail and provenance.</span></div>}
          {detailLoading && <p className="panel-state">Loading canonical object detail…</p>}
          {detailError && <div className="panel-state error-state"><strong>Canonical detail unavailable</strong><span>{detailError}.</span></div>}
          {detail && <div className="intelligence-detail">
            <div className="detail-title-row"><div><span className={`severity-pill severity-${displaySeverity(detail.severity)}`}>{displaySeverity(detail.severity)}</span><h3>{detail.title}</h3><p>{detail.summary || 'No canonical summary recorded.'}</p></div><a className="button secondary" href={detail.canonical_url} target="_blank" rel="noreferrer">Open source</a></div>
            <dl className="intelligence-facts"><div><dt>Source</dt><dd>{detail.source_id}</dd></div><div><dt>Education relevance</dt><dd>{detail.education_relevance}/100</dd></div><div><dt>Confidence</dt><dd>{detail.confidence_score}/100 · {detail.confidence_level}</dd></div><div><dt>Review status</dt><dd>{detail.review_status}</dd></div><div><dt>Sharing</dt><dd>{detail.share_approved ? 'Approved for sharing' : 'Not approved for sharing'}</dd></div><div><dt>Discovered</dt><dd>{displayDate(detail.discovered_at)}</dd></div></dl>
            <section className="detail-section object-actions" aria-label="Object actions"><h4>Continue investigation</h4><div className="quick-grid"><a className="quick-action" href={`/workbench/analysis?item=${encodeURIComponent(detail.id)}`}><span aria-hidden="true">⌁</span><div><strong>Analyze &amp; enrich</strong><small>Open persisted IntelOwl/Cortex history for this canonical object.</small></div></a><a className="quick-action" href={`/workbench/intelligence/graph?item=${encodeURIComponent(detail.id)}`}><span aria-hidden="true">⌘</span><div><strong>Open graph context</strong><small>Load only persisted OpenCTI mappings for this canonical object.</small></div></a><a className="quick-action" href={`/workbench/investigations?item=${encodeURIComponent(detail.id)}`}><span aria-hidden="true">▣</span><div><strong>Open investigation</strong><small>Load persisted case-handoff state and explicit TheHive blockers for this canonical object.</small></div></a><a className="quick-action" href={`/workbench/sharing?item=${encodeURIComponent(detail.id)}`}><span aria-hidden="true">⇄</span><div><strong>Review &amp; share</strong><small>Open the governed review, approval and MISP export chain for this canonical object.</small></div></a></div><p className="boundary-copy">These pivots carry only the canonical object identifier. Each destination reloads server-authorized persisted context. Analysis never executes an analyzer automatically; Graph does not query OpenCTI directly or infer absent upstream knowledge; Investigations does not create a case or grant responder authority; Sharing grants no review, share approval, export, publication or synchronization authority by navigation alone.</p></section>
            <section className="detail-section"><h4>Analytical confidence</h4><p>{detail.confidence_rationale || 'No confidence rationale recorded.'}</p></section>
            <section className="detail-section"><h4>Threat context</h4><div className="context-tags">{detail.context.cve_ids.map((cve) => <span key={cve}>{cve}</span>)}{detail.context.known_exploited && <span>Known exploited</span>}{detail.context.vendor && <span>{detail.context.vendor}</span>}{detail.context.product && <span>{detail.context.product}</span>}{detail.tags.map((tag) => <span key={`tag-${tag}`}>{tag}</span>)}</div></section>
            <section className="detail-section"><h4>Provenance chain</h4>{!detail.provenance.length && <p>No provenance records are available for this canonical object.</p>}<div className="provenance-list">{detail.provenance.map((item, index) => <a href={item.source_url} target="_blank" rel="noreferrer" key={`${item.source_url}-${index}`} className="provenance-row"><span><strong>{item.source_title ?? item.publisher ?? 'Source evidence'}</strong><small>{item.publisher ?? 'publisher not recorded'} · retrieved {displayDate(item.retrieved_at)}</small></span><span><b>{item.is_primary_source ? 'Primary' : 'Secondary'}</b><small>integrity {item.content_integrity_verified ? 'verified' : 'not verified'} · confidence {item.confidence_score}</small></span></a>)}</div></section>
          </div>}
        </article>
      </div>

      <article className="surface evidence-surface intelligence-evidence"><div><p className="eyebrow">Evidence boundary</p><h2>Canonical recent view without fabricated content</h2></div><p>The default Threat Intelligence view is populated only from objects already present in canonical DTMO persistence. When that persistence is empty, an authorized operator can execute an already-enabled governed source from the same canonical workspace and then explicitly reload recent persistence. IOC and other canonical object pivots may deep-link by canonical item identifier, but the detail is still retrieved from the server-authorized canonical workspace API. Search remains a separate governed projection. Missing content stays visibly missing and is never converted into synthetic intelligence, live-source health, staging acceptance or production authorization.</p></article>
    </section>
  );
}
