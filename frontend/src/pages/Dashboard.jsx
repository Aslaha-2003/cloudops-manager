import { useEffect, useState } from 'react'

const API_BASE_URL = 'http://127.0.0.1:8000'

function Dashboard() {
  const [resources, setResources] = useState([])
  const [healthData, setHealthData] = useState({})
  const [metricsData, setMetricsData] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)
  const [refreshing, setRefreshing] = useState(false)

  const [selectedResource, setSelectedResource] = useState(null)

  const fetchDashboardData = async (isAutoRefresh = false) => {
    try {
      if (isAutoRefresh) {
        setLoading(true)
      } else{
        setLoading(true)
      }
      setError(null)

      // Fetch all resources
      const response = await fetch(
        `${API_BASE_URL}/resources/`
      )

      if (!response.ok) {
        throw new Error('Failed to fetch resources')
      }

      const data = await response.json()

      setResources(data)

      const healthResults = {}
      const metricsResults = {}

      // Fetch health and latest metrics
      await Promise.all(
        data.map(async (resource) => {
          try {
            const healthResponse = await fetch(
              `${API_BASE_URL}/resources/${resource.id}/health`
            )

            if (healthResponse.ok) {
              const health =
                await healthResponse.json()

              healthResults[resource.id] = health
            } else {
              healthResults[resource.id] = {
                health: 'unknown'
              }
            }

            const metricsResponse = await fetch(
              `${API_BASE_URL}/resources/${resource.id}/metrics/latest`
            )

            if (metricsResponse.ok) {
              const metrics =
                await metricsResponse.json()

              metricsResults[resource.id] =
                metrics
            } else {
              metricsResults[resource.id] = null
            }
          } catch (error) {
            console.error(
              `Error fetching resource ${resource.id}:`,
              error
            )

            healthResults[resource.id] = {
              health: 'unknown'
            }

            metricsResults[resource.id] = null
          }
        })
      )

      setHealthData(healthResults)
      setMetricsData(metricsResults)
      setLastUpdated(new Date())

    } catch (err) {
      console.error('API Error:', err)

      setError(
        'Unable to connect to the CloudOps API'
      )

      setResources([])
      setHealthData({})
      setMetricsData({})

    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  useEffect(() => {
    // Initial data load
    fetchDashboardData()

    // Refresh every 10 seconds
    const interval = setInterval(() => {
      fetchDashboardData(true)
    }, 10000)

    // Clean up when component unmounts
    return () => {
      clearInterval(interval)
    }
  }, [])

  // Dashboard calculations

  const totalResources = resources.length

  const runningResources = resources.filter(
    (resource) =>
      resource.status?.toLowerCase() ===
      'running'
  )

  const healthValues =
    Object.values(healthData)

  const healthyResources =
    healthValues.filter(
      (health) =>
        health.health?.toLowerCase() ===
        'healthy'
    )

  const warningResources =
    healthValues.filter(
      (health) =>
        health.health?.toLowerCase() ===
        'warning'
    )

  const criticalResources =
    healthValues.filter(
      (health) =>
        health.health?.toLowerCase() ===
        'critical'
    )

  const getHealthClass = (status) => {
    if (!status) return 'unknown-badge'

    switch (status.toLowerCase()) {
      case 'healthy':
        return 'healthy-badge'

      case 'warning':
        return 'warning-badge'

      case 'critical':
        return 'critical-badge'

      default:
        return 'unknown-badge'
    }
  }

  const getUsageClass = (percentage) => {
    if (percentage >= 90) {
      return 'usage-critical'
    }

    if (percentage >= 70) {
      return 'usage-warning'
    }

    return 'usage-normal'
  }

  const getProgressClass = (percentage) => {
    if (percentage >= 90) {
      return 'progress-critical'
    }

    if (percentage >= 70) {
      return 'progress-warning'
    }

    return 'progress-normal'
  }

  const UsageBar = ({ value }) => {
    if (value === undefined || value === null) {
      return (
        <span className="no-data">
          No data
        </span>
      )
    }

    return (
      <div className="usage-container">
        <div className="usage-value">
          <span
            className={getUsageClass(value)}
          >
            {value}%
          </span>
        </div>

        <div className="progress-track">
          <div
            className={`progress-bar ${getProgressClass(
              value
            )}`}
            style={{
              width: `${Math.min(value, 100)}%`
            }}
          />
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard-page">

      {/* HEADER */}

      <div className="dashboard-header">

  <div>
    <h1>Dashboard</h1>

    <p>
      Overview of your cloud resources
    </p>
  </div>

  <div className="dashboard-actions">

    {/* API STATUS */}

    <div
      className={`api-status ${
        error
          ? 'api-disconnected'
          : 'api-connected'
      }`}
    >
      <span className="status-dot"></span>

      {error
        ? 'API Disconnected'
        : 'API Connected'}
    </div>


    {/* LAST UPDATED TIME */}

    {lastUpdated && (
      <span className="last-updated">
        Updated: {lastUpdated.toLocaleTimeString()}
      </span>
    )}


    {/* MANUAL REFRESH BUTTON */}

    <button
      className="refresh-button"
      onClick={() => fetchDashboardData(true)}
      disabled={refreshing}
    >
      {refreshing
        ? 'Refreshing...'
        : '↻ Refresh'}
    </button>

  </div>

</div>

      {/* ERROR */}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* DASHBOARD CARDS */}

      <section className="stats-grid">

        <div className="stat-card">
          <div className="stat-icon resource-icon">
            ▣
          </div>

          <div>
            <p>Total</p>

            <span>Resources</span>

            <h3>
              {loading
                ? '...'
                : totalResources}
            </h3>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon running-icon">
            ▶
          </div>

          <div>
            <p>Running</p>

            <h3>
              {loading
                ? '...'
                : runningResources.length}
            </h3>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon healthy-icon">
            ♥
          </div>

          <div>
            <p>Healthy</p>

            <h3>
              {loading
                ? '...'
                : healthyResources.length}
            </h3>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon warning-icon">
            !
          </div>

          <div>
            <p>Warning</p>

            <h3>
              {loading
                ? '...'
                : warningResources.length}
            </h3>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon critical-icon">
            !
          </div>

          <div>
            <p>Critical</p>

            <h3>
              {loading
                ? '...'
                : criticalResources.length}
            </h3>
          </div>
        </div>

      </section>

      {/* RESOURCE OVERVIEW */}

      <section className="resource-section">

        <div className="resource-header">
          <div>
            <h2>
              Resource Overview
            </h2>

            <p>
              Current resources and live usage metrics
            </p>
          </div>
        </div>

        <div className="resource-table">

          <div className="table-header">
            <span>RESOURCE</span>
            <span>TYPE</span>
            <span>CPU</span>
            <span>MEMORY</span>
            <span>STORAGE</span>
            <span>STATUS</span>
            <span>HEALTH</span>
          </div>

          {loading && (
            <div className="empty-state">
              Loading resources...
            </div>
          )}

          {!loading &&
            resources.length === 0 && (
              <div className="empty-state">
                No resources found.
              </div>
            )}

          {!loading &&
            resources.map((resource) => {
              const healthStatus =
                healthData[resource.id]
                  ?.health || 'unknown'

              const metrics =
                metricsData[resource.id]

              return (
                <div
                  className="table-row clickable-row"
                  key={resource.id}
                  onClick={() =>
                    setSelectedResource(resource)
                  }
                >

                  {/* RESOURCE */}

                  <div className="resource-name">
                    <span className="resource-type-icon">
                      VM
                    </span>

                    <strong>
                      {resource.name}
                    </strong>
                  </div>

                  {/* TYPE */}

                  <span>
                    {resource.resource_type}
                  </span>

                  {/* CPU */}

                  <UsageBar
                    value={
                      metrics?.cpu_usage_percent
                    }
                  />

                  {/* MEMORY */}

                  <UsageBar
                    value={
                      metrics?.memory_usage_percent
                    }
                  />

                  {/* STORAGE */}

                  <UsageBar
                    value={
                      metrics?.storage_usage_percent
                    }
                  />

                  {/* STATUS */}

                  <span
                    className={`badge ${
                      resource.status
                        ?.toLowerCase() ===
                      'running'
                        ? 'running-badge'
                        : ''
                    }`}
                  >
                    {resource.status}
                  </span>

                  {/* HEALTH */}

                  <span
                    className={`badge ${getHealthClass(
                      healthStatus
                    )}`}
                  >
                    {healthStatus}
                  </span>

                </div>
              )
            })}

        </div>

      </section>

      {/* RESOURCE DETAILS MODAL */}

      {selectedResource && (
        <div
          className="modal-overlay"
          onClick={() =>
            setSelectedResource(null)
          }
        >
          <div
            className="resource-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            <div className="modal-header">
              <div>
                <h2>
                  {selectedResource.name}
                </h2>

                <p>
                  Resource Details
                </p>
              </div>

              <button
                className="close-button"
                onClick={() =>
                  setSelectedResource(null)
                }
              >
                ×
              </button>
            </div>

            <div className="details-grid">

              <div className="detail-item">
                <span>Resource ID</span>

                <strong>
                  {selectedResource.id}
                </strong>
              </div>

              <div className="detail-item">
                <span>Type</span>

                <strong>
                  {selectedResource.resource_type}
                </strong>
              </div>

              <div className="detail-item">
                <span>Status</span>

                <strong>
                  {selectedResource.status}
                </strong>
              </div>

              <div className="detail-item">
                <span>Health</span>

                <strong>
                  {healthData[
                    selectedResource.id
                  ]?.health || 'unknown'}
                </strong>
              </div>

              <div className="detail-item">
                <span>CPU Cores</span>

                <strong>
                  {selectedResource.cpu_cores}
                </strong>
              </div>

              <div className="detail-item">
                <span>Memory Capacity</span>

                <strong>
                  {selectedResource.memory_gb} GB
                </strong>
              </div>

              <div className="detail-item">
                <span>Storage Capacity</span>

                <strong>
                  {selectedResource.storage_gb} GB
                </strong>
              </div>

            </div>

            <div className="metrics-details">

              <h3>
                Current Usage
              </h3>

              <div className="metric-detail">

                <div className="metric-label">
                  <span>CPU Usage</span>

                  <strong>
                    {metricsData[
                      selectedResource.id
                    ]?.cpu_usage_percent ?? 0}%
                  </strong>
                </div>

                <div className="progress-track large">
                  <div
                    className={`progress-bar ${getProgressClass(
                      metricsData[
                        selectedResource.id
                      ]?.cpu_usage_percent ?? 0
                    )}`}
                    style={{
                      width: `${
                        metricsData[
                          selectedResource.id
                        ]?.cpu_usage_percent ?? 0
                      }%`
                    }}
                  />
                </div>

              </div>

              <div className="metric-detail">

                <div className="metric-label">
                  <span>Memory Usage</span>

                  <strong>
                    {metricsData[
                      selectedResource.id
                    ]?.memory_usage_percent ?? 0}%
                  </strong>
                </div>

                <div className="progress-track large">
                  <div
                    className={`progress-bar ${getProgressClass(
                      metricsData[
                        selectedResource.id
                      ]?.memory_usage_percent ?? 0
                    )}`}
                    style={{
                      width: `${
                        metricsData[
                          selectedResource.id
                        ]?.memory_usage_percent ?? 0
                      }%`
                    }}
                  />
                </div>

              </div>

              <div className="metric-detail">

                <div className="metric-label">
                  <span>Storage Usage</span>

                  <strong>
                    {metricsData[
                      selectedResource.id
                    ]?.storage_usage_percent ?? 0}%
                  </strong>
                </div>

                <div className="progress-track large">
                  <div
                    className={`progress-bar ${getProgressClass(
                      metricsData[
                        selectedResource.id
                      ]?.storage_usage_percent ?? 0
                    )}`}
                    style={{
                      width: `${
                        metricsData[
                          selectedResource.id
                        ]?.storage_usage_percent ?? 0
                      }%`
                    }}
                  />
                </div>

              </div>

            </div>

          </div>
        </div>
      )}

    </div>
  )
}

export default Dashboard