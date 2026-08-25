import { useEffect, useMemo, useState } from 'react';
import type { FormEvent } from 'react';

import { ThreatIntelligencePopulation } from './ThreatIntelligencePopulation';
import './opencti-graph.css';

type Capability = { enabled: boolean; configured: boolean; allowed_entity_types: string[]; runtime_health_claim: boolean; upstream_relationship_topology_persisted: boolean; external_share_authority: boolean; local_compromise_proof: boolean };
type Node = { id: string; kind: string; label: string; entity_type: string; stix_id: string | null; confidence: number | null; markings: Array<Record<string, unknown>>; last_seen_at: string | null };
type Edge = { id: string; source: string; target: string; relationship_type: string; evidence_class: string };
type Graph = { item_id: string; title: string; nodes: Node[]; edges: Edge[]; topology_scope: string; upstream_relationship_topology_persisted: boolean; evidence_boundary: string };
type Revision = { id: string; snapshot_hash: string; recorded_at: string; snapshot: Record<string, unknown> };
type Entity = { mapping_id: string; item_id: string; opencti_id: string; stix_id: string; entity_type: string; parent_types: string[]; markings: Array<Record<string, unknown>>; confidence: number | null; upstream_created_at: string | null; upstream_updated_at: string | null; external_references: Array<Record<string, unknown>>; provenance: Record<string, unknown>; snapshot_hash: string; last_seen_at: string; external_share_authorized: boolean; local_compromise_proven: boolean; revisions: Revision[]; evidence_boundary: string };
type RecentIntelligence = { id: string; title: string; source_id: string; severity: string; education_relevance: number; review_status: string; discovered_at: string };
type CommandCenterSnapshot = { data_state: 'available' | 'unavailable'; recent_intelligence: RecentIntelligence[] };

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

function mappingId(node: Node) { return node.id.startsWith('opencti:') ? node.id.slice('opencti:'.length) : null; }

