import React from 'react'
import { Link } from 'react-router-dom'

const STATUS_STYLES = {
  new: 'bg-slate-100 text-slate-600',
  processing: 'bg-amber-50 text-amber-600',
  pending_review: 'bg-blue-50 text-blue-600',
  approved: 'bg-emerald-50 text-emerald-600',
  rejected: 'bg-red-50 text-red-600',
}

export default function StudentCard({ student }) {
  return (
    <Link to={`/students/${student.id}`} className="card block hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-semibold text-slate-900">{student.full_name}</h3>
          <p className="text-sm text-slate-500">{student.university} · {student.degree_program}</p>
        </div>
        <span className={`badge ${STATUS_STYLES[student.status] || 'bg-slate-100 text-slate-600'}`}>
          {student.status.replace('_', ' ')}
        </span>
      </div>
      <div className="mt-3 flex flex-wrap gap-1.5">
        {student.skills?.slice(0, 5).map((s) => (
          <span key={s} className="badge bg-slate-100 text-slate-600">{s}</span>
        ))}
      </div>
      <div className="mt-3 flex items-center justify-between text-sm">
        <span className="text-slate-500">{student.category || 'Uncategorized'}</span>
        {student.potential_score != null && (
          <span className={`font-semibold ${student.is_high_potential ? 'text-emerald-600' : 'text-slate-600'}`}>
            Score: {student.potential_score}
            {student.is_high_potential && ' 🌟'}
          </span>
        )}
      </div>
    </Link>
  )
}
