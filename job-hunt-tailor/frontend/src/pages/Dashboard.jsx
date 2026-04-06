import { useEffect, useState, useCallback } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../api.js'

const STATUS_CLASS = {
  draft:     'status-draft',
  applied:   'status-applied',
  interview: 'status-interview',
  rejected:  'status-rejected',
  archived:  'status-archived',
}

export default function Dashboard() {
  const [apps, setApps]       = useState([])
  const [search, setSearch]   = useState('')
  const [status, setStatus]   = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)
  const navigate = useNavigate()

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.listApplications({
        search: search || undefined,
        status: status || undefined,
      })
      setApps(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [search, status])

  useEffect(() => { load() }, [load])

  return (
    <div className="page">
      <div className="page-header">
        <h1>Applications</h1>
        <Link to="/new" className="btn btn-primary">+ New</Link>
      </div>

      <div className="filters">
        <input
          type="search"
          className="input"
          placeholder="Search by company or role…"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <select
          className="input"
          style={{ width: 'auto' }}
          value={status}
          onChange={e => setStatus(e.target.value)}
        >
          <option value="">All statuses</option>
          <option value="draft">Draft</option>
          <option value="applied">Applied</option>
          <option value="interview">Interview</option>
          <option value="rejected">Rejected</option>
          <option value="archived">Archived</option>
        </select>
      </div>

      {error && <div className="error">{error}</div>}
      {loading && <p className="muted">Loading…</p>}

      {!loading && apps.length === 0 && (
        <div className="empty">
          No applications yet.{' '}
          <Link to="/new">Generate your first one.</Link>
        </div>
      )}

      {!loading && apps.length > 0 && (
        <div className="app-list">
          {apps.map(app => (
            <div
              key={app.id}
              className="app-card"
              onClick={() => navigate(`/applications/${app.id}`)}
            >
              <div className="app-card-main">
                <span className="app-company">{app.company_name}</span>
                <span className="app-role">{app.job_title}</span>
              </div>
              <div className="app-card-meta">
                <span className={`status-badge ${STATUS_CLASS[app.status] || 'status-draft'}`}>
                  {app.status}
                </span>
                <span className="muted small">
                  {new Date(app.updated_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
