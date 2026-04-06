import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api.js'

const TONES    = ['balanced', 'concise', 'confident', 'technical']
const EMPHASES = ['auto', 'backend', 'full-stack', 'ai-ml', 'platform', 'leadership']

const EMPTY_FORM = {
  company_name:       '',
  job_title:          '',
  job_description:    '',
  company_notes:      '',
  tone:               'balanced',
  emphasis:           'auto',
  extra_instructions: '',
}

export default function NewApplication() {
  const navigate = useNavigate()

  const [form, setForm]           = useState(EMPTY_FORM)
  const [result, setResult]       = useState(null)
  const [editedCL, setEditedCL]   = useState('')
  const [editedNotes, setEditedNotes] = useState('')
  const [generating, setGenerating] = useState(false)
  const [saving, setSaving]       = useState(false)
  const [error, setError]         = useState(null)
  const [copied, setCopied]       = useState(false)

  const set = field => e => setForm(f => ({ ...f, [field]: e.target.value }))

  const handleGenerate = async e => {
    e.preventDefault()
    if (!form.company_name.trim() || !form.job_title.trim() || !form.job_description.trim()) {
      setError('Company, job title, and job description are required.')
      return
    }
    setGenerating(true)
    setError(null)
    try {
      const data = await api.generate(form)
      setResult(data)
      setEditedCL(data.generated_cover_letter)
      setEditedNotes('')
    } catch (e) {
      setError(e.message)
    } finally {
      setGenerating(false)
    }
  }

  const handleSave = async () => {
    if (!result) return
    setSaving(true)
    setError(null)
    try {
      const app = await api.createApplication({
        ...form,
        detected_keywords_json:             JSON.stringify(result.keywords),
        fit_summary:                        result.fit_summary,
        generated_cover_letter:             result.generated_cover_letter,
        edited_cover_letter:                editedCL,
        generated_resume_suggestions_json:  JSON.stringify(result.resume_suggestions),
        edited_notes:                       editedNotes,        status:                             'draft',
      })
      navigate(`/applications/${app.id}`)
    } catch (e) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(editedCL)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleReset = () => {
    if (result) setEditedCL(result.generated_cover_letter)
  }

  const wordCount = editedCL.split(/\s+/).filter(Boolean).length

  return (
    <div className="page">
      <div className="page-header">
        <h1>New Application</h1>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="two-col">
        {/* ── Left: input form ─────────────────────────────────── */}
        <div>
          <form onSubmit={handleGenerate}>
            <div className="field">
              <label htmlFor="company_name">Company *</label>
              <input
                id="company_name"
                className="input"
                value={form.company_name}
                onChange={set('company_name')}
                placeholder="e.g. Stripe"
              />
            </div>

            <div className="field">
              <label htmlFor="job_title">Job Title *</label>
              <input
                id="job_title"
                className="input"
                value={form.job_title}
                onChange={set('job_title')}
                placeholder="e.g. Backend Software Engineer"
              />
            </div>

            <div className="field">
              <label htmlFor="jd">Job Description *</label>
              <textarea
                id="jd"
                className="input textarea-lg"
                value={form.job_description}
                onChange={set('job_description')}
                placeholder="Paste the full job description here…"
              />
            </div>

            <div className="field">
              <label htmlFor="notes">
                Company Notes{' '}
                <span className="muted">(optional)</span>
              </label>
              <textarea
                id="notes"
                className="input textarea-sm"
                value={form.company_notes}
                onChange={set('company_notes')}
                placeholder="e.g. They value systems-thinking; fintech infra focus"
              />
            </div>

            <div className="row-fields">
              <div className="field">
                <label htmlFor="tone">Tone</label>
                <select
                  id="tone"
                  className="input"
                  value={form.tone}
                  onChange={set('tone')}
                >
                  {TONES.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <div className="field">
                <label htmlFor="emphasis">Emphasis</label>
                <select
                  id="emphasis"
                  className="input"
                  value={form.emphasis}
                  onChange={set('emphasis')}
                >
                  {EMPHASES.map(e => <option key={e} value={e}>{e}</option>)}
                </select>
              </div>
            </div>

            <div className="field">
              <label htmlFor="extra">
                Extra Instructions{' '}
                <span className="muted">(optional)</span>
              </label>
              <input
                id="extra"
                className="input"
                value={form.extra_instructions}
                onChange={set('extra_instructions')}
                placeholder="e.g. Emphasise team lead experience; keep it under 250 words"
              />
            </div>

            <div className="btn-group">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={generating}
              >
                {generating ? 'Generating…' : 'Generate'}
              </button>
              {result && (
                <button
                  type="button"
                  className="btn btn-outline"
                  onClick={handleGenerate}
                  disabled={generating}
                >
                  Regenerate
                </button>
              )}
            </div>
          </form>
        </div>

        {/* ── Right: output panel ──────────────────────────────── */}
        <div>
          {!result && !generating && (
            <div className="placeholder-msg">
              Fill in the form and click <strong>Generate</strong> to see
              your cover letter and resume suggestions.
            </div>
          )}

          {generating && (
            <div className="placeholder-msg">Generating…</div>
          )}

          {result && (
            <>
              <section>
                <h3>Detected Keywords</h3>
                <div className="keywords">
                  {result.keywords.map(k => (
                    <span key={k} className="keyword-badge">{k}</span>
                  ))}
                  {result.keywords.length === 0 && (
                    <span className="muted small">None detected</span>
                  )}
                </div>
              </section>

              <section>
                <h3>Fit Summary</h3>
                <p className="fit-summary">{result.fit_summary}</p>
              </section>

              <section>
                <div className="section-header">
                  <h3>Cover Letter</h3>
                  <div className="btn-group">
                    <button className="btn btn-sm btn-primary" onClick={handleCopy}>
                      {copied ? 'Copied!' : 'Copy'}
                    </button>
                    <button className="btn btn-sm btn-outline" onClick={handleReset}>
                      Reset
                    </button>
                  </div>
                </div>
                <textarea
                  className="input textarea-cover"
                  value={editedCL}
                  onChange={e => setEditedCL(e.target.value)}
                  spellCheck
                />
                <div className="word-count muted">{wordCount} words</div>
              </section>

              <section>
                <h3>Resume Suggestions</h3>
                <ol className="suggestions">
                  {result.resume_suggestions.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ol>
              </section>

              <section>
                <h3>Notes</h3>
                <textarea
                  className="input textarea-sm"
                  value={editedNotes}
                  onChange={e => setEditedNotes(e.target.value)}
                  placeholder="Personal notes about this application (recruiter name, deadlines, etc.)"
                />
              </section>

              <div className="btn-group">
                <button
                  className="btn btn-primary"
                  onClick={handleSave}
                  disabled={saving}
                >
                  {saving ? 'Saving…' : 'Save Application'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
