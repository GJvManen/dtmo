import { useEffect, useMemo, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { NavLink, Navigate, Route, Routes, useLocation, useNavigate } from 'react-router-dom';

import { AdministrationWorkspace } from './AdministrationWorkspace';
import { AnalysisWorkspace } from './AnalysisWorkspace';
import { AutomationWorkspace } from './AutomationWorkspace';
import { CollectionWorkspace } from './CollectionWorkspace';
import { ExposureWorkspace } from './ExposureWorkspace';
import { GovernanceWorkspace } from './GovernanceWorkspace';
import { InvestigationsWorkspace } from './InvestigationsWorkspace';
import { IocExplorerWorkspace } from './IocExplorerWorkspace';
import { MispSharingWorkspace } from './MispSharingWorkspace';
import { OpenCTIGraphWorkspace } from './OpenCTIGraphWorkspace';
import { OperationsWorkspace } from './OperationsWorkspace';
import { UnifiedIntelligenceWorkspace } from './UnifiedIntelligenceWorkspace';

type Health = {
  status: string;
  version: string;
  environment: string;
  publication_gate: string;
  authentication: string;
};

type Session = {
  subject: string;
  roles: string[];
  permissions: string[];
};

type CommandMetric = {
  id: string;
  label: string;
  value: number | null;
  tone: 'neutral' | 'critical' | 'warning' | 'accent';
};

type RecentIntelligence = {
  id: string;
  title: string;
  source_id: string;
  severity: string;
  education_relevance: number;
  review_status: string;
  discovered_at: string;
};

type IntegrationCapability = {
  id: string;
  label: string;
  state: string;
  enabled: boolean;
  configured: boolean;
  scheduled_collection: boolean;
  runtime_observation: string | null;
  last_observed_at: string | null;
  runtime_health_claim: boolean;
};

type IntelligenceTrendPoint = {
  date: string;
  count: number;
};

type SeverityDistributionPoint = {
  severity: string;
  count: number;
};

type CommandCenterSnapshot = {
  generated_at: string;
  data_state: 'available' | 'unavailable';
  metrics: CommandMetric[];
  recent_intelligence: RecentIntelligence[];
  trends?: {
    intelligence_7d: IntelligenceTrendPoint[];
    severity_distribution: SeverityDistributionPoint[];
  };
  integrations: IntegrationCapability[];
  evidence_boundary: string;
};

type WorkspaceDefinition = {
  path: string;
  label: string;
  group: string;
  icon: string;
  title: string;
  description: string;
  delivery: string;
};

const workspaces: WorkspaceDefinition[] = [
  { path: '/command-center', label: 'Command Center', group: 'Home', icon: '⌂', title: 'Command Center', description: 'Canonical operational landing workspace.', delivery: 'Command Center is delivered in Phase 11.10c.' },
  { path: '/intelligence', label: 'Threat Intelligence', group: 'Intelligence', icon: '◎', title: 'Threat Intelligence', description: 'Canonical intelligence workspace and object navigation.', delivery: 'Unified intelligence content is delivered in Phase 11.10d.' },
  { path: '/intelligence/iocs', label: 'IOC Explorer', group: 'Intelligence', icon: '◇', title: 'IOC Explorer', description: 'IOC-oriented route within the canonical intelligence workspace.', delivery: 'IOC feature content is delivered with the unified intelligence workspace.' },
  { path: '/intelligence/graph', label: 'Knowledge Graph', group: 'Intelligence', icon: '⌘', title: 'Knowledge Graph', description: 'Graph route governed by DTMO API and provenance boundaries.', delivery: 'OpenCTI graph/entity content is delivered in Phase 11.10f.' },
  { path: '/exposure', label: 'Exposure', group: 'Exposure', icon: '△', title: 'Exposure', description: 'Vulnerability, asset and prioritization workspace foundation.', delivery: 'Exposure feature content is delivered in Phase 11.10i.' },
  { path: '/investigations', label: 'Investigations', group: 'Investigations', icon: '▣', title: 'Investigations', description: 'Cases, alerts, tasks and timeline workspace foundation.', delivery: 'TheHive investigation and case content is delivered in Phase 11.10h.' },
  { path: '/analysis', label: 'Analysis & Enrichment', group: 'Analysis', icon: '⌁', title: 'Analysis & Enrichment', description: 'Governed IntelOwl enrichment and Cortex analyzer workspace.', delivery: 'IntelOwl and Cortex analysis content is delivered in Phase 11.10e.' },
  { path: '/sharing', label: 'Sharing & Exchange', group: 'Sharing', icon: '⇄', title: 'Sharing & Exchange', description: 'Human-governed MISP review, approval and unpublished export workflow.', delivery: 'MISP exchange content is delivered in Phase 11.10g.' },
  { path: '/automation', label: 'Automation & Playbooks', group: 'Automation', icon: '↯', title: 'Automation & Playbooks', description: 'Playbooks, jobs, schedules and approval workspace foundation.', delivery: 'Automation feature content is delivered in Phase 11.10k.' },
  { path: '/collection', label: 'Collection', group: 'Collection', icon: '↓', title: 'Collection', description: 'Sources, connectors, catalog and collection-run workspace foundation.', delivery: 'Collection control-center content is delivered in Phase 11.10j.' },
  { path: '/governance', label: 'Governance & Evidence', group: 'Governance', icon: '✓', title: 'Governance & Evidence', description: 'Framework, mapping, evidence, risk and audit workspace foundation.', delivery: 'Governance and evidence content is delivered in Phase 11.10l.' },
  { path: '/operations', label: 'Operations', group: 'Operations', icon: '◫', title: 'Operations', description: 'System health, observability, runtime and recovery workspace foundation.', delivery: 'Operations content is delivered in Phase 11.10m.' },
  { path: '/administration', label: 'Administration', group: 'Administration', icon: '⚙', title: 'Administration', description: 'Users, roles, policies and governed configuration workspace foundation.', delivery: 'Administration content is delivered in Phase 11.10m.' },
];

const groups = [...new Set(workspaces.map((workspace) => workspace.group))];

async function fetchJson<T>(url: string): Promise<T> {
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
    const detail = typeof body === 'object' && body !== null && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

function useShellStatus() {
  const health = useQuery({ queryKey: ['shell', 'health'], queryFn: () => fetchJson<Health>('/health'), refetchInterval: 60_000 });
  const session = useQuery({ queryKey: ['shell', 'session'], queryFn: () => fetchJson<Session>('/api/v1/ui/session'), retry: false });
  return { health, session };
}

function severityLabel(value: string) {
  if (value === 'critical') return 'Critical';
  if (value === 'high') return 'High';
  if (value === 'medium') return 'Medium';
  if (value === 'low') return 'Low';
  return 'Informational';
}

function relativeTime(value: string | null) {
  if (!value) return 'No runtime observation';
  const delta = Date.now() - new Date(value).getTime();
  if (!Number.isFinite(delta) || delta < 0) return new Date(value).toLocaleString();
  const minutes = Math.floor(delta / 60_000);
  if (minutes < 1) return 'just now';
  if (minutes < 60) return `${minutes} min ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} h ago`;
  return `${Math.floor(hours / 24)} d ago`;
}

function CommandCenter({ session, health }: { session?: Session; health?: Health }) {
  const snapshot = useQuery({
    queryKey: ['command-center'],
    queryFn: () => fetchJson<CommandCenterSnapshot>('/api/v1/command-center'),
    retry: false,
    refetchInterval: 60_000,
  });
  const permissions = new Set(session?.permissions ?? []);
  const quickActions = [
    { label: 'Threat Intelligence', detail: 'Search and investigate canonical intelligence.', path: '/intelligence', permission: 'read:intelligence', icon: '◎' },
    { label: 'Review queue', detail: 'Continue governed intelligence review.', path: '/intelligence', permission: 'review:intelligence', icon: '✓' },
    { label: 'Collection control', detail: 'Manage sources and connector execution.', path: '/collection', permission: 'manage:connectors', icon: '↓' },
    { label: 'Investigations', detail: 'Prepare or continue case handoff workflows.', path: '/investigations', permission: 'handoff:case', icon: '▣' },
    { label: 'Sharing approvals', detail: 'Open the human-governed sharing workspace.', path: '/sharing', permission: 'approve:share', icon: '⇄' },
    { label: 'Administration', detail: 'Manage identities, roles and policies.', path: '/administration', permission: 'manage:users', icon: '⚙' },
  ].filter((item) => permissions.has(item.permission));
  const data = snapshot.data;
  const canonicalDataAvailable = !snapshot.isError && data?.data_state === 'available';
  const enabledIntegrations = data?.integrations.filter((item) => item.enabled).length ?? 0;
  const configurationRequired = data?.integrations.filter((item) => item.state === 'configuration-required').length ?? 0;
  const observedIntegrations = data?.integrations.filter((item) => item.runtime_observation !== null).length ?? 0;
  const trendPoints = data?.trends?.intelligence_7d ?? [];
  const severityPoints = data?.trends?.severity_distribution ?? [];
  const trendMax = Math.max(1, ...trendPoints.map((point) => point.count));
  const severityMax = Math.max(1, ...severityPoints.map((point) => point.count));

  return (
    <section className="command-center" aria-labelledby="workspace-title">
      <header className="workspace-heading command-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Command Center</h1>
          <p>Attributable operational overview of canonical DTMO intelligence, governed workload and integration capability.</p>
        </div>
        <div className="heading-statuses">
          <span className="phase-badge">11.10c Command Center · 11.10q recovery</span>
          <span className={`phase-badge ${canonicalDataAvailable ? 'available' : 'unavailable'}`}>{canonicalDataAvailable ? 'Canonical data available' : 'Canonical data unavailable'}</span>
        </div>
      </header>

      <section className="kpi-grid" aria-label="Operational KPIs">
        {(data?.metrics ?? Array.from({ length: 6 }, (_, index) => ({ id: `loading-${index}`, label: 'Loading metric', value: null, tone: 'neutral' as const }))).map((metric) => (
          <article className={`kpi-card tone-${metric.tone}`} key={metric.id}>
            <p>{metric.label}</p>
            <strong>{metric.value === null ? '—' : metric.value.toLocaleString()}</strong>
            <span>{metric.value === null ? 'No attributable value' : 'Canonical DTMO store'}</span>
          </article>
        ))}
      </section>

      <div className="command-grid">
        <article className="surface command-panel threat-panel">
          <header className="panel-heading">
            <div><p className="eyebrow">Threat picture</p><h2>Recent intelligence</h2></div>
            <NavLink className="text-link" to="/intelligence">Open workspace →</NavLink>
          </header>
          {snapshot.isPending && <p className="panel-state">Loading canonical intelligence…</p>}
          {(snapshot.isError || data?.data_state === 'unavailable') && <div className="panel-state error-state"><strong>Canonical store unavailable</strong><span>No threat counts or recent intelligence are synthesized while the canonical datastore cannot be observed.</span></div>}
          {canonicalDataAvailable && !data?.recent_intelligence.length && <p className="panel-state">No canonical intelligence objects are currently recorded.</p>}
          {canonicalDataAvailable && Boolean(data?.recent_intelligence.length) && (
            <div className="intel-list">
              {data?.recent_intelligence.map((item) => (
                <div className="intel-row" key={item.id}>
                  <span className={`severity-dot severity-${item.severity}`} aria-label={severityLabel(item.severity)} />
                  <div className="intel-copy"><strong>{item.title}</strong><span>{item.source_id} · relevance {item.education_relevance} · {item.review_status}</span></div>
                  <time dateTime={item.discovered_at}>{relativeTime(item.discovered_at)}</time>
                </div>
              ))}
            </div>
          )}
        </article>

        <article className="surface command-panel integration-panel">
          <header className="panel-heading">
            <div><p className="eyebrow">Integration readiness</p><h2>{enabledIntegrations}/{data?.integrations.length ?? 6} enabled</h2><small>{configurationRequired} configuration required · {observedIntegrations} runtime observed</small></div>
            <NavLink className="text-link" to="/administration">Open administration →</NavLink>
          </header>
          {snapshot.isPending && <p className="panel-state">Loading integration capability…</p>}
          {snapshot.isError && <p className="panel-state error-state">Integration capability could not be loaded.</p>}
          {data && (
            <div className="integration-list">
              {data.integrations.map((integration) => (
                <div className="integration-row" key={integration.id}>
                  <span className={`integration-state state-${integration.state}`} aria-hidden="true" />
                  <div><strong>{integration.label}</strong><span>{integration.state.replaceAll('-', ' ')} · {integration.runtime_observation ? `observed ${integration.runtime_observation}` : 'runtime not observed'}</span></div>
                  <div className="integration-meta"><time>{relativeTime(integration.last_observed_at)}</time><NavLink className="integration-pivot" to={integration.state === 'configuration-required' ? '/administration' : '/collection'}>{integration.state === 'configuration-required' ? 'Configure' : 'Inspect collection'}</NavLink></div>
                </div>
              ))}
            </div>
          )}
          <p className="boundary-copy">Enabled and configured are capability states only. Runtime observation is historical evidence and is never promoted to a health claim.</p>
        </article>

        <article className="surface command-panel trend-panel">
          <header className="panel-heading"><div><p className="eyebrow">Canonical trend</p><h2>Intelligence arrivals · 7 days</h2></div><NavLink className="text-link" to="/intelligence">Investigate →</NavLink></header>
          {!canonicalDataAvailable && <p className="panel-state">Trend unavailable while canonical intelligence cannot be observed.</p>}
          {canonicalDataAvailable && !trendPoints.length && <p className="panel-state">No attributable trend series is available.</p>}
          {canonicalDataAvailable && Boolean(trendPoints.length) && <div className="trend-chart" role="list" aria-label="Canonical intelligence arrivals over seven days">
            {trendPoints.map((point) => <div className="trend-column" role="listitem" key={point.date} aria-label={`${point.date}: ${point.count} intelligence objects`}><strong>{point.count}</strong><div className="trend-track"><span style={{ height: `${Math.max(4, (point.count / trendMax) * 100)}%` }} /></div><time dateTime={point.date}>{new Date(`${point.date}T00:00:00Z`).toLocaleDateString(undefined, { weekday: 'short' })}</time></div>)}
          </div>}
        </article>

        <article className="surface command-panel severity-panel">
          <header className="panel-heading"><div><p className="eyebrow">Canonical distribution</p><h2>Severity composition</h2></div><span className="evidence-label">Current store</span></header>
          {!canonicalDataAvailable && <p className="panel-state">Severity distribution unavailable.</p>}
          {canonicalDataAvailable && Boolean(severityPoints.length) && <div className="severity-bars" role="list" aria-label="Canonical intelligence severity distribution">
            {severityPoints.map((point) => <div className="severity-bar" role="listitem" key={point.severity}><div><span className={`severity-dot severity-${point.severity}`} aria-hidden="true" /><strong>{severityLabel(point.severity)}</strong><span>{point.count}</span></div><div className="severity-track"><span className={`severity-fill severity-${point.severity}`} style={{ width: `${Math.max(2, (point.count / severityMax) * 100)}%` }} /></div></div>)}
          </div>}
        </article>

        <article className="surface command-panel quick-panel">
          <header className="panel-heading"><div><p className="eyebrow">Role-aware access</p><h2>Quick actions</h2></div><span className="evidence-label">Visibility ≠ authority</span></header>
          {!session && <p className="panel-state">No authorized session context available.</p>}
          {session && !quickActions.length && <p className="panel-state">No quick actions are exposed for this principal.</p>}
          <div className="quick-grid">
            {quickActions.map((action) => (
              <NavLink className="quick-action" to={action.path} key={action.label}>
                <span aria-hidden="true">{action.icon}</span><div><strong>{action.label}</strong><small>{action.detail}</small></div>
              </NavLink>
            ))}
          </div>
        </article>

        <article className="surface command-panel workflow-panel">
          <header className="panel-heading"><div><p className="eyebrow">Operational flow</p><h2>Governed CTI lifecycle</h2></div><span className={`status-chip ${health?.status === 'healthy' ? 'success' : 'neutral'}`}><span className="status-dot" />{health?.status ?? 'unknown'}</span></header>
          <div className="workflow-strip" aria-label="Collect enrich analyze investigate respond learn">
            {['Collect', 'Enrich', 'Analyze', 'Investigate', 'Respond', 'Learn'].map((step, index) => <div key={step}><span>{index + 1}</span><strong>{step}</strong></div>)}
          </div>
          <p className="boundary-copy">Command Center is read-only. Review, sharing, case mutation, connector execution and administration remain separate server-authorized actions in their governed workspaces.</p>
        </article>
      </div>

      <article className="surface evidence-surface">
        <div><p className="eyebrow">Evidence boundary</p><h2>Operational visibility without synthetic claims</h2></div>
        <p>{data?.evidence_boundary ?? 'Command Center never converts missing evidence into a healthy, zero-risk or production-ready claim.'}</p>
      </article>
    </section>
  );
}

function WorkspaceFoundation({ workspace }: { workspace: WorkspaceDefinition }) {
  if (workspace.path === '/administration') return <AdministrationWorkspace />;
  if (workspace.path === '/automation') return <AutomationWorkspace />;
  if (workspace.path === '/collection') return <CollectionWorkspace />;
  if (workspace.path === '/exposure') return <ExposureWorkspace />;
  if (workspace.path === '/governance') return <GovernanceWorkspace />;
  if (workspace.path === '/investigations') return <InvestigationsWorkspace />;
  if (workspace.path === '/operations') return <OperationsWorkspace />;
  if (workspace.path === '/sharing') return <MispSharingWorkspace />;
  return (
    <section className="workspace-foundation" aria-labelledby="workspace-title">
      <header className="workspace-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">{workspace.title}</h1>
          <p>{workspace.description}</p>
        </div>
        <span className="phase-badge">11.10b shell foundation</span>
      </header>
      <div className="foundation-grid">
        <article className="surface welcome-surface"><span className="surface-icon" aria-hidden="true">{workspace.icon}</span><div><h2>Workspace route ready</h2><p>{workspace.delivery}</p></div></article>
        <article className="surface boundary-surface"><p className="eyebrow">Evidence boundary</p><h2>No synthetic operational state</h2><p>This shell deliberately does not fabricate intelligence, incidents, vulnerabilities, cases, connector health or approval state. Feature data appears only when its governed DTMO API contract is implemented in the corresponding bounded slice.</p></article>
      </div>
      <article className="surface compatibility-surface"><div><p className="eyebrow">Migration compatibility</p><h2>Existing console remains available during bounded migration</h2><p>Legacy views remain compatibility paths while capabilities are migrated. They are not parallel targets for new feature development.</p></div><a className="button secondary" href="/ui/console">Open compatibility console</a></article>
    </section>
  );
}

function Navigation({ open, onNavigate }: { open: boolean; onNavigate: () => void }) {
  return (
    <aside className={`primary-nav ${open ? 'open' : ''}`} aria-label="Primaire navigatie">
      <div className="brand-block"><div className="brand-mark" aria-hidden="true">D</div><div><strong>DTMO</strong><span>Unified Operations</span></div></div>
      <nav aria-label="Werkruimten">
        {groups.map((group) => <div className="nav-group" key={group}><p>{group}</p>{workspaces.filter((workspace) => workspace.group === group).map((workspace) => <NavLink key={workspace.path} to={workspace.path} onClick={onNavigate} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}><span className="nav-icon" aria-hidden="true">{workspace.icon}</span><span>{workspace.label}</span></NavLink>)}</div>)}
      </nav>
      <div className="nav-footer"><a href="/docs">API documentation</a></div>
    </aside>
  );
}

function CommandPalette({ open, onClose }: { open: boolean; onClose: () => void }) {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  const results = useMemo(() => workspaces.filter((item) => `${item.label} ${item.group}`.toLowerCase().includes(query.trim().toLowerCase())), [query]);
  useEffect(() => { if (open) { setQuery(''); window.setTimeout(() => inputRef.current?.focus(), 0); } }, [open]);
  if (!open) return null;
  return (
    <div className="palette-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <section className="command-palette" role="dialog" aria-modal="true" aria-labelledby="palette-title">
        <header><div><p className="eyebrow">Navigation only</p><h2 id="palette-title">Command palette</h2></div><button type="button" className="icon-button" onClick={onClose} aria-label="Sluiten">×</button></header>
        <label className="sr-only" htmlFor="palette-query">Zoek werkruimte</label><input ref={inputRef} id="palette-query" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Ga naar werkruimte…" autoComplete="off" />
        <div className="palette-results">{results.map((item) => <button key={item.path} type="button" onClick={() => { navigate(item.path); onClose(); }}><span aria-hidden="true">{item.icon}</span><span><strong>{item.label}</strong><small>{item.group}</small></span></button>)}{!results.length && <p className="empty-message">Geen werkruimte gevonden.</p>}</div>
        <footer>Navigation is safe convenience only. Governed mutations remain in server-authorized APIs.</footer>
      </section>
    </div>
  );
}

function ContextRail({ open, onClose }: { open: boolean; onClose: () => void }) {
  return (
    <aside className={`context-rail ${open ? 'open' : ''}`} aria-label="Objectcontext">
      <header><div><p className="eyebrow">Context</p><h2>Object details</h2></div><button type="button" className="icon-button" onClick={onClose} aria-label="Context sluiten">×</button></header>
      <div className="context-empty"><span aria-hidden="true">◇</span><h3>Geen object geselecteerd</h3><p>De context rail toont alleen attributable canonical data nadat een feature-workspace een object selecteert. Ontbrekende feiten worden niet afgeleid uit een geconfigureerde integratie.</p></div>
    </aside>
  );
}

export function App() {
  const location = useLocation();
  const { health, session } = useShellStatus();
  const [navOpen, setNavOpen] = useState(false);
  const [contextOpen, setContextOpen] = useState(false);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [theme, setTheme] = useState<'dark' | 'light'>(() => (localStorage.getItem('dtmo-workbench-theme') === 'light' ? 'light' : 'dark'));

  useEffect(() => { document.documentElement.dataset.theme = theme; localStorage.setItem('dtmo-workbench-theme', theme); }, [theme]);
  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); setPaletteOpen(true); }
      if (event.key === 'Escape') { setPaletteOpen(false); setNavOpen(false); }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);
  useEffect(() => setNavOpen(false), [location.pathname]);

  const healthLabel = health.isPending ? 'Status controleren' : health.isError ? 'Platformstatus onbekend' : `${health.data?.environment ?? 'unknown'} · ${health.data?.status ?? 'unknown'}`;
  const principalLabel = session.isPending ? 'Principal controleren' : session.isError ? 'Geen geautoriseerde sessie' : `${session.data?.subject} · ${session.data?.roles.join(', ') || 'geen rollen'}`;

  return (
    <div className={`app-shell ${contextOpen ? 'with-context' : ''}`}>
      <a className="skip-link" href="#main-workspace">Ga naar hoofdinhoud</a>
      <Navigation open={navOpen} onNavigate={() => setNavOpen(false)} />
      <div className="app-main">
        <header className="topbar">
          <div className="topbar-start"><button className="icon-button mobile-only" type="button" onClick={() => setNavOpen((value) => !value)} aria-label="Navigatie openen" aria-expanded={navOpen}>☰</button><div><p className="eyebrow">Dutch Threat Monitoring for Education</p><strong>Operations Workbench</strong></div></div>
          <div className="topbar-center"><button type="button" className="command-trigger" onClick={() => setPaletteOpen(true)}><span aria-hidden="true">⌕</span><span>Zoek of navigeer</span><kbd>Ctrl K</kbd></button></div>
          <div className="topbar-actions"><span className={`status-chip ${health.isError ? 'error' : health.data?.status === 'healthy' ? 'success' : 'neutral'}`} role="status"><span className="status-dot" />{healthLabel}</span><button type="button" className="icon-button" onClick={() => setContextOpen((value) => !value)} aria-label="Objectcontext wisselen" aria-expanded={contextOpen}>◇</button><button type="button" className="icon-button" onClick={() => setTheme((value) => value === 'dark' ? 'light' : 'dark')} aria-label="Thema wisselen">{theme === 'dark' ? '☀' : '☾'}</button></div>
        </header>
        <div className="identity-strip" aria-live="polite"><span>{principalLabel}</span><span>Publication/share authority remains server-side and human-governed.</span></div>
        <main id="main-workspace" className="workspace">
          <Routes>
            <Route path="/" element={<Navigate to="/command-center" replace />} />
            <Route path="/command-center/*" element={<CommandCenter session={session.data} health={health.data} />} />
            <Route path="/intelligence" element={<UnifiedIntelligenceWorkspace />} />
            <Route path="/intelligence/iocs" element={<IocExplorerWorkspace />} />
            <Route path="/intelligence/graph" element={<OpenCTIGraphWorkspace />} />
            <Route path="/analysis/*" element={<AnalysisWorkspace />} />
            {workspaces.filter((workspace) => !['/command-center', '/intelligence', '/intelligence/iocs', '/intelligence/graph', '/analysis'].includes(workspace.path)).map((workspace) => <Route key={workspace.path} path={`${workspace.path}/*`} element={<WorkspaceFoundation workspace={workspace} />} />)}
            <Route path="*" element={<Navigate to="/command-center" replace />} />
          </Routes>
        </main>
      </div>
      <ContextRail open={contextOpen} onClose={() => setContextOpen(false)} />
      <CommandPalette open={paletteOpen} onClose={() => setPaletteOpen(false)} />
    </div>
  );
}
