import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';

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

async function loadExposure(): Promise<Analytics> {
  const response = await fetch('/api/v1/console/vulnerability-analytics?window=30d', {
    credentials: 'same-origin', headers: { Accept: 'application/json' },
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

function score(row: VulnerabilityRow) { return row.cvss_score ?? row.cvss ?? null; }
function rows(data?: Analytics) { return data?.rows ?? data?.vulnerabilities ?? data?.items ?? []; }

export function ExposureWorkspace() {
  const query = useQuery({ queryKey: ['exposure', '30d'], queryFn: loadExposure, retry: false, refetchInterval: 60_000 });
  const [filter, setFilter] = useState<'all' | 'kev' | 'critical'>('all');
  const visible = useMemo(() => rows(query.data).filter((row) => filter === 'all' || (filter === 'kev' ? row.kev === true : (score(row) ?? 0) >= 9)), [query.data, filter]);

  return <section aria-labelledby="exposure-title">
    <header className="workspace-heading"><div><p className="eyebrow">Phase 11.10i · Vulnerability & Exposure</p><h1 id="exposure-title">Vulnerability & Exposure Center</h1><p>Evidence-backed vulnerability intelligence from the canonical DTMO store. CVSS, EPSS and KEV are prioritization evidence, not proof that an asset is exposed or compromised.</p></div><span className="phase-badge">Canonical DTMO API</span></header>
    <div className="identity-strip" role="note"><span>Read authority: read:intelligence</span><span>No asset exposure, exploitability, remediation or compromise is inferred from intelligence presence.</span></div>
    <div className="surface command-panel">
      <header className="panel-heading"><div><p className="eyebrow">30-day evidence window</p><h2>Prioritized vulnerabilities</h2></div><div>{(['all','kev','critical'] as const).map((value) => <button key={value} type="button" className="text-link" aria-pressed={filter===value} onClick={() => setFilter(value)}>{value === 'all' ? 'All' : value === 'kev' ? 'KEV' : 'CVSS ≥ 9'}</button>)}</div></header>
      {query.isPending && <p className="panel-state">Loading canonical vulnerability evidence…</p>}
      {query.isError && <div className="panel-state error-state"><strong>Vulnerability evidence unavailable</strong><span>The workspace fails closed and does not synthesize exposure state.</span></div>}
      {query.data?.degraded_reasons?.length ? <div className="panel-state error-state"><strong>Evidence degraded</strong><span>{query.data.degraded_reasons.join(' · ')}</span></div> : null}
      {!query.isPending && !query.isError && visible.length === 0 && <p className="panel-state">No attributable vulnerability evidence matches this view.</p>}
      {visible.length > 0 && <div className="intel-list" role="list">{visible.map((row, index) => <article className="intel-row" role="listitem" key={`${row.cve_id ?? row.title ?? 'vulnerability'}-${index}`}><span className={`severity-dot ${(score(row) ?? 0) >= 9 ? 'severity-critical' : (score(row) ?? 0) >= 7 ? 'severity-high' : 'severity-medium'}`} /><div className="intel-copy"><strong>{row.cve_id ?? row.title ?? 'Unidentified vulnerability'}</strong><span>{row.source_id ?? 'canonical source'} · CVSS {score(row) ?? '—'} · EPSS {row.epss ?? '—'} · {row.kev ? 'CISA KEV evidence present' : 'no KEV evidence'}</span><span>{[...(row.vendors ?? []), ...(row.products ?? [])].slice(0,4).join(' · ') || 'No attributable vendor/product mapping'}</span></div><span className="evidence-label">{row.raw_sha256 ? 'raw evidence bound' : 'evidence reference unavailable'}</span></article>)}</div>}
    </div>
    <p className="evidence-label">{query.data?.evidence_boundary ?? 'Repository/runtime data shown here does not constitute production-equivalent validation or production authorization.'}</p>
  </section>;
}
