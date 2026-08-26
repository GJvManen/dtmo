import { useEffect, useState } from 'react';

type GrafanaState = 'checking' | 'available' | 'authentication-required' | 'unavailable';

export function BundledPlatformReadiness() {
  const [grafanaState, setGrafanaState] = useState<GrafanaState>('checking');

  const checkGrafana = async () => {
    setGrafanaState('checking');
    try {
      const response = await fetch('/grafana/api/health', {
        credentials: 'same-origin',
        headers: { Accept: 'application/json' },
      });
      if (response.ok) {
        setGrafanaState('available');
      } else if (response.status === 401 || response.status === 403) {
        setGrafanaState('authentication-required');
      } else {
        setGrafanaState('unavailable');
      }
    } catch {
      setGrafanaState('unavailable');
    }
  };

  useEffect(() => { void checkGrafana(); }, []);

  const statusCopy = grafanaState === 'available'
    ? 'Grafana is reachable through the supported same-origin gateway.'
    : grafanaState === 'authentication-required'
      ? 'Grafana is reachable but requires its configured authenticated session.'
      : grafanaState === 'unavailable'
        ? 'Grafana is not reachable through /grafana/. Verify the bundled Compose service and gateway.'
        : 'Checking same-origin Grafana readiness…';

  return (
    <section className="workspace-foundation" aria-labelledby="bundled-platform-title" data-admin-section="bundled-platform-readiness">
      <article className="surface command-panel">
        <header className="panel-heading">
          <div><p className="eyebrow">Bundled platform services</p><h2 id="bundled-platform-title">Platform readiness</h2></div>
          <button type="button" onClick={() => void checkGrafana()} disabled={grafanaState === 'checking'}>Check Grafana</button>
        </header>
        <p className="boundary-copy">Bundled services are part of the supported DTMO startup topology, but reachability does not imply healthy telemetry, production readiness or authorization. Grafana anonymous access remains disabled.</p>
        <article className="quick-action" data-platform-readiness="grafana">
          <span aria-hidden="true">◇</span>
          <div>
            <strong>Grafana dashboards</strong>
            <small data-grafana-state={grafanaState}>{statusCopy}</small>
            <small>Provisioned dashboards: DTMO Operations and DTMO Intelligence.</small>
          </div>
          <div>
            <a href="/grafana/d/dtmo-operations/dtmo-operations">Open Operations dashboard</a>{' '}
            <a href="/grafana/d/dtmo-intelligence/dtmo-intelligence">Open Intelligence dashboard</a>
          </div>
        </article>
      </article>
    </section>
  );
}