export function OpenCTIGraphWorkspace() {
  const initialItem = useMemo(() => new URLSearchParams(window.location.search).get('item') ?? '', []);
  const [capability, setCapability] = useState<Capability | null>(null);
  const [roots, setRoots] = useState<RecentIntelligence[]>([]);
  const [rootsState, setRootsState] = useState<'loading' | 'available' | 'empty' | 'error'>('loading');
  const [rootsError, setRootsError] = useState<string | null>(null);
  const [populationRefresh, setPopulationRefresh] = useState(0);
  const [itemId, setItemId] = useState(initialItem);
  const [graph, setGraph] = useState<Graph | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [detailError, setDetailError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    json<Capability>('/api/v1/opencti/capabilities').then(setCapability).catch(() => setCapability(null));
    let active = true;
    setRootsState('loading');
    setRootsError(null);
    void json<CommandCenterSnapshot>('/api/v1/command-center').then((snapshot) => {
      if (!active) return;
      if (snapshot.data_state !== 'available') { setRoots([]); setRootsState('error'); setRootsError('Canonical DTMO persistence is unavailable'); return; }
      setRoots(snapshot.recent_intelligence);
      setRootsState(snapshot.recent_intelligence.length ? 'available' : 'empty');
    }).catch((reason) => {
      if (!active) return;
      setRoots([]); setRootsState('error'); setRootsError(reason instanceof Error ? reason.message : 'Canonical graph roots unavailable');
    });
    return () => { active = false; };
  }, [populationRefresh]);

  async function loadGraphFor(id: string) {
    const normalized = id.trim();
    if (!normalized) return;
    setItemId(normalized); setLoading(true); setError(null); setSelected(null); setDetailError(null);
    try {
      const data = await json<Graph>(`/api/v1/opencti/items/${encodeURIComponent(normalized)}/graph`);
      setGraph(data);
      const url = new URL(window.location.href); url.searchParams.set('item', normalized); window.history.replaceState({}, '', url);
    } catch (reason) {
      setGraph(null); setError(reason instanceof Error ? reason.message : 'Graph could not be loaded');
    } finally { setLoading(false); }
  }

  async function loadGraph(event?: FormEvent) { event?.preventDefault(); await loadGraphFor(itemId); }

  async function loadEntity(node: Node) {
    const id = mappingId(node); if (!id) return;
    setDetailError(null);
    try { setSelected(await json<Entity>(`/api/v1/opencti/entities/${encodeURIComponent(id)}`)); }
    catch (reason) { setSelected(null); setDetailError(reason instanceof Error ? reason.message : 'Entity detail could not be loaded'); }
  }

  useEffect(() => { if (initialItem) void loadGraphFor(initialItem); }, []); // intentional one-shot deep link

  const entityNodes = graph?.nodes.filter((node) => node.kind === 'opencti-entity') ?? [];
  const radius = 150; const center = 190;

  return (
    <section className="opencti-workspace" aria-labelledby="workspace-title">
      <header className="workspace-heading graph-heading">
        <div><p className="eyebrow">Unified Operations Workbench · Intelligence</p><h1 id="workspace-title">Knowledge Graph</h1><p>Discover canonical intelligence roots and inspect persisted OpenCTI/STIX context, provenance and revisions without knowing an internal UUID.</p></div>
        <div className="heading-statuses"><span className="phase-badge">11.10q Functional recovery</span><span className="phase-badge available">Read-only evidence</span></div>
      </header>

      <section className="graph-capability surface" aria-label="OpenCTI capability state">
        <div><span>Feature</span><strong>{capability?.enabled ? 'enabled' : 'disabled / unknown'}</strong></div><div><span>Configuration</span><strong>{capability?.configured ? 'configured' : 'not established'}</strong></div><div><span>Runtime health</span><strong>not inferred</strong></div><div><span>Relationship topology</span><strong>{capability?.upstream_relationship_topology_persisted ? 'persisted' : 'not persisted'}</strong></div>
      </section>

      <section className="surface" aria-label="Discoverable graph roots">
        <header><div><p className="eyebrow">Canonical discovery</p><h2>Recent intelligence roots</h2></div><span className="evidence-label">{rootsState === 'loading' ? 'Loading…' : `${roots.length} available`}</span></header>
        {rootsState === 'loading' && <p className="panel-state">Loading canonical graph roots…</p>}
        {rootsState === 'empty' && <>
          <div className="graph-empty"><strong>No canonical intelligence roots recorded yet</strong><p>Use an already-enabled governed source below. After ingestion, reload canonical graph roots without leaving this workspace.</p></div>
          <ThreatIntelligencePopulation onPopulated={() => setPopulationRefresh((current) => current + 1)} />
        </>}
        {rootsState === 'error' && <div className="panel-state error-state"><strong>Graph root discovery unavailable</strong><span>{rootsError}. No upstream-health or absence conclusion is inferred.</span></div>}
        {rootsState === 'available' && <div className="entity-list" aria-label="Recent canonical graph roots">{roots.map((root) => <button type="button" className="entity-row" key={root.id} onClick={() => void loadGraphFor(root.id)} aria-pressed={itemId === root.id}><span><strong>{root.title}</strong><small>{root.source_id} · {root.severity} · discovered {new Date(root.discovered_at).toLocaleString()}</small></span><span><small>education relevance</small><strong>{root.education_relevance}</strong></span></button>)}</div>}
        <p className="boundary-copy">Roots are discovered from canonical DTMO persistence. Selecting a root reads only DTMO-persisted graph mappings; the browser does not query OpenCTI directly. Population can execute only an already-enabled governed source and does not change source activation, endpoints or credentials.</p>
      </section>

      <details className="surface graph-loader"><summary>Advanced: open a known canonical item ID</summary><form onSubmit={loadGraph}><label htmlFor="graph-item">Canonical DTMO item UUID</label><div><input id="graph-item" value={itemId} onChange={(event) => setItemId(event.target.value)} placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" required /><button type="submit" disabled={loading}>{loading ? 'Loading…' : 'Load graph context'}</button></div><small>Secondary deep-link/troubleshooting path only. Normal operator discovery is provided above.</small></form></details>

      {error && <div className="panel-state error-state"><strong>Graph context unavailable</strong><span>{error}</span></div>}
      {graph && <><div className="graph-layout"><article className="surface graph-canvas-card"><header><div><p className="eyebrow">Persisted projection</p><h2>{graph.title}</h2></div><span className="evidence-label">{entityNodes.length} OpenCTI mappings</span></header>
        {entityNodes.length === 0 ? <div className="graph-empty"><strong>No persisted OpenCTI mapping context</strong><p>This is an attributable empty state for this canonical item; it is not evidence that OpenCTI has no related knowledge.</p></div> : <svg className="graph-svg" viewBox="0 0 380 380" role="img" aria-label="DTMO canonical item with persisted OpenCTI mapping nodes">{entityNodes.map((node,index)=>{const angle=(Math.PI*2*index)/Math.max(entityNodes.length,1)-Math.PI/2;const x=center+radius*Math.cos(angle);const y=center+radius*Math.sin(angle);return <line key={`edge-${node.id}`} x1={center} y1={center} x2={x} y2={y} className="graph-edge"/>})}<circle cx={center} cy={center} r="54" className="graph-root"/><text x={center} y={center-5} textAnchor="middle" className="graph-root-label">DTMO</text><text x={center} y={center+14} textAnchor="middle" className="graph-root-sub">canonical</text>{entityNodes.map((node,index)=>{const angle=(Math.PI*2*index)/Math.max(entityNodes.length,1)-Math.PI/2;const x=center+radius*Math.cos(angle);const y=center+radius*Math.sin(angle);return <g key={node.id} role="button" tabIndex={0} aria-label={`Open ${node.entity_type} ${node.stix_id ?? ''}`} onClick={()=>void loadEntity(node)} onKeyDown={(event)=>{if(event.key==='Enter'||event.key===' ')void loadEntity(node)}}><circle cx={x} cy={y} r="34" className="graph-node"/><text x={x} y={y-3} textAnchor="middle" className="graph-node-label">{node.entity_type.slice(0,12)}</text><text x={x} y={y+13} textAnchor="middle" className="graph-node-sub">{node.confidence ?? '—'}%</text></g>})}</svg>}
        <p className="boundary-copy"><strong>Topology boundary:</strong> {graph.topology_scope}. OpenCTI entity-to-entity relationships are not drawn unless they are durably persisted by DTMO.</p></article><article className="surface entity-list-card"><header><div><p className="eyebrow">Entities</p><h2>Attributed mappings</h2></div></header><div className="entity-list">{entityNodes.map((node)=><button type="button" key={node.id} onClick={()=>void loadEntity(node)} className="entity-row"><span><strong>{node.entity_type}</strong><small>{node.stix_id}</small></span><span><small>confidence</small><strong>{node.confidence ?? '—'}</strong></span></button>)}{!entityNodes.length&&<p className="panel-state">No entity mappings recorded for this item.</p>}</div></article></div><article className="surface graph-evidence"><div><p className="eyebrow">Evidence boundary</p><h2>Graph presence is context, not a verdict</h2></div><p>{graph.evidence_boundary}</p></article></>}

      {detailError && <div className="panel-state error-state"><strong>Entity detail unavailable</strong><span>{detailError}</span></div>}
      {selected && <article className="surface entity-detail"><header><div><p className="eyebrow">OpenCTI entity evidence</p><h2>{selected.entity_type}</h2><p>{selected.stix_id}</p></div><span className="evidence-label">{selected.revisions.length} revisions</span></header><div className="detail-grid"><div><span>OpenCTI ID</span><strong>{selected.opencti_id}</strong></div><div><span>Confidence</span><strong>{selected.confidence ?? 'unknown'}</strong></div><div><span>External sharing</span><strong>{selected.external_share_authorized ? 'authorized' : 'not authorized'}</strong></div><div><span>Local compromise</span><strong>{selected.local_compromise_proven ? 'proven' : 'not proven'}</strong></div><div><span>Last persisted observation</span><strong>{new Date(selected.last_seen_at).toLocaleString()}</strong></div><div><span>Snapshot</span><strong className="mono">{selected.snapshot_hash.slice(0,16)}…</strong></div></div><div className="entity-detail-columns"><section><h3>Markings</h3>{selected.markings.length?selected.markings.map((marking,index)=><code key={index}>{String(marking.definition ?? marking.id ?? 'marking')}</code>):<p>No persisted markings.</p>}</section><section><h3>External references</h3>{selected.external_references.length?selected.external_references.map((reference,index)=><p key={index}>{String(reference.source_name ?? 'reference')} · {String(reference.external_id ?? reference.url ?? '')}</p>):<p>No persisted external references.</p>}</section><section><h3>Revision history</h3>{selected.revisions.length?selected.revisions.map((revision)=><p key={revision.id}><time>{new Date(revision.recorded_at).toLocaleString()}</time> · <span className="mono">{revision.snapshot_hash.slice(0,12)}…</span></p>):<p>No revision snapshots.</p>}</section></div><p className="boundary-copy">{selected.evidence_boundary}</p></article>}
    </section>
  );
}
