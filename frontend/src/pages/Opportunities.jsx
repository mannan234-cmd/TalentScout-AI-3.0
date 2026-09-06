import React, { useEffect, useState } from 'react'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import LoadingState from '../components/LoadingState'

const EMPTY = { title: '', organization: '', type: 'internship', description: '', required_skills: '', location: 'Remote' }

export default function Opportunities() {
  const { isAdmin } = useAuth()
  const [opportunities, setOpportunities] = useState([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState(EMPTY)
  const [showForm, setShowForm] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  async function load() {
    setLoading(true)
    try {
      const res = await api.get('/opportunities')
      setOpportunities(res.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  async function handleCreate(e) {
    e.preventDefault()
    setSubmitting(true)
    try {
      await api.post('/opportunities', {
        ...form,
        required_skills: form.required_skills.split(',').map((s) => s.trim()).filter(Boolean),
      })
      setForm(EMPTY)
      setShowForm(false)
      load()
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create opportunity')
    } finally {
      setSubmitting(false)
    }
  }

  const TYPE_COLORS = {
    internship: 'bg-blue-50 text-blue-600',
    scholarship: 'bg-purple-50 text-purple-600',
    job: 'bg-emerald-50 text-emerald-600',
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-1">
        <h1 className="text-2xl font-bold text-slate-900">Opportunities</h1>
        {isAdmin && (
          <button className="btn-primary" onClick={() => setShowForm((s) => !s)}>
            {showForm ? 'Cancel' : '+ New Opportunity'}
          </button>
        )}
      </div>
      <p className="text-slate-500 mb-6">Internships, scholarships, and jobs the Matching Agent evaluates candidates against.</p>

      {showForm && (
        <form onSubmit={handleCreate} className="card mb-6 space-y-3">
          <div className="grid sm:grid-cols-2 gap-3">
            <div>
              <label className="label">Title</label>
              <input className="input" required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            </div>
            <div>
              <label className="label">Organization</label>
              <input className="input" required value={form.organization} onChange={(e) => setForm({ ...form, organization: e.target.value })} />
            </div>
          </div>
          <div className="grid sm:grid-cols-2 gap-3">
            <div>
              <label className="label">Type</label>
              <select className="input" value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}>
                <option value="internship">Internship</option>
                <option value="scholarship">Scholarship</option>
                <option value="job">Job</option>
              </select>
            </div>
            <div>
              <label className="label">Location</label>
              <input className="input" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} />
            </div>
          </div>
          <div>
            <label className="label">Required Skills (comma-separated)</label>
            <input className="input" required placeholder="python, sql, excel" value={form.required_skills} onChange={(e) => setForm({ ...form, required_skills: e.target.value })} />
          </div>
          <div>
            <label className="label">Description</label>
            <textarea className="input" rows={3} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          </div>
          <button className="btn-primary" disabled={submitting}>{submitting ? 'Creating…' : 'Create Opportunity'}</button>
        </form>
      )}

      {loading ? <LoadingState /> : (
        <div className="grid sm:grid-cols-2 gap-4">
          {opportunities.map((o) => (
            <div key={o.id} className="card">
              <div className="flex items-start justify-between">
                <h3 className="font-semibold text-slate-900">{o.title}</h3>
                <span className={`badge ${TYPE_COLORS[o.type]}`}>{o.type}</span>
              </div>
              <p className="text-sm text-slate-500">{o.organization} · {o.location}</p>
              <p className="text-sm text-slate-600 mt-2">{o.description}</p>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {o.required_skills.map((s) => <span key={s} className="badge bg-slate-100 text-slate-600">{s}</span>)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
