import { useEffect, useMemo, useState } from 'react';
import type { FormEvent } from 'react';

import './analysis-workspace.css';

type Session = { subject: string; roles: string[]; permissions: string[] };
type Capabilities = {
  intelowl_enabled: boolean; intelowl_observable_types: string[]; intelowl_analyzers: string[];
  cortex_enabled: boolean; cortex_observable_types: string[]; cortex_analyzers: string[];
  runtime_health_claim: boolean; responder_actions_allowed: boolean; external_share_authority: boolean; local_compromise_proof: boolean;
};
type RecentIntelligence = { id: string; title: string; source_id: string; severity: string; education_relevance: number; review_status: string; discovered_at: string };
type CommandCenterSnapshot = { data_state: 'available' | 'unavailable'; recent_intelligence: RecentIntelligence[] };
type IntelOwlRecord = { record_id: string; item_id: string; job_id: string; status: string; partial: boolean; analyzers: string[]; external_share_authorized: boolean; local_compromise_proven: boolean };
type CortexRecord = { record_id: string; item_id: string; job_id: string; status: string; analyzer_id: string; tlp: number; report: Record<string, unknown>; external_share_authorized: boolean; local_compromise_proven: boolean };
type History = { item_id: string; intelowl: { records: IntelOwlRecord[] }; cortex: { records: CortexRecord[] }; evidence_boundary: string };

