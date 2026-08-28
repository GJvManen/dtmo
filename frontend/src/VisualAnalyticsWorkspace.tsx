import { useQuery } from '@tanstack/react-query';

type TrendPoint = { date: string; count: number };
type SeverityPoint = { severity: string; count: number };
type SourcePoint = { source_id: string; count: number };
type IntelligenceTypePoint = { item_type: string; count: number };
type EnrichmentStatusPoint = { status: string; count: number };
type CollectionVolumePoint = { connector_id: string; inserted: number };
type CommandCenterSnapshot = {
  data_state: 'available' | 'unavailable';
  trends?: {
    intelligence_7d: TrendPoint[];
    severity_distribution: SeverityPoint[];
    source_distribution: SourcePoint[];
    type_distribution: IntelligenceTypePoint[];
    enrichment_status_distribution: EnrichmentStatusPoint[];
    collection_volume_distribution: CollectionVolumePoint[];
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

function AccessibleBars({ title, points, labelKey }: { title: string; points: Array<{ label: string; value: number }>; labelKey: string }) {
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
            <thead><tr><th scope="col">{labelKey}</th><th scope="col">Count</th></tr></thead>
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
  const collectionVolume = commandCenter.data?.data_state === 'available'
    ? (commandCenter.data.trends?.collection_volume_distribution ?? []).map((point) => ({ label: point.connector_id, value: point.inserted }))
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
        <AccessibleBars title="Enrichment status" points={enrichmentStatuses} labelKey="Status" />
        <AccessibleBars title="Collection volume" points={collectionVolume} labelKey="Connector" />
        <AccessibleBars title="Severity distribution" points={severity} labelKey="Severity" />
        <AccessibleBars title="Vulnerability observations" points={vulnerabilityTrend} labelKey="Date" />
      </div>

      <section className="surface command-panel" aria-label="Analytics evidence boundary">
        <h2>Evidence boundary</h2>
        <p>Source contribution, intelligence type distribution, enrichment status and collection volume are counted directly from persisted canonical records. Collection volume is the sum of persisted inserted-record counts by connector and is historical execution evidence only. Persisted analytics does not prove live connectivity, freshness, connector health, current upstream availability or local exposure; it does not grant review authority, sharing approval or publication authority and does not prove compromise or analyzer correctness.</p>
        {vulnerability.data?.claim_boundary && <p>{vulnerability.data.claim_boundary}</p>}
      </section>
    </section>
  );
}