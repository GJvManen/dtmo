import { useQuery } from '@tanstack/react-query';

type TrendPoint = { date: string; count: number };
type SeverityPoint = { severity: string; count: number };
type SourcePoint = { source_id: string; count: number };
type IntelligenceTypePoint = { item_type: string; count: number };
type EnrichmentStatusPoint = { status: string; count: number };
type IocTypePoint = { observable_type: string; count: number };
type CollectionVolumePoint = { connector_id: string; inserted: number };
type CollectionObservationAgePoint = { connector_id: string; last_started_at: string; age_hours: number };
type CommandCenterSnapshot = {
  data_state: 'available' | 'unavailable';
  trends?: {
    intelligence_7d: TrendPoint[];
    severity_distribution: SeverityPoint[];
    source_distribution: SourcePoint[];
    type_distribution: IntelligenceTypePoint[];
    enrichment_status_distribution: EnrichmentStatusPoint[];
    ioc_type_distribution: IocTypePoint[];
    collection_volume_distribution: CollectionVolumePoint[];
    collection_observation_age: CollectionObservationAgePoint[];
  };
};
type VulnerabilityItem = { kev?: boolean | null; cvss?: number | null; epss?: number | null };
type VulnerabilityAnalytics = {
  status: string;
  trend?: TrendPoint[];
  summary?: {
    total?: number;
    kev?: number;
    with_sightings?: number;
  };
  items?: VulnerabilityItem[];
  claim_boundary?: string;
};

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url, {
    credentials: 'same-origin',
    headers: { Accept: 'application/json' },
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json() as Promise<T>;
}

function AccessibleBars({ title, points, labelKey, valueKey = 'Count' }: { title: string; points: Array<{ label: string; value: number }>; labelKey: string; valueKey?: string }) {
  const max = Math.max(1, ...points.map((point) => point.value));
  return (
    <section className="surface command-panel" aria-label={title}>
      <header className="panel-heading"><div><p className="eyebrow">Canonical analytics</p><h2>{title}</h2></div></header>
      {!points.length ? <p className="panel-state">No attributable data is available for this view.</p> : (
        <>
          <div className="trend-chart" role="list" aria-label={`${title} chart`}>
            {points.map((point) => (
              <div className="trend-column" role="listitem" key={point.label} aria-label={`${point.label}: ${point.value}`}>
                <strong>{point.value}</strong>
                <div className="trend-track"><span style={{ height: `${Math.max(4, (point.value / max) * 100)}%` }} /></div>
                <span>{point.label}</span>
              </div>
            ))}
          </div>
          <table aria-label={`${title} table`}>
            <thead><tr><th scope="col">{labelKey}</th><th scope="col">{valueKey}</th></tr></thead>
            <tbody>{points.map((point) => <tr key={point.label}><td>{point.label}</td><td>{point.value}</td></tr>)}</tbody>
          </table>
        </>
      )}
    </section>
  );
}

