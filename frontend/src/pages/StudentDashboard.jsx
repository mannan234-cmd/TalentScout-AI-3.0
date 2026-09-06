import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import LoadingState from '../components/LoadingState'

export default function StudentDashboard() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [notFound, setNotFound] = useState(false)

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get('/students/me/profile')
        setProfile(res.data)
      } catch (err) {
        if (err.response?.status === 404) setNotFound(true)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) return <LoadingState />

  if (notFound || !profile) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center">
        <h2 className="text-xl font-bold text-slate-900 mb-2">No profile submitted yet</h2>
        <p className="text-slate-600 mb-6">
          Submit your profile and evidence so our AI agents can analyze your
          skills and match you with opportunities.
        </p>
        <Link to="/student/profile" className="btn-primary">Submit My Profile</Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-1">Welcome back, {profile.full_name.split(' ')[0]}</h1>
      <p className="text-slate-500 mb-6">Here's where your application stands.</p>

      <div className="grid sm:grid-cols-3 gap-4 mb-6">
        <div className="card text-center">
          <div className="text-lg font-bold text-slate-900 capitalize">{profile.status.replace('_', ' ')}</div>
          <div className="text-xs text-slate-500 mt-1">Application Status</div>
        </div>
        <div className="card text-center">
          <div className="text-lg font-bold text-brand-700">{profile.potential_score ?? '—'}</div>
          <div className="text-xs text-slate-500 mt-1">Potential Score</div>
        </div>
        <div className="card text-center">
          <div className="text-lg font-bold text-slate-900">{profile.category || '—'}</div>
          <div className="text-xs text-slate-500 mt-1">Category</div>
        </div>
      </div>

      <div className="card mb-6">
        <h3 className="font-semibold mb-2">Pipeline Status</h3>
        <PipelineTimeline status={profile.status} />
      </div>

      <div className="flex gap-3">
        <Link to="/student/profile" className="btn-secondary">View / Edit Profile</Link>
        <Link to="/matches" className="btn-primary">View My Matches</Link>
      </div>
    </div>
  )
}

function PipelineTimeline({ status }) {
  const steps = [
    { key: 'new', label: 'Submitted' },
    { key: 'processing', label: 'AI Analysis' },
    { key: 'pending_review', label: 'Human Review' },
    { key: 'approved', label: 'Approved & Matched' },
  ]
  const order = ['new', 'processing', 'pending_review', 'approved']
  const currentIdx = status === 'rejected' ? -1 : order.indexOf(status)

  return (
    <div className="flex items-center">
      {steps.map((s, idx) => (
        <React.Fragment key={s.key}>
          <div className="flex flex-col items-center flex-1">
            <div className={`h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold
              ${idx <= currentIdx ? 'bg-brand-600 text-white' : 'bg-slate-200 text-slate-500'}`}>
              {idx + 1}
            </div>
            <span className="text-xs text-slate-500 mt-1 text-center">{s.label}</span>
          </div>
          {idx < steps.length - 1 && (
            <div className={`h-0.5 flex-1 -mt-5 ${idx < currentIdx ? 'bg-brand-600' : 'bg-slate-200'}`} />
          )}
        </React.Fragment>
      ))}
      {status === 'rejected' && (
        <span className="badge bg-red-50 text-red-600 ml-3">Rejected</span>
      )}
    </div>
  )
}
