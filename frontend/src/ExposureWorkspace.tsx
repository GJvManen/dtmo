import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';

import { ThreatIntelligencePopulation } from './ThreatIntelligencePopulation';

type VulnerabilityRow = {
  cve_id?: string;
  title?: string;
  cvss?: number | null;
  cvss_score?: number | null;
  epss?: number | null;
  kev?: boolean;
  vendors?: string[];
  products?: string[];
  cwes?: string[];
  source_id?: string;
  canonical_url?: string | null;
  discovered_at?: string | null;
  raw_sha256?: string | null;
};

type Analytics = {
  rows?: VulnerabilityRow[];
  vulnerabilities?: VulnerabilityRow[];
  items?: VulnerabilityRow[];
  degraded_reasons?: string[];
  evidence_boundary?: string;
};

type PriorityFilter = 'all' | 'kev' | 'critical';

async function loadExposure(): Promise<Analytics> {
  const response = await fetch('/api/v1/console/vulnerability-analytics?window=30d', {
    credentials: 'same-origin', headers: { Accept: 'application/json' },
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

function score(row: VulnerabilityRow) { return row.cvss_score ?? row.cvss ?? null; }
function rows(data?: Analytics) { return data?.rows ?? data?.vulnerabilities ?? data?.items ?? []; }
function normalizedEpss(row: VulnerabilityRow) {
  const value = row.epss;
  if (value == null || Number.isNaN(Number(value))) return null;
  const numeric = Number(value);
  return numeric > 1 ? numeric / 100 : numeric;
}
function contains(values: string[] | undefined, needle: string) {
  if (!needle.trim()) return true;
  const normalized = needle.trim().toLowerCase();
  return (values ?? []).some((value) => value.toLowerCase().includes(normalized));
}
function displayDate(value?: string | null) {
  if (!value) return 'Not recorded';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

export function ExposureWorkspace() {
  const query = useQuery({ queryKey: ['exposure', '30d'], queryFn: loadExposure, retry: false, refetchInterval: 60_000 });
  const [priority, setPriority] = useState<PriorityFilter>('all');
  const [vendor, setVendor] = useState('');
  const [product, setProduct] = useState('');
  const [cwe, setCwe] = useState('');
  const [minimumEpss, setMinimumEpss] = useState(0);
  const inventory = rows(query.data);

  const visible = useMemo(() => rows(query.data).filter((row) => {
    if (priority === 'kev' && row.kev !== true) return false;
    if (priority === 'critical' && (score(row) ?? 0) < 9) return false;
    if (!contains(row.vendors, vendor)) return false;
    if (!contains(row.products, product)) return false;
    if (!contains(row.cwes, cwe)) return false;
    const epss = normalizedEpss(row);
    if (minimumEpss > 0 && (epss == null || epss < minimumEpss / 100)) return false;
    return true;
  }), [query.data, priority, vendor, product, cwe, minimumEpss]);

  return <section aria-labelledby="exposure-title">
    <header className="workspace-heading"><div><p className="eyebrow">Phase 11.10q · Functional recovery</p><h1 id="exposure-title">Vulnerability &amp; Exposure Center</h1><p>Evidence-backed vulnerability intelligence from the canonical DTMO store. CVSS, EPSS and KEV are prioritization evidence, not proof that an asset is exposed or compromised.</p></div><span className="phase-badge">Canonical DTMO API</span></header>
    <div className="identity-strip" role="note"><span>Read authority: read:intelligence</span><span>No asset exposure, exploitability, remediation or compromise is inferred from intelligence presence.</span></div>

    <div className="surface command-panel">
      <header className="panel-heading"><div><p className="eyebrow">30-day canonical evidence window</p><h2>Exposure discovery filters</h2></div><span className="evidence-label">Canonical attributes only</span></header>
      <div className="intelligence-search-form exposure-filter-grid">
        <label><span>Priority view</span><select value={priority} onChange={(event) => setPriority(event.target.value as PriorityFilter)}><option value="all">All vulnerabilities</option><option value="kev">CISA KEV evidence</option><option value="critical">CVSS ≥ 9</option></select></label>
        <label><span>Vendor</span><input value={vendor} onChange={(event) => setVendor(event.target.value)} placeholder="e.g. Microsoft" autoComplete="off" /></label>
        <label><span>Product</span><input value={product} onChange={(event) => setProduct(event.target.value)} placeholder="e.g. Exchange" autoComplete="off" /></label>
        <label><span>CWE</span><input value={cwe} onChange={(event) => setCwe(event.target.value)} placeholder="e.g. CWE-79" autoComplete="off" /></label>
        <label><span>Minimum EPSS (%)</span><input type="number" min={0} max={100} step={1} value={minimumEpss} onChange={(event) => setMinimumEpss(Number(event.target.value))} /></label>
      </div>
      <p className="boundary-copy">Filters operate only on attributes already present in canonical DTMO vulnerability evidence. Missing attributes never satisfy a positive filter and are never synthesized.</p>
    </div>

    <div className="surface command-panel">
      <header className="panel-heading"><div><p className="eyebrow">Prioritization evidence</p><h2>Canonical vulnerability inventory</h2></div><span className="evidence-label">{query.isPending ? 'Loading…' : `${visible.length} matching`}</span></header>
      {query.isPending && <p className="panel-state">Loading canonical vulnerability evidence…</p>}
      {query.isError && <div className="panel-state error-state"><strong>Vulnerability evidence unavailable</strong><span>The workspace fails closed and does not synthesize exposure state.</span></div>}
      {query.data?.degraded_reasons?.length ? <div className="panel-state error-state"><strong>Evidence degraded</strong><span>{query.data.degraded_reasons.join(' · ')}</span></div> : null}
      {!query.isPending && !query.isError && inventory.length === 0 && <>
        <div className="panel-state"><strong>No attributable vulnerability evidence is recorded yet</strong><span>Use an already-enabled governed source below. An empty canonical projection does not prove absence of vulnerabilities or exposure.</span></div>
        <ThreatIntelligencePopulation
          title="Populate canonical vulnerability evidence"
          reloadLabel="Reload vulnerability evidence"
          enabledSourcesLabel="Enabled governed sources for vulnerability population"
          onPopulated={() => { void query.refetch(); }}
        />
      </>}
      {!query.isPending && !query.isError && inventory.length > 0 && visible.length === 0 && <div className="panel-state"><strong>No attributable vulnerability evidence matches these filters</strong><span>Adjust the filters. A filtered empty view does not prove absence of vulnerabilities or exposure.</span></div>}
      {visible.length > 0 && <div className="intel-list" role="list">{visible.map((row, index) => <article className="intel-row" role="listitem" key={`${row.cve_id ?? row.title ?? 'vulnerability'}-${index}`}>
        <span className={`severity-dot ${(score(row) ?? 0) >= 9 ? 'severity-critical' : (score(row) ?? 0) >= 7 ? 'severity-high' : 'severity-medium'}`} />
        <div className="intel-copy"><strong>{row.cve_id ?? row.title ?? 'Unidentified vulnerability'}</strong><span>{row.source_id ?? 'canonical source'} · CVSS {score(row) ?? '—'} · EPSS {row.epss ?? '—'} · {row.kev ? 'CISA KEV evidence present' : 'no KEV evidence'}</span><span>{[...(row.vendors ?? []), ...(row.products ?? []), ...(row.cwes ?? [])].slice(0,6).join(' · ') || 'No attributable vendor/product/CWE mapping'}</span><span>Discovered {displayDate(row.discovered_at)}</span></div>
        <div className="result-meta"><span className="evidence-label">{row.raw_sha256 ? 'raw evidence bound' : 'evidence reference unavailable'}</span>{row.canonical_url ? <a className="button secondary" href={row.canonical_url} target="_blank" rel="noreferrer">Open evidence source</a> : <span className="evidence-label">No canonical source link</span>}</div>
      </article>)}</div>}
    </div>

    <article className="surface evidence-surface"><div><p className="eyebrow">Evidence boundary</p><h2>Prioritize vulnerabilities without inventing local exposure</h2></div><p>CVSS, EPSS, KEV, vendor, product and CWE are canonical intelligence attributes. When the canonical vulnerability projection is empty, an authorized operator can execute an already-enabled governed source from this workspace and then explicitly reload the projection. The source pivot opens attributable evidence only. Neither population, the inventory nor its filters establish that a local asset is affected, reachable, exploitable, compromised or remediated, and they grant no scanner, remediation, case, publication or sharing authority.</p></article>
    <p className="evidence-label">{query.data?.evidence_boundary ?? 'Repository/runtime data shown here does not constitute production-equivalent validation or production authorization.'}</p>
  </section>;
}
