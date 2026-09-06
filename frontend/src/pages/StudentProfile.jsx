import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import LoadingState from '../components/LoadingState'
import EvidenceCard from '../components/EvidenceCard'
import SignalCard from '../components/SignalCard'
import ReviewPanel from '../components/ReviewPanel'

const EMPTY = {
  full_name: '', email: '', university: '', degree_program: '',
  graduation_year: new Date().getFullYear() + 1, skills: '', bio: '',
  portfolio_url: '', evidence_text: '',
}

export default function StudentProfile() {
  const { id } = useParams() // present only on the admin detail route /students/:id
  const { isAdmin } = useAuth()

  if (id && isAdmin) return <AdminStudentDetail id={id} />
  return <SelfSubmitForm />
}

// ---------------------------------------------------------------------------
// Admin / reviewer view of a single candidate: profile + evidence + AI
// signals + (if applicable) the human review decision panel.
// ---------------------------------------------------------------------------
function AdminStudentDetail({ id }) {
  const [student, setStudent] = useState(null)
  const [evidence, setEvidence] = useState([])
  const [signals, setSignals] = useState(null)
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)

  async function load() {
    setLoading(true)
    try {
      const [sRes, eRes] = await Promise.all([
        api.get(`/students/${id}`),
        api.get(`/students/${id}/evidence`),
      ])
      setStudent(sRes.data)
      setEvidence(eRes.data)
      try {
        const sigRes = await api.get(`/students/${id}/signals`)
        setSignals(sigRes.data)
      } catch { /* no signal report yet */ }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [id])

  async function handleDecision(decision, notes) {
    setBusy(true)
    try {
      await api.post(`/review/${id}/decision`, { decision, notes })
      await load()
    } catch (err) {
      alert(err.response?.data?.detail || 'Action failed')
    } finally {
      setBusy(false)
    }
  }

  if (loading) return <LoadingState />
  if (!student) return <p className="text-center py-16 text-slate-500">Student not found.</p>

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
      <div className="card">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-xl font-bold text-slate-900">{student.full_name}</h1>
            <p className="text-slate-500">{student.email}</p>
            <p className="text-slate-500">{student.university} · {student.degree_program} · Class of {student.graduation_year}</p>
          </div>
          <span className="badge bg-slate-100 text-slate-600 capitalize">{student.status.replace('_', ' ')}</span>
        </div>
        {student.bio && <p className="text-sm text-slate-600 mt-3">{student.bio}</p>}
        {student.portfolio_url && (
          <a href={student.portfolio_url} target="_blank" rel="noreferrer" className="text-sm text-brand-600 mt-2 inline-block">
            🔗 {student.portfolio_url}
          </a>
        )}
        <div className="mt-3 flex flex-wrap gap-1.5">
          {student.skills?.map((s) => <span key={s} className="badge bg-slate-100 text-slate-600">{s}</span>)}
        </div>
      </div>

      <SignalCard report={signals} />

      {evidence.length > 0 && (
        <div>
          <h3 className="font-semibold text-slate-900 mb-2">Submitted Evidence</h3>
          <div className="space-y-3">
            {evidence.map((e) => <EvidenceCard key={e.id} item={e} />)}
          </div>
        </div>
      )}

      {student.status === 'pending_review' && (
        <ReviewPanel
          student={student}
          busy={busy}
          onApprove={(notes) => handleDecision('approve', notes)}
          onReject={(notes) => handleDecision('reject', notes)}
        />
      )}
      {student.status === 'approved' && (
        <div className="card bg-emerald-50 border-emerald-100 text-emerald-800 text-sm">
          ✅ Approved by reviewer{student.reviewed_by ? '' : ''}. Matching has run automatically.
        </div>
      )}
      {student.status === 'rejected' && (
        <div className="card bg-red-50 border-red-100 text-red-800 text-sm">
          ❌ This candidate was rejected. {student.review_notes && `Notes: ${student.review_notes}`}
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Candidate's own submission / edit form (route: /student/profile)
// ---------------------------------------------------------------------------
function SelfSubmitForm() {
  const navigate = useNavigate()
  const [form, setForm] = useState(EMPTY)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [existing, setExisting] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get('/students/me/profile')
        const p = res.data
        setExisting(p)
        setForm({
          full_name: p.full_name, email: p.email, university: p.university,
          degree_program: p.degree_program, graduation_year: p.graduation_year,
          skills: p.skills.join(', '), bio: p.bio, portfolio_url: p.portfolio_url || '',
          evidence_text: p.evidence_text,
        })
      } catch {
        // no profile yet — fine, blank form
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await api.post('/students/submit', {
        ...form,
        graduation_year: Number(form.graduation_year),
        skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean),
      })
      navigate('/student')
    } catch (err) {
      const detail = err.response?.data?.detail
      setError(Array.isArray(detail) ? detail[0]?.msg : detail || 'Submission failed')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <LoadingState />

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-1">
        {existing ? 'Update Your Profile' : 'Submit Your Profile'}
      </h1>
      <p className="text-slate-500 mb-6">
        {existing
          ? 'Resubmitting will re-run the AI analysis and queue a fresh human review.'
          : 'Our Discovery, Evidence & Signals agents will analyze this automatically.'}
      </p>

      <form onSubmit={handleSubmit} className="card space-y-4">
        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="label">Full Name</label>
            <input className="input" required value={form.full_name} onChange={(e) => update('full_name', e.target.value)} />
          </div>
          <div>
            <label className="label">Email</label>
            <input className="input" type="email" required value={form.email} onChange={(e) => update('email', e.target.value)} />
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="label">University</label>
            <input className="input" required value={form.university} onChange={(e) => update('university', e.target.value)} />
          </div>
          <div>
            <label className="label">Degree Program</label>
            <input className="input" required value={form.degree_program} onChange={(e) => update('degree_program', e.target.value)} />
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="label">Graduation Year</label>
            <input className="input" type="number" required value={form.graduation_year} onChange={(e) => update('graduation_year', e.target.value)} />
          </div>
          <div>
            <label className="label">Portfolio / GitHub URL</label>
            <input className="input" value={form.portfolio_url} onChange={(e) => update('portfolio_url', e.target.value)} />
          </div>
        </div>

        <div>
          <label className="label">Skills (comma-separated)</label>
          <input className="input" placeholder="python, sql, data analysis" required value={form.skills} onChange={(e) => update('skills', e.target.value)} />
        </div>

        <div>
          <label className="label">Short Bio</label>
          <textarea className="input" rows={3} value={form.bio} onChange={(e) => update('bio', e.target.value)} />
        </div>

        <div>
          <label className="label">Evidence (projects, achievements, certificates — one per paragraph)</label>
          <textarea
            className="input"
            rows={6}
            placeholder={"Built a Power BI dashboard analyzing sales data using SQL and Python.\n\nWon 1st place in a university hackathon building a React web app."}
            value={form.evidence_text}
            onChange={(e) => update('evidence_text', e.target.value)}
          />
        </div>

        {error && <p className="text-sm text-red-600">{typeof error === 'string' ? error : JSON.stringify(error)}</p>}

        <button className="btn-primary w-full" disabled={submitting}>
          {submitting ? 'Submitting to AI pipeline…' : existing ? 'Resubmit Profile' : 'Submit Profile'}
        </button>
      </form>
    </div>
  )
}
