import { useEffect, useState } from 'react'
import { api } from '../api.js'

const TONES    = ['balanced', 'concise', 'confident', 'technical']
const EMPHASES = ['auto', 'backend', 'full-stack', 'ai-ml', 'platform', 'leadership']

export default function Settings() {
  const [form, setForm]     = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving]   = useState(false)
  const [saveMsg, setSaveMsg] = useState('')
  const [error, setError]     = useState(null)

  useEffect(() => {
    api.getSettings()
      .then(data => { setForm(data); setLoading(false) })
      .catch(e  => { setError(e.message); setLoading(false) })
  }, [])

  const set = field => e => setForm(f => ({ ...f, [field]: e.target.value }))

  const handleSave = async e => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    setSaveMsg('')
    try {
      const updated = await api.updateSettings({
        master_profile_text:  form.master_profile_text,
        fixed_philosophy_text: form.fixed_philosophy_text,
        strengths_block_text:  form.strengths_block_text,
        closing_block_text:    form.closing_block_text,
        default_tone:          form.default_tone,
        default_emphasis:      form.default_emphasis,
      })
      setForm(updated)
      setSaveMsg('Saved.')
      setTimeout(() => setSaveMsg(''), 2500)
    } catch (e) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="page"><p className="muted">Loading…</p></div>
  if (!form)   return <div className="page"><div className="error">{error}</div></div>

  return (
    <div className="page settings-page">
      <div className="page-header">
        <h1>Profile &amp; Settings</h1>
      </div>

      <p className="muted" style={{ marginBottom: '24px' }}>
        Changes here affect all future generations. The philosophy and closing blocks appear
        verbatim in every cover letter — edit them to match your voice.
      </p>

      {error   && <div className="error">{error}</div>}
      {saveMsg && <div className="notice">{saveMsg}</div>}

      <form onSubmit={handleSave}>
        <div className="field">
          <label htmlFor="profile">Master Profile</label>
          <div className="field-hint muted">
            Canonical source of truth for your experience. Used by LLM providers as context.
            Do not add things not in your actual resume.
          </div>
          <textarea
            id="profile"
            className="input textarea-xl"
            value={form.master_profile_text}
            onChange={set('master_profile_text')}
          />
        </div>

        <div className="field">
          <label htmlFor="philosophy">
            Engineering Philosophy Block{' '}
            <span className="muted">(80% fixed section)</span>
          </label>
          <div className="field-hint muted">
            This paragraph appears in every generated cover letter. Keep it under 80 words.
            Edit to reflect your actual thinking, not what sounds impressive.
          </div>
          <textarea
            id="philosophy"
            className="input textarea-md"
            value={form.fixed_philosophy_text}
            onChange={set('fixed_philosophy_text')}
          />
        </div>

        <div className="field">
          <label htmlFor="strengths">
            Strengths Block{' '}
            <span className="muted">(optional)</span>
          </label>
          <div className="field-hint muted">
            Used as context for project emphasis in future versions. Edit to reflect
            what you genuinely want to highlight.
          </div>
          <textarea
            id="strengths"
            className="input textarea-md"
            value={form.strengths_block_text}
            onChange={set('strengths_block_text')}
          />
        </div>

        <div className="field">
          <label htmlFor="closing">Closing Paragraph</label>
          <div className="field-hint muted">
            Appears at the end of every cover letter. Keep it short and direct.
          </div>
          <textarea
            id="closing"
            className="input textarea-sm"
            value={form.closing_block_text}
            onChange={set('closing_block_text')}
          />
        </div>

        <div className="row-fields">
          <div className="field">
            <label htmlFor="tone">Default Tone</label>
            <select
              id="tone"
              className="input"
              value={form.default_tone}
              onChange={set('default_tone')}
            >
              {TONES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="field">
            <label htmlFor="emphasis">Default Emphasis</label>
            <select
              id="emphasis"
              className="input"
              value={form.default_emphasis}
              onChange={set('default_emphasis')}
            >
              {EMPHASES.map(e => <option key={e} value={e}>{e}</option>)}
            </select>
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={saving}
        >
          {saving ? 'Saving…' : saveMsg || 'Save Settings'}
        </button>
      </form>
    </div>
  )
}