async function json<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, { credentials: 'same-origin', ...init, headers: { Accept: 'application/json', ...(init?.body ? { 'Content-Type': 'application/json' } : {}), ...(init?.headers ?? {}) } });
  let body: unknown = null;
  try { body = await response.json(); } catch { body = null; }
  if (!response.ok) {
    const detail = typeof body === 'object' && body !== null && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

function selectDefault(values: string[], fallback: string) { return values[0] ?? fallback; }
function displayDate(value: string) { const date = new Date(value); return Number.isNaN(date.getTime()) ? value : date.toLocaleString(); }

export function AnalysisWorkspace() {
  const initial = useMemo(() => new URLSearchParams(window.location.search), []);
  const initialItem = initial.get('item') ?? '';
  const initialObservableType = initial.get('observable_type') ?? '';
  const initialObservableValue = initial.get('observable_value') ?? '';
  const [session, setSession] = useState<Session | null>(null);
  const [capabilities, setCapabilities] = useState<Capabilities | null>(null);
  const [recent, setRecent] = useState<RecentIntelligence[]>([]);
  const [recentState, setRecentState] = useState<'loading' | 'available' | 'empty' | 'error'>('loading');
  const [itemId, setItemId] = useState(initialItem);
  const [loadedItem, setLoadedItem] = useState('');
  const [history, setHistory] = useState<History | null>(null);
  const [historyError, setHistoryError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [observableType, setObservableType] = useState(initialObservableType || 'domain');
  const [observableValue, setObservableValue] = useState(initialObservableValue);
  const [handling, setHandling] = useState('TLP:AMBER');
  const [intelowlAnalyzers, setIntelowlAnalyzers] = useState('');
  const [cortexAnalyzer, setCortexAnalyzer] = useState('');
  const [tlp, setTlp] = useState(2);
  const [executionState, setExecutionState] = useState<string | null>(null);
  const [executionError, setExecutionError] = useState<string | null>(null);
  const canReview = session?.permissions.includes('review:intelligence') ?? false;

  useEffect(() => {
    void Promise.all([json<Session>('/api/v1/ui/session'), json<Capabilities>('/api/v1/analysis/capabilities')]).then(([nextSession, nextCapabilities]) => {
      setSession(nextSession); setCapabilities(nextCapabilities);
      if (!initialObservableType) setObservableType(selectDefault(nextCapabilities.intelowl_observable_types, selectDefault(nextCapabilities.cortex_observable_types, 'domain')));
      setIntelowlAnalyzers(nextCapabilities.intelowl_analyzers.join(', '));
      setCortexAnalyzer(selectDefault(nextCapabilities.cortex_analyzers, ''));
    }).catch((error) => setHistoryError(error instanceof Error ? error.message : 'Analysis capabilities unavailable'));
    void json<CommandCenterSnapshot>('/api/v1/command-center').then((snapshot) => {
      if (snapshot.data_state !== 'available') { setRecent([]); setRecentState('error'); return; }
      setRecent(snapshot.recent_intelligence); setRecentState(snapshot.recent_intelligence.length ? 'available' : 'empty');
    }).catch(() => { setRecent([]); setRecentState('error'); });
  }, [initialObservableType]);

  async function loadHistory(target = itemId) {
    const normalized = target.trim(); if (!normalized) return;
    setLoading(true); setHistoryError(null);
    try {
      const response = await json<History>(`/api/v1/analysis/items/${encodeURIComponent(normalized)}/history`);
      setHistory(response); setLoadedItem(normalized); setItemId(normalized);
      const params = new URLSearchParams({ item: normalized });
      if (observableType.trim()) params.set('observable_type', observableType.trim());
      if (observableValue.trim()) params.set('observable_value', observableValue.trim());
      window.history.replaceState(null, '', `/workbench/analysis?${params.toString()}`);
    } catch (error) {
      setHistory(null); setHistoryError(error instanceof Error ? error.message : 'Integrated analysis history unavailable');
    } finally { setLoading(false); }
  }

  useEffect(() => { if (initialItem) void loadHistory(initialItem); }, []);

  async function executeIntelOwl(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setExecutionState('Running IntelOwl enrichment…'); setExecutionError(null);
    try {
      await json(`/api/v1/intelowl/items/${encodeURIComponent(itemId.trim())}/enrich`, { method: 'POST', body: JSON.stringify({ observable_type: observableType, observable_value: observableValue.trim(), handling, analyzers: intelowlAnalyzers.split(',').map((value) => value.trim()).filter(Boolean) }) });
      setExecutionState('IntelOwl enrichment persisted as governed evidence.'); await loadHistory(itemId);
    } catch (error) { setExecutionState(null); setExecutionError(error instanceof Error ? error.message : 'IntelOwl execution failed'); }
  }

  async function executeCortex(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setExecutionState('Running Cortex analyzer…'); setExecutionError(null);
    try {
      await json(`/api/v1/analysis/items/${encodeURIComponent(itemId.trim())}/cortex`, { method: 'POST', body: JSON.stringify({ observable_type: observableType, observable_value: observableValue.trim(), analyzer_id: cortexAnalyzer, tlp }) });
      setExecutionState('Cortex analyzer result persisted as governed evidence.'); await loadHistory(itemId);
    } catch (error) { setExecutionState(null); setExecutionError(error instanceof Error ? error.message : 'Cortex execution failed'); }
  }

  return <section className="analysis-workspace" aria-labelledby="workspace-title">
    <header className="workspace-heading analysis-heading"><div><p className="eyebrow">Unified Operations Workbench</p><h1 id="workspace-title">Analysis &amp; Enrichment</h1><p>Object-driven IntelOwl enrichment and analyzer-only Cortex execution with persisted history and results.</p></div><div className="heading-statuses"><span className="phase-badge">11.10e Integrated Analysis · 11.10q recovery</span><span className="phase-badge available">Human authorized</span></div></header>

    <article className="surface analysis-object-surface">
      <div className="panel-heading"><div><p className="eyebrow">Canonical target discovery</p><h2>Select intelligence object</h2></div><span className="evidence-label">Canonical DTMO persistence</span></div>
      {recentState === 'loading' && <p className="panel-state">Loading recent canonical intelligence…</p>}
      {recentState === 'error' && <div className="panel-state error-state"><strong>Canonical target discovery unavailable</strong><span>No empty-object or platform-health conclusion is inferred. A deep link remains available for troubleshooting.</span></div>}
      {recentState === 'empty' && <div className="panel-state"><strong>No canonical intelligence targets recorded yet</strong><span>Run a governed source first; Analysis does not synthesize targets.</span></div>}
      {recent.length > 0 && <div className="analysis-record-list" aria-label="Recent canonical intelligence targets">{recent.map((item) => <button type="button" className="analysis-record" key={item.id} aria-pressed={itemId === item.id} onClick={() => void loadHistory(item.id)}><div><strong>{item.title}</strong><span>{item.source_id} · {item.severity}</span></div><p>Review {item.review_status} · relevance {item.education_relevance}/100</p><small>{displayDate(item.discovered_at)}</small></button>)}</div>}
      <details><summary>Advanced deep link / troubleshooting</summary><form className="analysis-object-form" onSubmit={(event) => { event.preventDefault(); void loadHistory(); }}><label><span>Canonical intelligence item ID</span><input value={itemId} onChange={(event) => setItemId(event.target.value)} required placeholder="Canonical UUID" /></label><button className="button secondary" type="submit" disabled={loading || !itemId.trim()}>{loading ? 'Loading…' : 'Load analysis history'}</button></form></details>
      {historyError && <div className="panel-state error-state"><strong>History unavailable</strong><span>{historyError}. No empty-history conclusion is inferred.</span></div>}
    </article>

    <section className="analysis-capability-grid" aria-label="Analysis capabilities">
      <article className="surface capability-card"><p className="eyebrow">IntelOwl</p><h2>{capabilities?.intelowl_enabled ? 'Enabled' : 'Disabled'}</h2><p>{capabilities?.intelowl_analyzers.length ? `${capabilities.intelowl_analyzers.length} allowlisted analyzers` : 'No analyzer allowlist exposed.'}</p></article>
      <article className="surface capability-card"><p className="eyebrow">Cortex</p><h2>{capabilities?.cortex_enabled ? 'Enabled' : 'Disabled'}</h2><p>{capabilities?.cortex_analyzers.length ? `${capabilities.cortex_analyzers.length} allowlisted analyzers` : 'No analyzer allowlist exposed.'}</p></article>
      <article className="surface capability-card boundary"><p className="eyebrow">Authority boundary</p><h2>No responder authority</h2><p>Capability configuration is not runtime-health evidence and never authorizes external sharing.</p></article>
    </section>

    <article className="surface analysis-execution-surface">
      <header className="panel-heading"><div><p className="eyebrow">Explicit object-driven execution</p><h2>Analyze selected observable</h2></div><span className="evidence-label">review:intelligence required</span></header>
      {!itemId.trim() && <div className="panel-state"><strong>Select a canonical target first</strong><span>Choose recent intelligence or arrive from an IOC/Threat Intelligence pivot.</span></div>}
      {!canReview && <div className="panel-state"><strong>Read-only principal</strong><span>History remains visible, but analyzer execution is not presented as authorized for this session.</span></div>}
      <div className="analysis-shared-fields"><label><span>Observable type</span><select value={observableType} onChange={(event) => setObservableType(event.target.value)}>{[...new Set([...(capabilities?.intelowl_observable_types ?? []), ...(capabilities?.cortex_observable_types ?? [])])].map((value) => <option key={value}>{value}</option>)}</select></label><label><span>Observable value</span><input value={observableValue} onChange={(event) => setObservableValue(event.target.value)} required placeholder="Domain, IP, URL, hash or approved observable" /></label></div>
      <div className="analysis-engine-grid">
        <form className="analysis-engine" onSubmit={executeIntelOwl}><div><p className="eyebrow">Enrichment</p><h3>IntelOwl</h3><p>Runs only explicitly allowlisted analyzers and persists bounded enrichment history.</p></div><label><span>Handling</span><input value={handling} onChange={(event) => setHandling(event.target.value)} /></label><label><span>Analyzers, comma separated</span><input value={intelowlAnalyzers} onChange={(event) => setIntelowlAnalyzers(event.target.value)} /></label><button className="button primary" type="submit" disabled={!canReview || !capabilities?.intelowl_enabled || !itemId.trim() || !observableValue.trim() || !intelowlAnalyzers.trim()}>Run IntelOwl</button></form>
        <form className="analysis-engine" onSubmit={executeCortex}><div><p className="eyebrow">Analyzer-only</p><h3>Cortex</h3><p>Responders, discovery and side-effect actions remain outside the approved connector boundary.</p></div><label><span>Analyzer</span><select value={cortexAnalyzer} onChange={(event) => setCortexAnalyzer(event.target.value)}>{(capabilities?.cortex_analyzers ?? []).map((value) => <option key={value}>{value}</option>)}</select></label><label><span>TLP</span><select value={tlp} onChange={(event) => setTlp(Number(event.target.value))}><option value={0}>0 · WHITE/CLEAR</option><option value={1}>1 · GREEN</option><option value={2}>2 · AMBER</option><option value={3}>3 · RED</option></select></label><button className="button primary" type="submit" disabled={!canReview || !capabilities?.cortex_enabled || !itemId.trim() || !observableValue.trim() || !cortexAnalyzer}>Run Cortex</button></form>
      </div>
      {executionState && <p className="panel-state success-state">{executionState}</p>}{executionError && <div className="panel-state error-state"><strong>Analysis not completed</strong><span>{executionError}. No result is fabricated.</span></div>}
    </article>

    <div className="analysis-history-grid">
      <article className="surface analysis-history-panel"><header className="panel-heading"><div><p className="eyebrow">Persisted enrichment</p><h2>IntelOwl history</h2></div><span className="evidence-label">{history ? `${history.intelowl.records.length} records` : 'Not loaded'}</span></header>{history && history.intelowl.records.length === 0 && <p className="panel-state">No persisted IntelOwl record exists for this item.</p>}<div className="analysis-record-list">{history?.intelowl.records.map((record) => <article className="analysis-record" key={record.record_id}><div><strong>{record.status}</strong><span>Job {record.job_id}</span></div><p>{record.analyzers.join(', ') || 'Analyzer names unavailable'}{record.partial ? ' · partial' : ''}</p><small>External share: no · Local compromise proven: no</small></article>)}</div></article>
      <article className="surface analysis-history-panel"><header className="panel-heading"><div><p className="eyebrow">Persisted analysis/results</p><h2>Cortex history</h2></div><span className="evidence-label">{history ? `${history.cortex.records.length} records` : 'Not loaded'}</span></header>{history && history.cortex.records.length === 0 && <p className="panel-state">No persisted Cortex analyzer record exists for this item.</p>}<div className="analysis-record-list">{history?.cortex.records.map((record) => <article className="analysis-record" key={record.record_id}><div><strong>{record.status || 'unknown'}</strong><span>Job {record.job_id}</span></div><p>{record.analyzer_id} · TLP {record.tlp}</p><details><summary>Persisted result</summary><pre>{JSON.stringify(record.report, null, 2)}</pre></details><small>External share: no · Local compromise proven: no</small></article>)}</div></article>
    </div>

    <article className="surface evidence-surface analysis-evidence"><div><p className="eyebrow">Evidence boundary</p><h2>Enrichment is evidence, not a verdict</h2></div><p>{history?.evidence_boundary ?? 'IntelOwl and Cortex output never proves local compromise by itself, never grants sharing authority, and configuration alone is not a runtime-health claim.'}</p>{loadedItem && <small>Loaded canonical item: {loadedItem}</small>}</article>
  </section>;
}
