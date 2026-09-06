import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import LoadingState from '../components/LoadingState'

export default function HumanReview() {
  const [queue, setQueue] = useState([])
  const [loading, setLoading] = useState(true)
  const [busyId, setBusyId] = useState(null)
  const [notes, setNotes] = useState({})

  async function load() {
    setLoading(true)
    try {
      const res = await api.get('/review/queue')
      setQueue(res.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  async function decide(studentId, decision) {
    setBusyId(studentId)
    try {
      await api.post(`/review/${studentId}/decision`, { decision, notes: notes[studentId] || '' })
      setQueue((q) => q.filter((s) => s.student_id !== studentId))
    } catch (err) {
      alert(err.response?.data?.detail || 'Action failed')
    } finally {
      setBusyId(null)
    }
  }

  if (loading) return <LoadingState />

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-1">Human Review Queue</h1>
      <p className="text-slate-500 mb-6">
        AI has produced advisory recommendations for these candidates. Approving
        unblocks Matching &amp; Application Support automatically.
      </p>

      {queue.length === 0 ? (
        <p className="text-slate-500">🎉 Nothing pending review right now.</p>
      ) : (
        <div className="space-y-4">
          {queue.map((s) => (
            <div key={s.student_id} className="card">
              <div className="flex items-start justify-between gap-4 mb-3">
                <div>
                  <Link to={`/students/${s.student_id}`} className="font-semibold text-slate-900 hover:underline">
                    {s.full_name}
                  </Link>
                  <p className="text-sm text-slate-500">{s.email}</p>
                  <p className="text-sm text-slate-500">Category: {s.category || '—'}</p>
                </div>
                <div className="text-right">
                  <div className={`font-bold ${s.is_high_potential ? 'text-emerald-600' : 'text-slate-700'}`}>
                    {s.potential_score} {s.is_high_potential && '🌟'}
                  </div>
                  <div className="text-xs text-slate-400">potential score</div>
                </div>
              </div>
              <textarea
                className="input mb-3"
                rows={2}
                placeholder="Optional review notes…"
                value={notes[s.student_id] || ''}
                onChange={(e) => setNotes((n) => ({ ...n, [s.student_id]: e.target.value }))}
              />
              <div className="flex gap-3">
                <button className="btn-success flex-1" disabled={busyId === s.student_id} onClick={() => decide(s.student_id, 'approve')}>
                  ✅ Approve
                </button>
                <button className="btn-danger flex-1" disabled={busyId === s.student_id} onClick={() => decide(s.student_id, 'reject')}>
                  ❌ Reject
                </button>
                <Link to={`/students/${s.student_id}`} className="btn-secondary flex-1 text-center">
                  View Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
