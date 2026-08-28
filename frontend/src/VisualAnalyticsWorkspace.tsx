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
type VulnerabilityAnalytics = {
  status: string;
  trend?: TrendPoint[];
  summary?: {
    total?: number;
    kev?: number;
    with_sightings?: number;
  };
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
      </div>

      <section className="surface command-panel" aria-label="Analytics evidence boundary">
        <h2>Evidence boundary</h2>
        <p>Source contribution, intelligence type distribution, IOC type distribution, enrichment status, collection volume and collection observation age are derived directly from persisted canonical records. IOC type distribution counts persisted observable types from canonical enrichment records and does not infer maliciousness or local compromise. Collection volume is the sum of persisted inserted-record counts by connector and is historical execution evidence only. Collection observation age is calculated from the latest persisted connector-run start timestamp and is historical observation evidence only. Persisted analytics does not prove live connectivity. It does not prove local exposure, does not prove source reachability, connector health, operational freshness or current upstream availability, and does not grant review authority, sharing approval or publication authority. It also does not prove compromise or analyzer correctness.</p>
        {vulnerability.data?.claim_boundary && <p>{vulnerability.data.claim_boundary}</p>}
      </section>
    </section>
  );
}