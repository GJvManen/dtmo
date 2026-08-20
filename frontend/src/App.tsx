import { useEffect, useMemo, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { NavLink, Navigate, Route, Routes, useLocation, useNavigate } from 'react-router-dom';

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
  { path: '/command-center', label: 'Command Center', group: 'Home', icon: '⌂', title: 'Command Center', description: 'Canonical operational landing workspace.', delivery: 'Functional command-center content is delivered in Phase 11.10c.' },
  { path: '/intelligence', label: 'Threat Intelligence', group: 'Intelligence', icon: '◎', title: 'Threat Intelligence', description: 'Canonical intelligence workspace and object navigation.', delivery: 'Unified intelligence content is delivered in Phase 11.10d.' },
  { path: '/intelligence/iocs', label: 'IOC Explorer', group: 'Intelligence', icon: '◇', title: 'IOC Explorer', description: 'IOC-oriented route within the canonical intelligence workspace.', delivery: 'IOC feature content is delivered with the unified intelligence workspace.' },
  { path: '/intelligence/graph', label: 'Knowledge Graph', group: 'Intelligence', icon: '⌘', title: 'Knowledge Graph', description: 'Graph route governed by DTMO API and provenance boundaries.', delivery: 'OpenCTI graph/entity content is delivered in Phase 11.10f.' },
  { path: '/exposure', label: 'Exposure', group: 'Exposure', icon: '△', title: 'Exposure', description: 'Vulnerability, asset and prioritization workspace foundation.', delivery: 'Exposure feature content is delivered in Phase 11.10i.' },
  { path: '/investigations', label: 'Investigations', group: 'Investigations', icon: '▣', title: 'Investigations', description: 'Cases, alerts, tasks and timeline workspace foundation.', delivery: 'TheHive investigation and case content is delivered in Phase 11.10h.' },
  { path: '/analysis', label: 'Analysis & Enrichment', group: 'Analysis', icon: '⌁', title: 'Analysis & Enrichment', description: 'Governed analysis and enrichment workspace foundation.', delivery: 'IntelOwl and Cortex analysis content is delivered in Phase 11.10e.' },
  { path: '/sharing', label: 'Sharing & Exchange', group: 'Sharing', icon: '⇄', title: 'Sharing & Exchange', description: 'Governed exchange, publication and approval workspace foundation.', delivery: 'MISP exchange content is delivered in Phase 11.10g.' },
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

function WorkspaceFoundation({ workspace }: { workspace: WorkspaceDefinition }) {
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
        <article className="surface welcome-surface">
          <span className="surface-icon" aria-hidden="true">{workspace.icon}</span>
          <div>
            <h2>Workspace route ready</h2>
            <p>{workspace.delivery}</p>
          </div>
        </article>
        <article className="surface boundary-surface">
          <p className="eyebrow">Evidence boundary</p>
          <h2>No synthetic operational state</h2>
          <p>This shell deliberately does not fabricate intelligence, incidents, vulnerabilities, cases, connector health or approval state. Feature data appears only when its governed DTMO API contract is implemented in the corresponding bounded slice.</p>
        </article>
      </div>
      <article className="surface compatibility-surface">
        <div>
          <p className="eyebrow">Migration compatibility</p>
          <h2>Existing console remains available during bounded migration</h2>
          <p>Legacy views remain compatibility paths while capabilities are migrated. They are not parallel targets for new feature development.</p>
        </div>
        <a className="button secondary" href="/ui/console">Open compatibility console</a>
      </article>
    </section>
  );
}

