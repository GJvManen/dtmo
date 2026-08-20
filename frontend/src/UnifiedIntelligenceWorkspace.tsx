import { useState } from 'react';
import type { FormEvent } from 'react';

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

type IntelligenceSearchResponse = {
  query: string;
  count: number;
  results: IntelligenceSearchResult[];
};

type IntelligenceProvenance = {
  source_url: string;
  source_title: string | null;
  publisher: string | null;
  retrieved_at: string;
  source_reliability: string | null;
  is_primary_source: boolean;
  content_integrity_verified: boolean;
  confidence_score: number;
};

type IntelligenceContext = {
  cve_ids: string[];
  known_exploited: boolean;
  vendor: string | null;
  product: string | null;
};

type IntelligenceWorkspaceDetail = {
  id: string;
  source_id: string;
  external_id: string | null;
  item_type: string;
  title: string;
  summary: string;
  canonical_url: string;
  published_at: string | null;
  discovered_at: string;
  severity: string;
  confidence_score: number;
  confidence_level: string;
  confidence_rationale: string;
  education_relevance: number;
  review_status: string;
  share_approved: boolean;
  tags: string[];
  context: IntelligenceContext;
  provenance: IntelligenceProvenance[];
};

type Mode = 'intelligence' | 'ioc';

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url, {
    credentials: 'same-origin',
    headers: { Accept: 'application/json' },
  });
  let body: unknown = null;
  try {
    body = await response.json();
  } catch {
    body = null;
  }
  if (!response.ok) {
    const detail = typeof body === 'object' && body !== null && 'detail' in body
      ? String((body as { detail: unknown }).detail)
      : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

function displaySeverity(value?: string) {
  if (!value) return 'informational';
  return value.toLowerCase();
}

function displayDate(value?: string | null) {
  if (!value) return 'Not recorded';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

export function UnifiedIntelligenceWorkspace({ mode = 'intelligence' }: { mode?: Mode }) {
  const [query, setQuery] = useState('');
  const [severity, setSeverity] = useState('');
  const [minimumRelevance, setMinimumRelevance] = useState(0);
  const [size, setSize] = useState(50);
  const [results, setResults] = useState<IntelligenceSearchResult[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<IntelligenceWorkspaceDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<string | null>(null);

  const isIoc = mode === 'ioc';
  const title = isIoc ? 'IOC Explorer' : 'Threat Intelligence';
  const description = isIoc
    ? 'Indicator-oriented discovery over the same governed DTMO intelligence index and canonical object detail.'
    : 'Search, triage and investigate DTMO intelligence with attributable canonical detail and provenance.';

  async function runSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const normalizedQuery = query.trim();
    if (normalizedQuery.length < 2) return;

    setSearching(true);
    setSearchError(null);
    setHasSearched(true);
    setSelectedId(null);
    setDetail(null);
    setDetailError(null);

    const params = new URLSearchParams({
      q: normalizedQuery,
      minimum_relevance: String(minimumRelevance),
      size: String(size),
    });
    if (severity) params.set('severity', severity);

    try {
      const response = await getJson<IntelligenceSearchResponse>(`/api/v1/intelligence/search?${params.toString()}`);
      setResults(response.results);
    } catch (error) {
      setResults([]);
      setSearchError(error instanceof Error ? error.message : 'Search backend unavailable');
    } finally {
      setSearching(false);
    }
  }

  async function selectResult(result: IntelligenceSearchResult) {
    setSelectedId(result.id);
    setDetail(null);
    setDetailError(null);
    setDetailLoading(true);
    try {
      const response = await getJson<IntelligenceWorkspaceDetail>(`/api/v1/intelligence/${encodeURIComponent(result.id)}/workspace`);
      setDetail(response);
    } catch (error) {
      setDetailError(error instanceof Error ? error.message : 'Canonical intelligence detail unavailable');
    } finally {
      setDetailLoading(false);
    }
  }

  return (
    <section className="unified-intelligence" aria-labelledby="workspace-title">
      <header className="workspace-heading intelligence-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">{title}</h1>
          <p>{description}</p>
        </div>
        <div className="heading-statuses">
          <span className="phase-badge">11.10d Unified Intelligence</span>
          <span className="phase-badge available">Read-only investigation</span>
        </div>
      </header>

      <article className="surface intelligence-search-surface">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">Governed discovery</p>
            <h2>{isIoc ? 'Search indicators and intelligence' : 'Search canonical intelligence'}</h2>
          </div>
          <span className="evidence-label">Explicit search · no synthetic results</span>
        </div>
        <form className="intelligence-search-form" onSubmit={runSearch}>
          <label className="search-query-field">
            <span>Search canonical intelligence</span>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              minLength={2}
              maxLength={300}
              required
              placeholder={isIoc ? 'Domain, IP, hash, CVE or indicator context…' : 'Threat, campaign, actor, CVE, technology…'}
              autoComplete="off"
            />
          </label>
          <label>
            <span>Severity</span>
            <select value={severity} onChange={(event) => setSeverity(event.target.value)}>
              <option value="">All severities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
              <option value="informational">Informational</option>
            </select>
          </label>
          <label>
            <span>Minimum education relevance</span>
            <input type="number" min={0} max={100} value={minimumRelevance} onChange={(event) => setMinimumRelevance(Number(event.target.value))} />
          </label>
          <label>
            <span>Maximum results</span>
            <input type="number" min={1} max={200} value={size} onChange={(event) => setSize(Number(event.target.value))} />
          </label>
          <button className="button primary intelligence-search-button" type="submit" disabled={searching || query.trim().length < 2}>
            {searching ? 'Searching…' : 'Search intelligence'}
          </button>
        </form>
        <p className="boundary-copy">Search requires server-authorized <code>read:intelligence</code>. Searching or selecting an object grants no review, publication, sharing, connector-execution or case-mutation authority.</p>
      </article>

      <div className="intelligence-workspace-grid">
        <article className="surface intelligence-results-panel">
          <header className="panel-heading">
            <div><p className="eyebrow">Discovery index</p><h2>Search results</h2></div>
            <span className="evidence-label">{hasSearched && !searchError ? `${results.length} returned` : 'Search not asserted'}</span>
          </header>
          {!hasSearched && <div className="intelligence-empty"><strong>Search is explicit</strong><span>No default or demonstration intelligence is fabricated before a governed query is submitted.</span></div>}
          {searching && <p className="panel-state">Searching the governed intelligence index…</p>}
          {searchError && <div className="panel-state error-state"><strong>Search service unavailable</strong><span>{searchError}. No empty-result or platform-health conclusion is inferred.</span></div>}
          {hasSearched && !searching && !searchError && results.length === 0 && <div className="intelligence-empty"><strong>No intelligence matched this query</strong><span>This result describes the queried DTMO search index only; it does not prove absence from upstream sources.</span></div>}
          {!searching && !searchError && results.length > 0 && (
            <div className="intelligence-result-list" aria-label="Intelligence search results">
              {results.map((result) => (
                <button
                  type="button"
                  key={result.id}
                  aria-label={`Open ${result.title}`}
                  aria-pressed={selectedId === result.id}
                  className={`intelligence-result ${selectedId === result.id ? 'selected' : ''}`}
                  onClick={() => void selectResult(result)}
                >
                  <span className={`severity-dot severity-${displaySeverity(result.severity)}`} aria-hidden="true" />
                  <span className="result-copy">
                    <strong>{result.title}</strong>
                    <small>{result.source_id ?? 'source unavailable'} · relevance {result.education_relevance ?? '—'} · confidence {result.confidence_score ?? '—'}</small>
                    {result.summary && <span>{result.summary}</span>}
                  </span>
                  <span className="result-meta"><b>{displaySeverity(result.severity)}</b><small>{displayDate(result.published_at)}</small></span>
                </button>
              ))}
            </div>
          )}
        </article>

        <article className="surface intelligence-detail-panel">
          <header className="panel-heading">
            <div><p className="eyebrow">Canonical DTMO persistence</p><h2>Object investigation</h2></div>
            <span className="evidence-label">Canonical detail</span>
          </header>
          {!selectedId && <div className="intelligence-empty"><strong>No intelligence object selected</strong><span>Select a search hit to retrieve its canonical DTMO object and provenance chain.</span></div>}
          {detailLoading && <p className="panel-state">Loading canonical object detail…</p>}
          {detailError && <div className="panel-state error-state"><strong>Canonical detail unavailable</strong><span>{detailError}. The search hit remains discovery evidence only.</span></div>}
          {detail && (
            <div className="intelligence-detail">
              <div className="detail-title-row">
                <div>
                  <span className={`severity-pill severity-${displaySeverity(detail.severity)}`}>{displaySeverity(detail.severity)}</span>
                  <h3>{detail.title}</h3>
                  <p>{detail.summary || 'No canonical summary recorded.'}</p>
                </div>
                <a className="button secondary" href={detail.canonical_url} target="_blank" rel="noreferrer">Open source</a>
              </div>

              <dl className="intelligence-facts">
                <div><dt>Source</dt><dd>{detail.source_id}</dd></div>
                <div><dt>Education relevance</dt><dd>{detail.education_relevance}/100</dd></div>
                <div><dt>Confidence</dt><dd>{detail.confidence_score}/100 · {detail.confidence_level}</dd></div>
                <div><dt>Review status</dt><dd>{detail.review_status}</dd></div>
                <div><dt>Sharing</dt><dd>{detail.share_approved ? 'Approved for sharing' : 'Not approved for sharing'}</dd></div>
                <div><dt>Discovered</dt><dd>{displayDate(detail.discovered_at)}</dd></div>
              </dl>

              <section className="detail-section" aria-labelledby="confidence-title">
                <h4 id="confidence-title">Analytical confidence</h4>
                <p>{detail.confidence_rationale || 'No confidence rationale recorded.'}</p>
              </section>

              <section className="detail-section" aria-labelledby="context-title">
                <h4 id="context-title">Threat context</h4>
                <div className="context-tags">
                  {detail.context.cve_ids.map((cve) => <span key={cve}>{cve}</span>)}
                  {detail.context.known_exploited && <span>Known exploited</span>}
                  {detail.context.vendor && <span>{detail.context.vendor}</span>}
                  {detail.context.product && <span>{detail.context.product}</span>}
                  {detail.tags.map((tag) => <span key={`tag-${tag}`}>{tag}</span>)}
                  {!detail.context.cve_ids.length && !detail.context.known_exploited && !detail.context.vendor && !detail.context.product && !detail.tags.length && <span>No structured context recorded</span>}
                </div>
              </section>

              <section className="detail-section" aria-labelledby="provenance-title">
                <h4 id="provenance-title">Provenance chain</h4>
                {!detail.provenance.length && <p>No provenance records are available for this canonical object.</p>}
                <div className="provenance-list">
                  {detail.provenance.map((item, index) => (
                    <a href={item.source_url} target="_blank" rel="noreferrer" key={`${item.source_url}-${index}`} className="provenance-row">
                      <span><strong>{item.source_title ?? item.publisher ?? 'Source evidence'}</strong><small>{item.publisher ?? 'publisher not recorded'} · retrieved {displayDate(item.retrieved_at)}</small></span>
                      <span><b>{item.is_primary_source ? 'Primary' : 'Secondary'}</b><small>integrity {item.content_integrity_verified ? 'verified' : 'not verified'} · confidence {item.confidence_score}</small></span>
                    </a>
                  ))}
                </div>
              </section>
            </div>
          )}
        </article>
      </div>

      <article className="surface evidence-surface intelligence-evidence">
        <div><p className="eyebrow">Evidence boundary</p><h2>Indexed discovery is not canonical truth</h2></div>
        <p>Search results are discovery projections from the governed DTMO search service. Selected object detail and provenance are retrieved from canonical DTMO persistence. Missing results, failed dependencies or absent fields remain unavailable and are never converted into synthetic intelligence, upstream-health evidence, staging acceptance or production authorization.</p>
      </article>
    </section>
  );
}