export function VisualAnalyticsWorkspace() {
  const commandCenter = useQuery({
    queryKey: ['visual-analytics', 'command-center'],
    queryFn: () => fetchJson<CommandCenterSnapshot>('/api/v1/command-center'),
    retry: false,
  });
  const vulnerability = useQuery({
    queryKey: ['visual-analytics', 'vulnerability'],
    queryFn: () => fetchJson<VulnerabilityAnalytics>('/api/v1/console/vulnerability-analytics'),
    retry: false,
  });

  const intelligenceTrend = commandCenter.data?.data_state === 'available'
    ? (commandCenter.data.trends?.intelligence_7d ?? []).map((point) => ({ label: point.date, value: point.count }))
    : [];
  const severity = commandCenter.data?.data_state === 'available'
    ? (commandCenter.data.trends?.severity_distribution ?? []).map((point) => ({ label: point.severity, value: point.count }))
    : [];
  const sourceContribution = commandCenter.data?.data_state === 'available'
    ? (commandCenter.data.trends?.source_distribution ?? []).map((point) => ({ label: point.source_id, value: point.count }))
    : [];
  const intelligenceTypes = commandCenter.data?.data_state === 'available'
    ? (commandCenter.data.trends?.type_distribution ?? []).map((point) => ({ label: point.item_type, value: point.count }))
    : [];
  const enrichmentStatuses = commandCenter.data?.data_state === 'available'
    ? (commandCenter.data.trends?.enrichment_status_distribution ?? []).map((point) => ({ label: point.status, value: point.count }))
    : [];
  const iocTypes = commandCenter.data?.data_state === 'available'
    ? (commandCenter.data.trends?.ioc_type_distribution ?? []).map((point) => ({ label: point.observable_type, value: point.count }))
    : [];
  const collectionVolume = commandCenter.data?.data_state === 'available'
    ? (commandCenter.data.trends?.collection_volume_distribution ?? []).map((point) => ({ label: point.connector_id, value: point.inserted }))
    : [];
  const collectionObservationAge = commandCenter.data?.data_state === 'available'
    ? (commandCenter.data.trends?.collection_observation_age ?? []).map((point) => ({ label: point.connector_id, value: point.age_hours }))
    : [];
  const vulnerabilityTrend = vulnerability.data?.status === 'ok'
    ? (vulnerability.data.trend ?? []).map((point) => ({ label: point.date, value: point.count }))
    : [];
  const vulnerabilityItems = vulnerability.data?.items ?? [];
  const kevDistribution = vulnerabilityItems.length
    ? [
        { label: 'known_exploited', value: vulnerabilityItems.filter((item) => item.kev === true).length },
        { label: 'not_known_exploited', value: vulnerabilityItems.filter((item) => item.kev === false).length },
        { label: 'unknown', value: vulnerabilityItems.filter((item) => item.kev !== true && item.kev !== false).length },
      ]
    : [];
  const cvssDistribution = vulnerabilityItems.length
    ? [
        { label: 'critical (9.0–10.0)', value: vulnerabilityItems.filter((item) => typeof item.cvss === 'number' && item.cvss >= 9).length },
        { label: 'high (7.0–8.9)', value: vulnerabilityItems.filter((item) => typeof item.cvss === 'number' && item.cvss >= 7 && item.cvss < 9).length },
        { label: 'medium (4.0–6.9)', value: vulnerabilityItems.filter((item) => typeof item.cvss === 'number' && item.cvss >= 4 && item.cvss < 7).length },
        { label: 'low (0.1–3.9)', value: vulnerabilityItems.filter((item) => typeof item.cvss === 'number' && item.cvss > 0 && item.cvss < 4).length },
        { label: 'none (0.0)', value: vulnerabilityItems.filter((item) => item.cvss === 0).length },
        { label: 'unknown', value: vulnerabilityItems.filter((item) => typeof item.cvss !== 'number').length },
      ]
    : [];
  const epssDistribution = vulnerabilityItems.length
    ? [
        { label: 'very high (0.75–1.00)', value: vulnerabilityItems.filter((item) => typeof item.epss === 'number' && item.epss >= 0.75).length },
        { label: 'high (0.50–0.74)', value: vulnerabilityItems.filter((item) => typeof item.epss === 'number' && item.epss >= 0.5 && item.epss < 0.75).length },
        { label: 'moderate (0.25–0.49)', value: vulnerabilityItems.filter((item) => typeof item.epss === 'number' && item.epss >= 0.25 && item.epss < 0.5).length },
        { label: 'low (0.00–0.24)', value: vulnerabilityItems.filter((item) => typeof item.epss === 'number' && item.epss >= 0 && item.epss < 0.25).length },
        { label: 'unknown', value: vulnerabilityItems.filter((item) => typeof item.epss !== 'number').length },
      ]
    : [];

  return (
    <section className="command-center" aria-labelledby="workspace-title">
      <header className="workspace-heading command-heading">
        <div>
          <p className="eyebrow">Unified Operations Workbench</p>
          <h1 id="workspace-title">Visual Analytics</h1>
          <p>Accessible, attributable trend and distribution views over canonical DTMO data.</p>
        </div>
        <span className="phase-badge">R5 cross-workspace analytics</span>
      </header>

      {(commandCenter.isError || vulnerability.isError) && (
        <div className="surface panel-state error-state" role="status">
          One or more canonical analytics sources are unavailable. No attributable values are synthesized.
        </div>
      )}

      <div className="command-grid">
        <AccessibleBars title="Intelligence arrivals · 7 days" points={intelligenceTrend} labelKey="Date" />
        <AccessibleBars title="Source contribution" points={sourceContribution} labelKey="Source" />
        <AccessibleBars title="Intelligence type distribution" points={intelligenceTypes} labelKey="Type" />
        <AccessibleBars title="IOC type distribution" points={iocTypes} labelKey="Observable type" />
        <AccessibleBars title="Enrichment status" points={enrichmentStatuses} labelKey="Status" />
        <AccessibleBars title="Collection volume" points={collectionVolume} labelKey="Connector" />
        <AccessibleBars title="Collection observation age" points={collectionObservationAge} labelKey="Connector" valueKey="Hours since latest persisted run start" />
        <AccessibleBars title="Severity distribution" points={severity} labelKey="Severity" />
        <AccessibleBars title="Vulnerability observations" points={vulnerabilityTrend} labelKey="Date" />
        <AccessibleBars title="KEV status distribution" points={kevDistribution} labelKey="KEV evidence status" />
        <AccessibleBars title="CVSS score distribution" points={cvssDistribution} labelKey="CVSS score band" />
        <AccessibleBars title="EPSS probability distribution" points={epssDistribution} labelKey="EPSS probability band" />
      </div>

      <section className="surface command-panel" aria-label="Analytics evidence boundary">
        <h2>Evidence boundary</h2>
        <p>Source contribution, intelligence type distribution, IOC type distribution, enrichment status, collection volume and collection observation age are derived directly from persisted canonical records. IOC type distribution counts persisted observable types from canonical enrichment records and does not infer maliciousness or local compromise. Collection volume is the sum of persisted inserted-record counts by connector and is historical execution evidence only. Collection observation age is calculated from the latest persisted connector-run start timestamp and is historical observation evidence only. KEV status distribution, CVSS score distribution and EPSS probability distribution are derived only from canonical vulnerability API rows that passed the existing raw-evidence integrity boundary. CVSS scores and EPSS probabilities are prioritization evidence and do not prove exploitability, local deployment or local exposure. KEV evidence does not prove local deployment, exploitability or compromise. Persisted analytics does not prove live connectivity. It does not prove local exposure, does not prove source reachability, connector health, operational freshness or current upstream availability, and does not grant review authority, sharing approval or publication authority. It also does not prove compromise or analyzer correctness.</p>
        {vulnerability.data?.claim_boundary && <p>{vulnerability.data.claim_boundary}</p>}
      </section>
    </section>
  );
}