function Navigation({ open, onNavigate }: { open: boolean; onNavigate: () => void }) {
  return (
    <aside className={`primary-nav ${open ? 'open' : ''}`} aria-label="Primaire navigatie">
      <div className="brand-block">
        <div className="brand-mark" aria-hidden="true">D</div>
        <div><strong>DTMO</strong><span>Unified Operations</span></div>
      </div>
      <nav aria-label="Werkruimten">
        {groups.map((group) => (
          <div className="nav-group" key={group}>
            <p>{group}</p>
            {workspaces.filter((workspace) => workspace.group === group).map((workspace) => (
              <NavLink key={workspace.path} to={workspace.path} onClick={onNavigate} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <span className="nav-icon" aria-hidden="true">{workspace.icon}</span>
                <span>{workspace.label}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </nav>
      <div className="nav-footer">
        <a href="/docs">API documentation</a>
        <a href="/ui/console">Compatibility console</a>
      </div>
    </aside>
  );
}

function CommandPalette({ open, onClose }: { open: boolean; onClose: () => void }) {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  const results = useMemo(() => workspaces.filter((item) => `${item.label} ${item.group}`.toLowerCase().includes(query.trim().toLowerCase())), [query]);

  useEffect(() => {
    if (open) {
      setQuery('');
      window.setTimeout(() => inputRef.current?.focus(), 0);
    }
  }, [open]);

  if (!open) return null;
  return (
    <div className="palette-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <section className="command-palette" role="dialog" aria-modal="true" aria-labelledby="palette-title">
        <header><div><p className="eyebrow">Navigation only</p><h2 id="palette-title">Command palette</h2></div><button type="button" className="icon-button" onClick={onClose} aria-label="Sluiten">×</button></header>
        <label className="sr-only" htmlFor="palette-query">Zoek werkruimte</label>
        <input ref={inputRef} id="palette-query" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Ga naar werkruimte…" autoComplete="off" />
        <div className="palette-results">
          {results.map((item) => <button key={item.path} type="button" onClick={() => { navigate(item.path); onClose(); }}><span aria-hidden="true">{item.icon}</span><span><strong>{item.label}</strong><small>{item.group}</small></span></button>)}
          {!results.length && <p className="empty-message">Geen werkruimte gevonden.</p>}
        </div>
        <footer>Phase 11.10b exposes safe navigation only. Governed actions remain in their feature slices and server-authorized APIs.</footer>
      </section>
    </div>
  );
}

function ContextRail({ open, onClose }: { open: boolean; onClose: () => void }) {
  return (
    <aside className={`context-rail ${open ? 'open' : ''}`} aria-label="Objectcontext">
      <header><div><p className="eyebrow">Context</p><h2>Object details</h2></div><button type="button" className="icon-button" onClick={onClose} aria-label="Context sluiten">×</button></header>
      <div className="context-empty">
        <span aria-hidden="true">◇</span>
        <h3>Geen object geselecteerd</h3>
        <p>De context rail toont alleen attributable canonical data nadat een feature-workspace een object selecteert. Ontbrekende feiten worden niet afgeleid uit een geconfigureerde integratie.</p>
      </div>
    </aside>
  );
}

export function App() {
  const location = useLocation();
  const { health, session } = useShellStatus();
  const [navOpen, setNavOpen] = useState(false);
  const [contextOpen, setContextOpen] = useState(true);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [theme, setTheme] = useState<'dark' | 'light'>(() => (localStorage.getItem('dtmo-workbench-theme') === 'light' ? 'light' : 'dark'));

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('dtmo-workbench-theme', theme);
  }, [theme]);

  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setPaletteOpen(true);
      }
      if (event.key === 'Escape') {
        setPaletteOpen(false);
        setNavOpen(false);
      }
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
          <div className="topbar-start">
            <button className="icon-button mobile-only" type="button" onClick={() => setNavOpen((value) => !value)} aria-label="Navigatie openen" aria-expanded={navOpen}>☰</button>
            <div><p className="eyebrow">Dutch Threat Monitoring for Education</p><strong>Operations Workbench</strong></div>
          </div>
          <div className="topbar-center">
            <button type="button" className="command-trigger" onClick={() => setPaletteOpen(true)}><span aria-hidden="true">⌕</span><span>Zoek of navigeer</span><kbd>Ctrl K</kbd></button>
          </div>
          <div className="topbar-actions">
            <span className={`status-chip ${health.isError ? 'error' : health.data?.status === 'healthy' ? 'success' : 'neutral'}`} role="status"><span className="status-dot" />{healthLabel}</span>
            <button type="button" className="icon-button" onClick={() => setContextOpen((value) => !value)} aria-label="Objectcontext wisselen" aria-expanded={contextOpen}>◇</button>
            <button type="button" className="icon-button" onClick={() => setTheme((value) => value === 'dark' ? 'light' : 'dark')} aria-label="Thema wisselen">{theme === 'dark' ? '☀' : '☾'}</button>
          </div>
        </header>
        <div className="identity-strip" aria-live="polite">
          <span>{principalLabel}</span>
          <span>Publication/share authority remains server-side and human-governed.</span>
        </div>
        <main id="main-workspace" className="workspace">
          <Routes>
            <Route path="/" element={<Navigate to="/command-center" replace />} />
            {workspaces.map((workspace) => <Route key={workspace.path} path={`${workspace.path}/*`} element={<WorkspaceFoundation workspace={workspace} />} />)}
            <Route path="*" element={<Navigate to="/command-center" replace />} />
          </Routes>
        </main>
      </div>
      <ContextRail open={contextOpen} onClose={() => setContextOpen(false)} />
      <CommandPalette open={paletteOpen} onClose={() => setPaletteOpen(false)} />
    </div>
  );
}
