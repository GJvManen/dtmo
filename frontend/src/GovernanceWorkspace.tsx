import { useQuery } from '@tanstack/react-query';

type Framework = { id: string; name: string; kind: string; coverage: string; coverage_label: string; mapping_ids: string[]; note: string; provenance: string[] };
type Mapping = { id: string; title: string; statement: string; source: string; section: string };
type GovernanceSnapshot = { status: string; frameworks: Framework[]; mappings: Mapping[]; authority_boundaries: string[]; claim_boundary: string };

async function readGovernance(): Promise<GovernanceSnapshot> {
  const response = await fetch('/api/v1/governance/knowledge', { credentials: 'same-origin', headers: { Accept: 'application/json' } });
  const body = await response.json().catch(() => null);
  if (!response.ok) throw new Error(typeof body === 'object' && body && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`);
  return body as GovernanceSnapshot;
}

export function GovernanceWorkspace() {
  const snapshot = useQuery({ queryKey: ['governance', 'knowledge'], queryFn: readGovernance, retry: false });
  const data = snapshot.data;
  return (
    <section className="workspace-foundation" aria-labelledby="workspace-title">
      <header className="workspace-heading"><div><p className="eyebrow">Unified Operations Workbench</p><h1 id="workspace-title">Governance & Evidence</h1><p>Repository-backed frameworks, mappings, provenance and authority boundaries without inferred compliance.</p></div><div className="heading-statuses"><span className="phase-badge">11.10l Governance & Evidence</span><span className="evidence-label">Mapping visibility ≠ compliance approval</span></div></header>
      {snapshot.isPending && <p className="panel-state">Loading canonical governance knowledge…</p>}
      {snapshot.isError && <article className="surface panel-state error-state"><strong>Governance evidence unavailable</strong><span>No framework coverage, control equivalence or compliance state is inferred while canonical governance knowledge is unavailable.</span></article>}
      {data && <>
        <div className="command-grid">
          <article className="surface command-panel"><header className="panel-heading"><div><p className="eyebrow">Frameworks</p><h2>Explicit coverage state</h2></div><span className="evidence-label">No inferred crosswalks</span></header><div className="integration-list">{data.frameworks.map((item) => <div className="integration-row" key={item.id}><span className={`integration-state state-${item.coverage === 'mapped_internal' ? 'enabled' : 'disabled'}`} aria-hidden="true" /><div><strong>{item.name}</strong><span>{item.coverage_label} · {item.kind}</span><small>{item.note}</small></div></div>)}</div></article>
          <article className="surface command-panel"><header className="panel-heading"><div><p className="eyebrow">Repository mappings</p><h2>Traceable controls</h2></div><span className="evidence-label">Source + section required</span></header><div className="integration-list">{data.mappings.map((item) => <div className="integration-row" key={item.id}><div><strong>{item.title}</strong><span>{item.statement}</span><small>{item.source} · {item.section}</small></div></div>)}</div></article>
          <article className="surface command-panel"><header className="panel-heading"><div><p className="eyebrow">Authority boundaries</p><h2>Separation of duties</h2></div></header><ul>{data.authority_boundaries.map((boundary) => <li key={boundary}>{boundary}</li>)}</ul></article>
        </div>
        <article className="surface evidence-surface"><div><p className="eyebrow">Claim boundary</p><h2>Evidence without synthetic assurance</h2></div><p>{data.claim_boundary}</p><p>Normenkader IBP, MITRE ATT&CK and CVSS remain explicitly unmapped/context-only where repository-backed control or technique mappings do not exist. Visibility does not grant review, share, publication or production authority.</p></article>
      </>}
    </section>
  );
}
