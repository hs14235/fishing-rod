import { useEffect, useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api.js'

const STATUSES = ['draft', 'applied', 'interview', 'rejected', 'archived']

const STATUS_CLASS = {
  draft:     'status-draft',
  applied:   'status-applied',
  interview: 'status-interview',
  rejected:  'status-rejected',
  archived:  'status-archived',
}

export default function ApplicationDetail() {
  const { id }  = useParams()
  const navigate = useNavigate()

  const [app, setApp]                   = useState(null)
  const [editedCL, setEditedCL]         = useState('')
  const [editedNotes, setEditedNotes]   = useState('')
  const [editedStatus, setEditedStatus] = useState('draft')
  const [loading, setLoading]           = useState(true)
  const [saving, setSaving]             = useState(false)
  const [regenerating, setRegenerating] = useState(false)
  const [error, setError]               = useState(null)
  const [saveMsg, setSaveMsg]           = useState('')
  const [copied, setCopied]             = useState(false)
  const [showGenerated, setShowGenerated] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.getApplication(id)
      setApp(data)
      setEditedCL(data.edited_cover_letter || data.generated_cover_letter || '')
      setEditedNotes(data.edited_notes || '')
      setEditedStatus(data.status || 'draft')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => { load() }, [load])

  const handleSave = async () => {
    setSaving(true)
    setError(null)
    setSaveMsg('')
    try {
      await api.updateApplication(id, {
        edited_cover_letter: editedCL,
        edited_notes:        editedNotes,
        status:              editedStatus,
      })
      setSaveMsg('Saved.')
      setTimeout(() => setSaveMsg(''), 2500)
    } catch (e) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  const handleRegenerate = async () => {
    if (!confirm('Regenerate will overwrite the generated cover letter (your edits are kept). Continue?')) return
    setRegenerating(true)
    setError(null)
    try {
      const updated = await api.regenerateApplication(id)
      setApp(updated)
      // Replace edited cover letter with the freshly generated one
      setEditedCL(updated.generated_cover_letter || '')
    } catch (e) {
      setError(e.message)
    } finally {
      setRegenerating(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Delete this application? This cannot be undone.')) return
    try {
      await api.deleteApplication(id)
      navigate('/')
    } catch (e) {
      setError(e.message)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(editedCL)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleResetCL = () => {
    if (app) setEditedCL(app.generated_cover_letter || '')
  }

  if (loading) return <div className="page"><p className="muted">Loading…</p></div>
  if (!app && error) return <div className="page"><div className="error">{error}</div></div>
  if (!app) return null

  let keywords = []
  let suggestions = []
  try { keywords    = JSON.parse(app.detected_keywords_json || '[]') } catch {}
  try { suggestions = JSON.parse(app.generated_resume_suggestions_json || '[]') } catch {}

  const wordCount = editedCL.split(/\s+/).filter(Boolean).length

  return (
    <div className="page">
      {/* ── Header ─────────────────────────────────────────────── */}
      <div className="page-header">
        <div>
          <h1>{app.company_name}</h1>
          <div className="muted">{app.job_title}</div>
        </div>
        <div className="btn-group">
          <select
            className="input"
            style={{ width: 'auto' }}
            value={editedStatus}
            onChange={e => setEditedStatus(e.target.value)}
          >
            {STATUSES.map(s => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
          <button
            className="btn btn-primary"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? 'Saving…' : saveMsg || 'Save Changes'}
          </button>
          <button
            className="btn btn-outline"
            onClick={handleRegenerate}
            disabled={regenerating}
          >
            {regenerating ? 'Regenerating…' : 'Regenerate'}
          </button>
          <button className="btn btn-danger" onClick={handleDelete}>
            Delete
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="two-col">
        {/* ── Left: editable cover letter + notes ─────────────── */}
        <div>
          <section>
            <div className="section-header">
              <h3>Cover Letter</h3>
              <div className="btn-group">
                <button className="btn btn-sm btn-primary" onClick={handleCopy}>
                  {copied ? 'Copied!' : 'Copy'}
                </button>
                <button
                  className="btn btn-sm btn-outline"
                  onClick={() => setShowGenerated(v => !v)}
                >
                  {showGenerated ? 'Hide Original' : 'Show Original'}
                </button>
                <button className="btn btn-sm btn-outline" onClick={handleResetCL}>
                  Reset
                </button>
              </div>
            </div>

            {showGenerated && app.generated_cover_letter && (
              <div className="generated-view">
                <div className="label-muted">Generated (read-only)</div>
                <pre className="generated-text">{app.generated_cover_letter}</pre>
              </div>
            )}

            <textarea
              className="input textarea-cover"
              value={editedCL}
              onChange={e => setEditedCL(e.target.value)}
              spellCheck
            />
            <div className="word-count muted">{wordCount} words</div>
          </section>

          <section>
            <h3>Notes</h3>
            <textarea
              className="input textarea-sm"
              value={editedNotes}
              onChange={e => setEditedNotes(e.target.value)}
              placeholder="Recruiter name, interview prep notes, deadlines…"
            />
          </section>
        </div>

        {/* ── Right: keywords, fit summary, suggestions, meta ─── */}
        <div>
          <section>
            <h3>Detected Keywords</h3>
            <div className="keywords">
              {keywords.map(k => (
                <span key={k} className="keyword-badge">{k}</span>
              ))}
              {keywords.length === 0 && (
                <span className="muted small">None</span>
              )}
            </div>
          </section>

          <section>
            <h3>Fit Summary</h3>
            <p className="fit-summary">{app.fit_summary || '—'}</p>
          </section>

          <section>
            <h3>Resume Suggestions</h3>
            {suggestions.length > 0 ? (
              <ol className="suggestions">
                {suggestions.map((s, i) => <li key={i}>{s}</li>)}
              </ol>
            ) : (
              <p className="muted small">None saved.</p>
            )}
          </section>

          <section className="meta-section">
            <h3>Details</h3>
            <div className="meta-grid">
              <div className="meta-row">
                <span className="muted">Status</span>
                <span>
                  <span className={`status-badge ${STATUS_CLASS[editedStatus] || 'status-draft'}`}>
                    {editedStatus}
                  </span>
                </span>
              </div>
              <div className="meta-row">
                <span className="muted">Tone</span>
                <span>{app.tone}</span>
              </div>
              <div className="meta-row">
                <span className="muted">Emphasis</span>
                <span>{app.emphasis}</span>
              </div>
              <div className="meta-row">
                <span className="muted">Created</span>
                <span>{new Date(app.created_at).toLocaleDateString()}</span>
              </div>
              <div className="meta-row">
                <span className="muted">Updated</span>
                <span>{new Date(app.updated_at).toLocaleDateString()}</span>
              </div>
            </div>
          </section>

          <section>
            <details>
              <summary className="muted">Job Description</summary>
              <pre className="jd-text">{app.job_description}</pre>
            </details>
          </section>
        </div>
      </div>
    </div>
  )
}
