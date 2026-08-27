import { useNavigate } from 'react-router-dom';

import { AdministrationSecurityAudit } from './AdministrationSecurityAudit';
import { AdministrationWorkspace } from './AdministrationWorkspace';
import { BundledPlatformReadiness } from './BundledPlatformReadiness';
import { FrameworkIntegrationReadiness } from './FrameworkIntegrationReadiness';

type SectionTarget = {
  id: string;
  label: string;
  selector?: string;
  route?: string;
};

const sections: SectionTarget[] = [
  { id: 'overview', label: 'Overview', selector: '#administration-overview' },
  { id: 'integrations', label: 'Integrations', selector: '#integration-admin-title' },
  { id: 'sources', label: 'Sources', route: '/collection' },
  { id: 'identity', label: 'Identity', selector: '#identity-admin-title' },
  { id: 'roles', label: 'Roles & Permissions', selector: '[data-admin-section="role-catalog"]' },
  { id: 'security', label: 'Security & Audit', selector: '[data-admin-section="security-audit"]' },
];

export function AdministrationConsole() {
  const navigate = useNavigate();

  const openSection = (target: SectionTarget) => {
    if (target.route) {
      navigate(target.route);
      return;
    }
    const element = target.selector ? document.querySelector<HTMLElement>(target.selector) : null;
    element?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    element?.focus({ preventScroll: true });
  };

  return (
    <div className="workspace-foundation" data-administration-console>
      <nav className="surface command-panel" aria-label="Administration sections">
        <header className="panel-heading">
          <div><p className="eyebrow">One administration console</p><h2>Administration sections</h2></div>
          <span className="evidence-label">Canonical workbench</span>
        </header>
        <p className="boundary-copy">Use this section navigation to move through the canonical Administration control plane without switching to legacy interfaces. Navigation does not grant authority; every read and mutation remains server-authorized.</p>
        <div className="quick-grid">
          {sections.map((target) => (
            <button
              key={target.id}
              type="button"
              className="quick-action"
              data-admin-nav={target.id}
              onClick={() => openSection(target)}
            >
              <span aria-hidden="true">◇</span>
              <div><strong>{target.label}</strong><small>{target.route ? 'Open the canonical Sources & Collection workspace.' : 'Jump to this section without leaving the canonical console.'}</small></div>
            </button>
          ))}
        </div>
      </nav>

      <div id="administration-overview" tabIndex={-1}>
        <BundledPlatformReadiness />
        <FrameworkIntegrationReadiness />
      </div>
      <AdministrationWorkspace />
      <AdministrationSecurityAudit />
    </div>
  );
}
