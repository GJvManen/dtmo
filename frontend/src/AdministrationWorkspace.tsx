import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { NavLink } from 'react-router-dom';

type Session = { subject: string; roles: string[]; permissions: string[] };
type IntegrationRow = {
  id: string;
  name: string;
  enabled: boolean;
  api_base: string;
  credential_configured: boolean;
  state: 'ready' | 'credential-required' | 'configuration-required' | 'disabled';
  can_activate: boolean;
  activation_blockers: string[];
  ail_object_global_ids: string;
  credential_boundary: string;
};
type ConnectorRunResult = {
  connector_id: string;
  status: string;
  records: number;
  inserted: number;
  indexed: number;
  attempts: number;
  error: string | null;
  alert_state: string;
  correlation_id: string | null;
};
type RoleRow = { role: string; permissions: string[]; eligible_principal_types: string[]; immutable: boolean };
type PrincipalRow = {
  subject: string;
  display_name: string | null;
  principal_type: 'human' | 'service_account';
  active: boolean;
  roles: string[];
  requires_token_reissue: boolean;
  authorization_note: string;
};
type RbacMatrix = { separation_of_duties: string[]; immutable_policy: boolean };
type GovernedAssignment = { principal: PrincipalRow; request_id: string; reason: string; authorization_note: string };
type DraftState = Record<string, { enabled: boolean; apiBase: string; credential: string; ailObjectScope: string }>;
type PrincipalDraftState = Record<string, { displayName: string; active: boolean; roles: string[]; reason: string }>;

async function readJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === 'object' && body && 'detail' in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

