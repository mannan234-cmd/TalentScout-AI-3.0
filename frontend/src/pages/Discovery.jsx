import React, { useEffect, useState } from 'react'
import api from '../services/api'
import StudentCard from '../components/StudentCard'
import LoadingState from '../components/LoadingState'

const STATUS_FILTERS = ['all', 'new', 'processing', 'pending_review', 'approved', 'rejected']

export default function Discovery() {
  const [students, setStudents] = useState([])
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      setLoading(true)
      try {
        const res = await api.get('/students', { params: filter === 'all' ? {} : { status: filter } })
        setStudents(res.data)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [filter])

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-1">Discovery</h1>
      <p className="text-slate-500 mb-6">All student submissions, auto-categorized by the Discovery Agent.</p>

      <div className="flex gap-2 mb-6 overflow-x-auto">
        {STATUS_FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`btn-secondary whitespace-nowrap ${filter === f ? '!bg-brand-600 !text-white' : ''}`}
          >
            {f.replace('_', ' ')}
          </button>
        ))}
      </div>

      {loading ? <LoadingState /> : (
        students.length === 0 ? (
          <p className="text-slate-500">No students found for this filter.</p>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {students.map((s) => <StudentCard key={s.id} student={s} />)}
          </div>
        )
      )}
    </div>
  )
}
