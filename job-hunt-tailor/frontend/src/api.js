const BASE = '/api'

async function request(method, path, body) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  }
  if (body !== undefined) opts.body = JSON.stringify(body)

  const res = await fetch(BASE + path, opts)

  if (res.status === 204) return null

  const data = await res.json().catch(() => ({ detail: res.statusText }))

  if (!res.ok) {
    throw new Error(data.detail || `Request failed: ${res.status}`)
  }

  return data
}

export const api = {
  generate: (data) => request('POST', '/generate', data),

  listApplications: (params = {}) => {
    const qs = new URLSearchParams(
      Object.fromEntries(
        Object.entries(params).filter(([, v]) => v !== undefined && v !== ''),
      ),
    ).toString()
    return request('GET', `/applications${qs ? '?' + qs : ''}`)
  },

  getApplication:      (id)       => request('GET',    `/applications/${id}`),
  createApplication:   (data)     => request('POST',   '/applications', data),
  updateApplication:   (id, data) => request('PUT',    `/applications/${id}`, data),
  deleteApplication:   (id)       => request('DELETE', `/applications/${id}`),
  regenerateApplication: (id)     => request('POST',   `/applications/${id}/regenerate`),

  getSettings:    ()     => request('GET', '/settings'),
  updateSettings: (data) => request('PUT', '/settings', data),
}