async function writeJson<T>(url: string, method: 'POST' | 'PATCH', body: object): Promise<T> {
  const response = await fetch(url, {
    method,
    credentials: 'same-origin',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json', 'X-Request-ID': crypto.randomUUID() },
    body: JSON.stringify(body),
  });
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof payload === 'object' && payload && 'detail' in payload ? String((payload as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return payload as T;
}

async function runJson<T>(url: string): Promise<T> {
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { Accept: 'application/json', 'X-Request-ID': crypto.randomUUID() },
  });
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof payload === 'object' && payload && 'detail' in payload ? String((payload as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return payload as T;
}

export function AdministrationWorkspace() {
  const client = useQueryClient();
  const [drafts, setDrafts] = useState<DraftState>({});
  const [principalDrafts, setPrincipalDrafts] = useState<PrincipalDraftState>({});
  const [lastSaved, setLastSaved] = useState<string | null>(null);
  const [lastMispRun, setLastMispRun] = useState<ConnectorRunResult | null>(null);
  const [lastAilRun, setLastAilRun] = useState<ConnectorRunResult | null>(null);
  const [lastIdentitySaved, setLastIdentitySaved] = useState<string | null>(null);
  const [newSubject, setNewSubject] = useState('');
  const [newDisplayName, setNewDisplayName] = useState('');
  const [newType, setNewType] = useState<'human' | 'service_account'>('human');
  const [newRoles, setNewRoles] = useState<string[]>([]);

  const session = useQuery({ queryKey: ['administration', 'session'], queryFn: () => readJson<Session>('/api/v1/ui/session'), retry: false });
  const connectorAllowed = session.data?.permissions.includes('manage:connectors') ?? false;
  const identityAllowed = session.data?.permissions.includes('manage:users') ?? false;
  const integrations = useQuery({
    queryKey: ['administration', 'integrations'],
    queryFn: () => readJson<IntegrationRow[]>('/api/v1/admin/integrations'),
    enabled: connectorAllowed,
    retry: false,
  });
  const roles = useQuery({
    queryKey: ['administration', 'rbac', 'roles'],
    queryFn: () => readJson<RoleRow[]>('/api/v1/admin/rbac/roles'),
    enabled: identityAllowed,
    retry: false,
  });
  const principals = useQuery({
    queryKey: ['administration', 'rbac', 'principals'],
    queryFn: () => readJson<PrincipalRow[]>('/api/v1/admin/rbac/principals'),
    enabled: identityAllowed,
    retry: false,
  });
  const matrix = useQuery({
    queryKey: ['administration', 'rbac', 'matrix'],
    queryFn: () => readJson<RbacMatrix>('/api/v1/admin/rbac/matrix'),
    enabled: identityAllowed,
    retry: false,
  });

  const rows = useMemo(() => integrations.data ?? [], [integrations.data]);
  const roleRows = useMemo(() => roles.data ?? [], [roles.data]);
  const principalRows = useMemo(() => principals.data ?? [], [principals.data]);
  const integrationMutation = useMutation({
    mutationFn: ({ id, enabled, apiBase, credential, ailObjectScope }: { id: string; enabled: boolean; apiBase: string; credential: string; ailObjectScope: string }) => writeJson<IntegrationRow>(`/api/v1/admin/integrations/${encodeURIComponent(id)}`, 'PATCH', {
      enabled,
      api_base: apiBase,
      ...(credential.trim() ? { credential: credential.trim() } : {}),
      ...(id === 'ail' ? { ail_object_global_ids: ailObjectScope } : {}),
    }),
    onSuccess: (row) => {
      setLastSaved(row.id);
      setDrafts((current) => ({ ...current, [row.id]: { enabled: row.enabled, apiBase: row.api_base, credential: '', ailObjectScope: row.ail_object_global_ids ?? '' } }));
      void client.invalidateQueries({ queryKey: ['administration', 'integrations'] });
    },
  });
  const mispRunMutation = useMutation({
    mutationFn: () => runJson<ConnectorRunResult>('/connectors/misp/run'),
    onSuccess: (result) => {
      setLastMispRun(result);
      void client.invalidateQueries({ queryKey: ['administration', 'integrations'] });
    },
  });
  const ailRunMutation = useMutation({
    mutationFn: () => runJson<ConnectorRunResult>('/connectors/ail/run'),
    onSuccess: (result) => {
      setLastAilRun(result);
      void client.invalidateQueries({ queryKey: ['administration', 'integrations'] });
    },
  });
  const createPrincipalMutation = useMutation({
    mutationFn: () => writeJson<PrincipalRow>('/api/v1/admin/rbac/principals', 'POST', {
      subject: newSubject,
      display_name: newDisplayName || null,
      principal_type: newType,
      roles: newRoles,
      active: true,
    }),
    onSuccess: (row) => {
      setLastIdentitySaved(row.subject);
      setNewSubject('');
      setNewDisplayName('');
      setNewType('human');
      setNewRoles([]);
      void client.invalidateQueries({ queryKey: ['administration', 'rbac', 'principals'] });
    },
  });
  const assignmentMutation = useMutation({
    mutationFn: ({ subject, displayName, active, selectedRoles, reason }: { subject: string; displayName: string; active: boolean; selectedRoles: string[]; reason: string }) => writeJson<GovernedAssignment>(`/api/v1/admin/rbac/principals/${encodeURIComponent(subject)}/governed-assignment`, 'POST', {
      display_name: displayName || null,
      active,
      roles: selectedRoles,
      reason,
    }),
    onSuccess: (result) => {
      setLastIdentitySaved(result.principal.subject);
      setPrincipalDrafts((current) => ({ ...current, [result.principal.subject]: { displayName: result.principal.display_name ?? '', active: result.principal.active, roles: result.principal.roles, reason: '' } }));
      void client.invalidateQueries({ queryKey: ['administration', 'rbac', 'principals'] });
    },
  });

  const toggleNewRole = (role: string, checked: boolean) => setNewRoles((current) => checked ? [...new Set([...current, role])] : current.filter((item) => item !== role));
  const refreshAdministration = () => {
    if (connectorAllowed) void integrations.refetch();
    if (identityAllowed) { void roles.refetch(); void principals.refetch(); void matrix.refetch(); }
  };

  return (
    <section className="workspace-foundation" aria-labelledby="workspace-title">
      <header className="workspace-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Administration</h1>
          <p>Canonical control plane for framework configuration and governed identity/RBAC administration. Credentials and authorization policy remain server-side.</p>
        </div>
        <div className="heading-statuses"><span className="phase-badge">11.10q functional recovery</span><span className="evidence-label">Configuration ≠ runtime health</span></div>
      </header>

      <article className="surface command-panel">
        <header className="panel-heading"><div><p className="eyebrow">Administration control plane</p><h2>Governed configuration and identity</h2></div><button type="button" onClick={refreshAdministration} disabled={integrations.isFetching || principals.isFetching}>Refresh</button></header>
        <p className="boundary-copy">All mutations are authorized by the server and carry request IDs. Identity changes use DTMO's governed assignment endpoint and persistent audit trail; they do not rewrite externally issued bearer tokens.</p>
      </article>

      <article className="surface command-panel" aria-labelledby="integration-admin-title">
        <header className="panel-heading"><div><p className="eyebrow">Framework integrations</p><h2 id="integration-admin-title">Runtime configuration</h2></div><span className="evidence-label">manage:connectors</span></header>
        <p className="boundary-copy">Endpoint, enablement and write-only credential replacement are mutable here. MISP exposes governed read/import execution. AIL additionally requires an explicit non-secret object scope and remains read-only/data-minimized; Administration never starts AIL crawlers. Completed runs are request-specific runtime evidence, not blanket upstream-health or publication claims.</p>
      </article>

      {!session.isPending && !connectorAllowed && <article className="surface panel-state error-state"><strong>Integration administration unavailable</strong><span>This principal does not have server-authorized <code>manage:connectors</code>.</span></article>}
      {connectorAllowed && integrations.isPending && <p className="panel-state">Loading governed integration settings…</p>}
      {connectorAllowed && integrations.isError && <article className="surface panel-state error-state"><strong>Integration configuration unavailable</strong><span>{integrations.error.message}</span></article>}

      {connectorAllowed && rows.length > 0 && <div className="command-grid">
        {rows.map((row) => {
          const draft = drafts[row.id] ?? { enabled: row.enabled, apiBase: row.api_base, credential: '', ailObjectScope: row.ail_object_global_ids ?? '' };
          const scopeDirty = row.id === 'ail' && draft.ailObjectScope !== (row.ail_object_global_ids ?? '');
          const dirty = draft.enabled !== row.enabled || draft.apiBase !== row.api_base || Boolean(draft.credential.trim()) || scopeDirty;
          const canRunMisp = row.id === 'misp' && row.enabled && row.state === 'ready' && !dirty;
          const canRunAil = row.id === 'ail' && row.enabled && row.state === 'ready' && !dirty;
          return <article className="surface command-panel" key={row.id} data-integration={row.id}>
            <header className="panel-heading"><div><p className="eyebrow">{row.id}</p><h2>{row.name}</h2></div><span className={`status-chip ${row.state === 'ready' ? 'success' : 'neutral'}`}>{row.state.replaceAll('-', ' ')}</span></header>
            <label><span>API endpoint</span><input value={draft.apiBase} placeholder="https://platform.example/api" onChange={(event) => setDrafts((current) => ({ ...current, [row.id]: { ...draft, apiBase: event.target.value } }))} /></label>
            <label><span>Credential (write-only)</span><input type="password" autoComplete="new-password" value={draft.credential} placeholder={row.credential_configured ? 'Leave blank to keep current credential' : 'Enter credential'} onChange={(event) => setDrafts((current) => ({ ...current, [row.id]: { ...draft, credential: event.target.value } }))} /></label>
            {row.id === 'ail' && <label><span>AIL object scope</span><input value={draft.ailObjectScope} placeholder="domain:None:example.org,ip:None:203.0.113.10" onChange={(event) => setDrafts((current) => ({ ...current, [row.id]: { ...draft, ailObjectScope: event.target.value } }))} /></label>}
            <label><input type="checkbox" checked={draft.enabled} onChange={(event) => setDrafts((current) => ({ ...current, [row.id]: { ...draft, enabled: event.target.checked } }))} /> Enabled</label>
            <p className="boundary-copy">Credential: {row.credential_configured ? 'configured server-side' : 'not configured'}. Submitted values are write-only, cleared from this form after save and never returned by the API. {row.credential_boundary}</p>
            {row.activation_blockers.length > 0 && <p className="panel-state">Activation blockers: {row.activation_blockers.join(', ')}.</p>}
            {row.id === 'ail' && <p className="boundary-copy">AIL scope is non-secret persisted runtime configuration. Only explicitly scoped objects are read; crawler creation or activation is outside this workspace.</p>}
            <div className="quick-grid">
              <button type="button" className="quick-action" disabled={!dirty || integrationMutation.isPending} onClick={() => integrationMutation.mutate({ id: row.id, enabled: draft.enabled, apiBase: draft.apiBase, credential: draft.credential, ailObjectScope: draft.ailObjectScope })}><span aria-hidden="true">✓</span><div><strong>Save configuration</strong><small>Persist endpoint, enablement, optional credential replacement and governed component scope through DTMO.</small></div></button>
              {row.id === 'misp' && <button type="button" className="quick-action" data-misp-run disabled={!canRunMisp || mispRunMutation.isPending} onClick={() => mispRunMutation.mutate()}><span aria-hidden="true">↻</span><div><strong>Run MISP import now</strong><small>{dirty ? 'Save the current configuration before execution.' : row.state === 'ready' && row.enabled ? 'Execute the existing server-side MISP read connector and ingest returned canonical records.' : 'Enable MISP with endpoint and server-side credential before execution.'}</small></div></button>}
              {row.id === 'ail' && <button type="button" className="quick-action" data-ail-run disabled={!canRunAil || ailRunMutation.isPending} onClick={() => ailRunMutation.mutate()}><span aria-hidden="true">↻</span><div><strong>Run AIL import now</strong><small>{dirty ? 'Save the current AIL configuration before execution.' : row.state === 'ready' && row.enabled ? 'Read only the explicitly scoped AIL objects through the existing server-side connector and canonical ingest path.' : 'Enable AIL with endpoint, server-side credential and explicit object scope before execution.'}</small></div></button>}
            </div>
            {lastSaved === row.id && !integrationMutation.isError && <p className="panel-state">Configuration saved and reloaded. Credential values are not reloaded into the browser.</p>}
            {integrationMutation.isError && <p className="panel-state error-state">{integrationMutation.error.message}</p>}
            {row.id === 'misp' && mispRunMutation.isError && <p className="panel-state error-state">MISP import failed: {mispRunMutation.error.message}</p>}
            {row.id === 'misp' && lastMispRun && !mispRunMutation.isError && <p className={`panel-state ${lastMispRun.status === 'completed' ? '' : 'error-state'}`}>MISP runtime result: {lastMispRun.status}. Records {lastMispRun.records}; inserted {lastMispRun.inserted}; indexed {lastMispRun.indexed}; attempts {lastMispRun.attempts}. Alert {lastMispRun.alert_state}. Correlation {lastMispRun.correlation_id ?? 'not reported'}.{lastMispRun.error ? ` Error: ${lastMispRun.error}` : ''}</p>}
            {row.id === 'ail' && ailRunMutation.isError && <p className="panel-state error-state">AIL import failed: {ailRunMutation.error.message}</p>}
            {row.id === 'ail' && lastAilRun && !ailRunMutation.isError && <p className={`panel-state ${lastAilRun.status === 'completed' ? '' : 'error-state'}`}>AIL runtime result: {lastAilRun.status}. Records {lastAilRun.records}; inserted {lastAilRun.inserted}; indexed {lastAilRun.indexed}; attempts {lastAilRun.attempts}. Alert {lastAilRun.alert_state}. Correlation {lastAilRun.correlation_id ?? 'not reported'}.{lastAilRun.error ? ` Error: ${lastAilRun.error}` : ''}</p>}
          </article>;
        })}
      </div>}

      <article className="surface command-panel" aria-labelledby="identity-admin-title">
        <header className="panel-heading"><div><p className="eyebrow">Identity & RBAC</p><h2 id="identity-admin-title">Managed principals and role assignments</h2></div><span className="evidence-label">manage:users</span></header>
        <p className="boundary-copy">Role policy, principal-type boundaries, self-management protection and last-admin protection remain server-side. Review and external-share approval remain independently governed permissions.</p>
      </article>

      {!session.isPending && !identityAllowed && <article className="surface panel-state error-state"><strong>Identity administration unavailable</strong><span>This principal does not have server-authorized <code>manage:users</code>. No browser-side bypass is provided.</span></article>}
      {identityAllowed && (roles.isPending || principals.isPending || matrix.isPending) && <p className="panel-state">Loading governed identity and role policy…</p>}
      {identityAllowed && (roles.isError || principals.isError || matrix.isError) && <article className="surface panel-state error-state"><strong>RBAC administration unavailable</strong><span>{roles.error?.message ?? principals.error?.message ?? matrix.error?.message}</span></article>}

      {identityAllowed && roleRows.length > 0 && <article className="surface command-panel" data-admin-section="role-catalog">
        <header className="panel-heading"><div><p className="eyebrow">Server-side role catalogue</p><h2>{roleRows.length} immutable roles</h2></div><span className="status-chip success">Policy-bound</span></header>
        <div className="quick-grid">{roleRows.map((role) => <div className="quick-action" key={role.role}><span aria-hidden="true">◇</span><div><strong>{role.role}</strong><small>{role.permissions.join(', ') || 'No permissions'} · {role.eligible_principal_types.join(', ')}</small></div></div>)}</div>
        {(matrix.data?.separation_of_duties ?? []).map((boundary) => <p className="boundary-copy" key={boundary}>• {boundary}</p>)}
      </article>}

      {identityAllowed && roleRows.length > 0 && <article className="surface command-panel" data-admin-section="principal-create">
        <header className="panel-heading"><div><p className="eyebrow">Managed identity</p><h2>Create principal</h2></div><span className="evidence-label">Audited mutation</span></header>
        <label><span>Subject</span><input value={newSubject} onChange={(event) => setNewSubject(event.target.value)} placeholder="analyst@example.test" /></label>
        <label><span>Display name</span><input value={newDisplayName} onChange={(event) => setNewDisplayName(event.target.value)} /></label>
        <label><span>Principal type</span><select value={newType} onChange={(event) => { const nextType = event.target.value as 'human' | 'service_account'; setNewType(nextType); setNewRoles(nextType === 'service_account' ? ['service_account'] : []); }}><option value="human">Human</option><option value="service_account">Service account</option></select></label>
        <div className="quick-grid">{roleRows.filter((role) => role.eligible_principal_types.includes(newType)).map((role) => <label className="quick-action" key={role.role}><input type="checkbox" checked={newRoles.includes(role.role)} disabled={newType === 'service_account'} onChange={(event) => toggleNewRole(role.role, event.target.checked)} /><div><strong>{role.role}</strong><small>{role.permissions.join(', ')}</small></div></label>)}</div>
        <button type="button" disabled={!newSubject.trim() || newRoles.length === 0 || createPrincipalMutation.isPending} onClick={() => createPrincipalMutation.mutate()}>Create managed principal</button>
        {createPrincipalMutation.isError && <p className="panel-state error-state">{createPrincipalMutation.error.message}</p>}
      </article>}

      {identityAllowed && principalRows.length > 0 && <div className="command-grid" data-admin-section="managed-principals">
        {principalRows.map((row) => {
          const draft = principalDrafts[row.subject] ?? { displayName: row.display_name ?? '', active: row.active, roles: row.roles, reason: '' };
          const selfManaged = row.subject === session.data?.subject;
          const eligibleRoles = roleRows.filter((role) => role.eligible_principal_types.includes(row.principal_type));
          const dirty = draft.displayName !== (row.display_name ?? '') || draft.active !== row.active || draft.roles.slice().sort().join(',') !== row.roles.slice().sort().join(',');
          const updateDraft = (next: Partial<typeof draft>) => setPrincipalDrafts((current) => ({ ...current, [row.subject]: { ...draft, ...next } }));
          return <article className="surface command-panel" key={row.subject} data-managed-principal={row.subject}>
            <header className="panel-heading"><div><p className="eyebrow">{row.principal_type}</p><h2>{row.display_name || row.subject}</h2><small>{row.subject}</small></div><span className={`status-chip ${row.active ? 'success' : 'neutral'}`}>{row.active ? 'active' : 'inactive'}</span></header>
            <label><span>Display name</span><input value={draft.displayName} disabled={selfManaged} onChange={(event) => updateDraft({ displayName: event.target.value })} /></label>
            <label><input type="checkbox" checked={draft.active} disabled={selfManaged} onChange={(event) => updateDraft({ active: event.target.checked })} /> Active</label>
            <div className="quick-grid">{eligibleRoles.map((role) => <label className="quick-action" key={role.role}><input type="checkbox" checked={draft.roles.includes(role.role)} disabled={selfManaged || row.principal_type === 'service_account'} onChange={(event) => updateDraft({ roles: event.target.checked ? [...new Set([...draft.roles, role.role])] : draft.roles.filter((item) => item !== role.role) })} /><div><strong>{role.role}</strong><small>{role.permissions.join(', ')}</small></div></label>)}</div>
            {selfManaged ? <p className="panel-state">Self-management is server-side blocked. Use a separate authorized administrator for this assignment.</p> : <label><span>Required change reason</span><textarea value={draft.reason} minLength={3} maxLength={500} onChange={(event) => updateDraft({ reason: event.target.value })} placeholder="Explain why this assignment or status change is required." /></label>}
            {!selfManaged && <button type="button" disabled={!dirty || draft.roles.length === 0 || draft.reason.trim().length < 3 || assignmentMutation.isPending} onClick={() => assignmentMutation.mutate({ subject: row.subject, displayName: draft.displayName, active: draft.active, selectedRoles: draft.roles, reason: draft.reason })}>Save governed assignment</button>}
            <p className="boundary-copy">Token reissue/reconciliation: {row.requires_token_reissue ? 'required after assignment changes' : 'not reported'}. {row.authorization_note}</p>
            {lastIdentitySaved === row.subject && !assignmentMutation.isError && <p className="panel-state">Identity state saved through the governed API and reloaded.</p>}
            {assignmentMutation.isError && <p className="panel-state error-state">{assignmentMutation.error.message}</p>}
          </article>;
        })}
      </div>}

      <article className="surface evidence-surface"><div><p className="eyebrow">Canonical administration boundary</p><h2>No legacy administration dependency</h2></div><p>Integration endpoint, enablement, write-only credential replacement, governed MISP runtime import, explicit scoped AIL read/import and managed identity/RBAC administration are available through same-origin canonical APIs. Continue to <NavLink to="/collection">Sources & Collection</NavLink> for source execution and to <NavLink to="/governance">Governance & Evidence</NavLink> for governance evidence. Administration never grants review, sharing, publication or external-assurance authority by UI presence alone.</p></article>
    </section>
  );
}
