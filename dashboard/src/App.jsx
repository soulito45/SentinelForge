import { useEffect, useState } from "react";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

const NAV_ITEMS = [
  { key: "overview", label: "Overview", icon: "◈" },
  { key: "assets", label: "Assets", icon: "◇" },
  { key: "findings", label: "Findings", icon: "△" },
  { key: "changes", label: "Changes", icon: "↗" },
  { key: "scans", label: "Scans", icon: "◎" },
];

function App() {
  const [activeSection, setActiveSection] = useState("overview");
  const [overview, setOverview] = useState(null);
  const [assets, setAssets] = useState([]);
  const [findings, setFindings] = useState([]);
  const [changes, setChanges] = useState([]);
  const [domains, setDomains] = useState([]);
  const [scanHistory, setScanHistory] = useState([]);
  const [domainName, setDomainName] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  useEffect(() => {
    void loadDashboard();
  }, []);

  const requestJson = async (url, options = {}) => {
    const response = await fetch(url, {
      ...options,
      headers: {
        Accept: "application/json",
        ...(options.headers || {}),
      },
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(text || `Request failed (${response.status})`);
    }

    return response.json();
  };

  const loadDashboard = async () => {
    try {
      setError("");
      setLoading(true);

      const [overviewResponse, assetsResponse, domainsResponse] = await Promise.all([
        requestJson(`${API_BASE}/dashboard/overview`),
        requestJson(`${API_BASE}/dashboard/assets`),
        requestJson(`${API_BASE}/domains/`),
      ]);

      setOverview(overviewResponse);
      setAssets(assetsResponse);
      setDomains(domainsResponse);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadFindings = async () => {
    if (findings.length) {
      return;
    }

    try {
      setError("");
      const data = await requestJson(`${API_BASE}/dashboard/findings`);
      setFindings(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const loadChanges = async () => {
    if (changes.length) {
      return;
    }

    try {
      setError("");
      const data = await requestJson(`${API_BASE}/dashboard/changes`);
      setChanges(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleNavClick = async (section) => {
    setActiveSection(section);

    if (section === "findings") {
      await loadFindings();
    }

    if (section === "changes") {
      await loadChanges();
    }
  };

  const handleCreateDomain = async (event) => {
    event.preventDefault();

    if (!domainName.trim()) {
      setStatusMessage("Enter a domain name first.");
      return;
    }

    try {
      setSubmitting(true);
      setError("");
      setStatusMessage("");

      const domain = await requestJson(
        `${API_BASE}/domains/?name=${encodeURIComponent(domainName.trim())}`,
        {
          method: "POST",
        },
      );

      setDomains((previousDomains) => [domain, ...previousDomains]);
      setDomainName("");
      setStatusMessage(`Domain "${domain.name}" added successfully.`);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleScanDomain = async (domainId, domainNameValue) => {
    try {
      setError("");
      setStatusMessage(`Starting scan for ${domainNameValue}...`);

      const result = await requestJson(
        `${API_BASE}/scans/?domain_id=${domainId}`,
        {
          method: "POST",
        },
      );

      setScanHistory((previousScans) => [
        {
          id: result.scan_id,
          domain: domainNameValue,
          status: result.status,
          assetsDiscovered: result.assets_discovered,
          totalChanges: result.total_changes,
          startedAt: result.started_at,
          completedAt: result.completed_at,
        },
        ...previousScans,
      ]);

      setStatusMessage(
        `Scan started for ${domainNameValue}. Status: ${result.status}.`,
      );
    } catch (err) {
      setError(err.message);
    }
  };

  const renderAssetTable = (title, subtitle) => (
    <section className="panel assets-panel">
      <div className="panel-header">
        <div>
          <div className="eyebrow">ATTACK SURFACE</div>
          <h3>{title}</h3>
        </div>

        <div className="asset-count">
          {subtitle || `${assets.length} TOTAL`}
        </div>
      </div>

      <div className="asset-table">
        <div className="table-header">
          <span>HOSTNAME</span>
          <span>STATUS</span>
          <span>HTTP</span>
          <span>RISK</span>
          <span>SCORE</span>
        </div>

        {assets.map((asset) => (
          <div className="asset-row" key={asset.id}>
            <div className="hostname-cell">
              <div className="host-icon">⌁</div>
              <div>
                <strong>{asset.hostname}</strong>
                <small>{asset.asset_type}</small>
              </div>
            </div>

            <div>
              <span className={`status-badge ${asset.status}`}>
                {asset.status}
              </span>
            </div>

            <div className="http-cell">
              {asset.http_status ? (
                <>
                  <strong>{asset.http_status}</strong>
                  <small>{asset.http_title || "HTTP service"}</small>
                </>
              ) : (
                <span className="muted">—</span>
              )}
            </div>

            <div>
              <span className={`risk-badge ${asset.risk_level.toLowerCase()}`}>
                {asset.risk_level}
              </span>
            </div>

            <div className="score-cell">
              <strong>{asset.risk_score}</strong>
              <span>/100</span>
            </div>
          </div>
        ))}

        {assets.length === 0 && (
          <div className="table-empty">No assets discovered yet.</div>
        )}
      </div>
    </section>
  );

  const renderOverview = () => (
    <>
      <section className="content">
        <div className="intro">
          <div>
            <div className="eyebrow">SECURITY INTELLIGENCE</div>
            <h2>What is happening to your attack surface?</h2>
          </div>
          <p>
            Continuous visibility across assets, exposure, technologies and
            security findings.
          </p>
        </div>

        <section className="metric-grid">
          <MetricCard
            label="Overall Risk"
            value={
              overview.risk_distribution.critical > 0
                ? "CRITICAL"
                : overview.risk_distribution.high > 0
                  ? "HIGH"
                  : overview.risk_distribution.medium > 0
                    ? "MEDIUM"
                    : "LOW"
            }
            detail="Highest asset risk"
            emphasis="risk"
          />

          <MetricCard
            label="Total Assets"
            value={overview.total_assets}
            detail={`${overview.active_assets} active`}
          />

          <MetricCard
            label="Open Ports"
            value={overview.open_ports}
            detail="Internet exposure"
          />

          <MetricCard
            label="Open Findings"
            value={overview.open_findings}
            detail="Require investigation"
            emphasis={overview.open_findings > 0 ? "warning" : ""}
          />
        </section>

        <section className="analysis-grid">
          <div className="panel">
            <div className="panel-header">
              <div>
                <div className="eyebrow">RISK POSTURE</div>
                <h3>Risk distribution</h3>
              </div>
              <span className="panel-meta">ASSETS</span>
            </div>

            <div className="risk-list">
              <RiskRow
                label="Critical"
                value={overview.risk_distribution.critical}
                total={overview.total_assets}
              />
              <RiskRow
                label="High"
                value={overview.risk_distribution.high}
                total={overview.total_assets}
              />
              <RiskRow
                label="Medium"
                value={overview.risk_distribution.medium}
                total={overview.total_assets}
              />
              <RiskRow
                label="Low"
                value={overview.risk_distribution.low}
                total={overview.total_assets}
              />
            </div>
          </div>

          <div className="panel">
            <div className="panel-header">
              <div>
                <div className="eyebrow">ATTENTION</div>
                <h3>Investigation queue</h3>
              </div>
              <span className="panel-meta">OPEN</span>
            </div>

            <div className="queue">
              {overview.open_findings > 0 ? (
                <div className="queue-item">
                  <div className="queue-marker warning-marker">!</div>
                  <div className="queue-content">
                    <strong>{overview.open_findings} open finding</strong>
                    <span>
                      Security finding requires analyst review
                    </span>
                  </div>
                  <span className="queue-arrow">→</span>
                </div>
              ) : (
                <div className="empty-state">
                  <div className="empty-icon">✓</div>
                  <strong>No open findings</strong>
                  <span>Attack surface currently clear</span>
                </div>
              )}

              {overview.open_ports > 0 && (
                <div className="queue-item">
                  <div className="queue-marker">↗</div>
                  <div className="queue-content">
                    <strong>{overview.open_ports} exposed ports</strong>
                    <span>Review externally reachable services</span>
                  </div>
                  <span className="queue-arrow">→</span>
                </div>
              )}
            </div>
          </div>
        </section>

        {renderAssetTable("Assets", `${overview.active_assets} ACTIVE / ${overview.total_assets} TOTAL`)}
      </section>
    </>
  );

  const renderFindings = () => (
    <section className="content">
      <div className="page-header">
        <div>
          <div className="eyebrow">SECURITY FINDINGS</div>
          <h2>Findings</h2>
        </div>
      </div>

      <section className="panel assets-panel">
        <div className="panel-header">
          <div>
            <div className="eyebrow">ATTENTION</div>
            <h3>Current findings</h3>
          </div>
          <div className="asset-count">{findings.length} TOTAL</div>
        </div>

        <div className="asset-table findings-table">
          <div className="table-header">
            <span>ASSET</span>
            <span>TITLE</span>
            <span>SEVERITY</span>
            <span>STATUS</span>
            <span>LAST SEEN</span>
          </div>

          {findings.map((finding) => (
            <div className="asset-row" key={finding.id}>
              <div className="hostname-cell">
                <div className="host-icon">⚑</div>
                <div>
                  <strong>{finding.asset_id}</strong>
                  <small>Asset ID</small>
                </div>
              </div>

              <div className="http-cell">
                <strong>{finding.title}</strong>
                <small>{finding.template_id}</small>
              </div>

              <div>
                <span className={`risk-badge ${finding.severity.toLowerCase()}`}>
                  {finding.severity}
                </span>
              </div>

              <div>
                <span className={`status-badge ${finding.status}`}>
                  {finding.status}
                </span>
              </div>

              <div className="score-cell">
                <strong>{new Date(finding.last_seen).toLocaleDateString()}</strong>
              </div>
            </div>
          ))}

          {findings.length === 0 && (
            <div className="table-empty">No findings available yet.</div>
          )}
        </div>
      </section>
    </section>
  );

  const renderChanges = () => (
    <section className="content">
      <div className="page-header">
        <div>
          <div className="eyebrow">CHANGE TRACKING</div>
          <h2>Changes</h2>
        </div>
      </div>

      <section className="panel assets-panel">
        <div className="panel-header">
          <div>
            <div className="eyebrow">HISTORY</div>
            <h3>Detected changes</h3>
          </div>
          <div className="asset-count">{changes.length} TOTAL</div>
        </div>

        <div className="asset-table findings-table">
          <div className="table-header">
            <span>ASSET</span>
            <span>CHANGE TYPE</span>
            <span>DESCRIPTION</span>
            <span>PREVIOUS</span>
            <span>CURRENT</span>
          </div>

          {changes.map((change) => (
            <div className="asset-row" key={change.id}>
              <div className="hostname-cell">
                <div className="host-icon">⇄</div>
                <div>
                  <strong>{change.asset_id}</strong>
                  <small>Asset ID</small>
                </div>
              </div>

              <div>
                <span className="status-badge active">{change.change_type}</span>
              </div>

              <div className="http-cell">
                <strong>{change.description}</strong>
                <small>{new Date(change.detected_at).toLocaleString()}</small>
              </div>

              <div className="score-cell">
                <strong>{change.previous_value || "—"}</strong>
              </div>

              <div className="score-cell">
                <strong>{change.current_value || "—"}</strong>
              </div>
            </div>
          ))}

          {changes.length === 0 && (
            <div className="table-empty">No change events yet.</div>
          )}
        </div>
      </section>
    </section>
  );

  const renderScans = () => (
    <section className="content">
      <div className="page-header">
        <div>
          <div className="eyebrow">OPERATIONS</div>
          <h2>Scans</h2>
        </div>
      </div>

      <section className="panel scan-panel">
        <div className="panel-header">
          <div>
            <div className="eyebrow">DOMAIN INPUT</div>
            <h3>Add a new domain</h3>
          </div>
        </div>

        <div className="scan-controls">
          <form className="scan-form" onSubmit={handleCreateDomain}>
            <input
              type="text"
              value={domainName}
              onChange={(event) => setDomainName(event.target.value)}
              placeholder="example.com"
            />
            <button type="submit" disabled={submitting}>
              {submitting ? "Adding..." : "Add domain"}
            </button>
          </form>
        </div>
      </section>

      <section className="panel assets-panel">
        <div className="panel-header">
          <div>
            <div className="eyebrow">AVAILABLE DOMAINS</div>
            <h3>Run scans</h3>
          </div>
          <div className="asset-count">{domains.length} DOMAINS</div>
        </div>

        <div className="domain-list">
          {domains.map((domain) => (
            <div className="domain-item" key={domain.id}>
              <div>
                <strong>{domain.name}</strong>
                <small>Created {new Date(domain.created_at).toLocaleDateString()}</small>
              </div>

              <button
                type="button"
                className="action-button"
                onClick={() => handleScanDomain(domain.id, domain.name)}
              >
                Start scan
              </button>
            </div>
          ))}

          {domains.length === 0 && (
            <div className="table-empty">No domains yet. Add one to start scanning.</div>
          )}
        </div>
      </section>

      <section className="panel assets-panel">
        <div className="panel-header">
          <div>
            <div className="eyebrow">RECENT ACTIVITY</div>
            <h3>Scan history</h3>
          </div>
          <div className="asset-count">{scanHistory.length} RUNS</div>
        </div>

        <div className="scan-history">
          {scanHistory.map((scan) => (
            <div className="scan-item" key={`${scan.id}-${scan.domain}`}>
              <div>
                <strong>{scan.domain}</strong>
                <small>
                  Started {new Date(scan.startedAt).toLocaleString()} · Status: {scan.status}
                </small>
              </div>

              <div className="scan-metrics">
                <span>{scan.assetsDiscovered ?? 0} assets</span>
                <span>{scan.totalChanges ?? 0} changes</span>
              </div>
            </div>
          ))}

          {scanHistory.length === 0 && (
            <div className="table-empty">
              No scans started yet. Add a domain and run a scan.
            </div>
          )}
        </div>
      </section>
    </section>
  );

  if (loading) {
    return (
      <div className="app-shell loading-screen">
        <div className="loading-mark">RYNEX</div>
        <div className="loading-text">Loading attack surface...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-shell loading-screen">
        <div className="error-card">
          <div className="eyebrow">SYSTEM ERROR</div>
          <h1>Unable to reach RYNEX API</h1>
          <p>{error}</p>
          <span>Check that FastAPI is running on port 8000.</span>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">R</div>
          <div>
            <div className="brand-name">RYNEX</div>
            <div className="brand-subtitle">ATTACK SURFACE</div>
          </div>
        </div>

        <nav className="navigation">
          <div className="nav-section">MONITOR</div>

          {NAV_ITEMS.map((item) => (
            <button
              key={item.key}
              type="button"
              className={`nav-item ${activeSection === item.key ? "active" : ""}`}
              onClick={() => handleNavClick(item.key)}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="system-status">
            <span className="status-dot"></span>
            <div>
              <strong>System Online</strong>
              <small>API connected</small>
            </div>
          </div>

          <div className="version">RYNEX v0.1.0</div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <div className="breadcrumb">RYNEX / {activeSection.toUpperCase()}</div>
            <h1>External Attack Surface</h1>
          </div>

          <div className="topbar-right">
            <span className="live-indicator">
              <span></span>
              LIVE
            </span>
            <div className="topbar-divider"></div>
            <span className="timestamp">LOCAL ENVIRONMENT</span>
          </div>
        </header>

        {statusMessage && <div className="status-banner">{statusMessage}</div>}

        {activeSection === "overview" && renderOverview()}
        {activeSection === "assets" && renderAssetTable("Assets", `${assets.length} TOTAL`)}
        {activeSection === "findings" && renderFindings()}
        {activeSection === "changes" && renderChanges()}
        {activeSection === "scans" && renderScans()}
      </main>
    </div>
  );
}

function MetricCard({ label, value, detail, emphasis = "" }) {
  return (
    <div className={`metric-card ${emphasis}`}>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      <div className="metric-detail">{detail}</div>
    </div>
  );
}

function RiskRow({ label, value, total }) {
  const percentage = total > 0 ? (value / total) * 100 : 0;

  return (
    <div className="risk-row">
      <div className="risk-label">
        <span className={`risk-dot ${label.toLowerCase()}`}></span>
        {label}
      </div>

      <div className="risk-bar">
        <div
          className={`risk-fill ${label.toLowerCase()}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>

      <strong>{value}</strong>
    </div>
  );
}

export default App;
