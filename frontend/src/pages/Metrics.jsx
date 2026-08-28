import { useEffect, useState } from 'react'

const API_BASE_URL = 'http://127.0.0.1:8000'

function Metrics() {
  const [resources, setResources] = useState([])
  const [metricsData, setMetricsData] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchMetricsData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch all resources
      const resourcesResponse = await fetch(
        `${API_BASE_URL}/resources/`
      )

      if (!resourcesResponse.ok) {
        throw new Error('Failed to fetch resources')
      }

      const resourcesData = await resourcesResponse.json()

      setResources(resourcesData)

      // Fetch latest metrics for every resource
      const metricsResults = {}

      await Promise.all(
        resourcesData.map(async (resource) => {
          try {
            const metricsResponse = await fetch(
              `${API_BASE_URL}/resources/${resource.id}/metrics/latest`
            )

            if (metricsResponse.ok) {
              const metrics = await metricsResponse.json()

              metricsResults[resource.id] = metrics
            } else {
              metricsResults[resource.id] = null
            }
          } catch {
            metricsResults[resource.id] = null
          }
        })
      )

      setMetricsData(metricsResults)

    } catch (err) {
      console.error('API Error:', err)

      setError('Unable to connect to the CloudOps API')

      setResources([])
      setMetricsData({})

    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMetricsData()
  }, [])

  return (
    <div className="metrics-page">

      {/* HEADER */}

      <div className="metrics-header">
        <div>
          <h1>Metrics</h1>

          <p>
            Monitor CPU, memory, and storage usage
          </p>
        </div>

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
      </div>

      {/* ERROR MESSAGE */}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* METRICS TABLE */}

      <section className="metrics-section">

        <div className="metrics-table">

          <div className="metrics-table-header">
            <span>RESOURCE</span>
            <span>CPU USAGE</span>
            <span>MEMORY USAGE</span>
            <span>STORAGE USAGE</span>
            <span>LAST UPDATED</span>
          </div>

          {loading && (
            <div className="empty-state">
              Loading metrics...
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
              const metrics = metricsData[resource.id]

              return (
                <div
                  className="metrics-table-row"
                  key={resource.id}
                >
                  {/* RESOURCE */}

                  <div className="metric-resource">
                    <span className="resource-type-icon">
                      VM
                    </span>

                    <strong>
                      {resource.name}
                    </strong>
                  </div>

                  {/* CPU */}

                  <div className="metric-value">
                    {metrics
                      ? `${metrics.cpu_usage_percent}%`
                      : 'No data'}
                  </div>

                  {/* MEMORY */}

                  <div className="metric-value">
                    {metrics
                      ? `${metrics.memory_usage_percent}%`
                      : 'No data'}
                  </div>

                  {/* STORAGE */}

                  <div className="metric-value">
                    {metrics
                      ? `${metrics.storage_usage_percent}%`
                      : 'No data'}
                  </div>

                  {/* LAST UPDATED */}

                  <div className="metric-time">
                    {metrics?.recorded_at
                      ? new Date(
                          metrics.recorded_at
                        ).toLocaleString()
                      : 'No data'}
                  </div>

                </div>
              )
            })}

        </div>

      </section>

    </div>
  )
}

export default Metrics