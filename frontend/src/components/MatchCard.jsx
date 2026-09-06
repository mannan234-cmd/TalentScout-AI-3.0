import React from 'react'

const STATUS_STYLES = {
  suggested: 'bg-slate-100 text-slate-600',
  shortlisted: 'bg-emerald-50 text-emerald-600',
  application_ready: 'bg-brand-50 text-brand-700',
  applied: 'bg-purple-50 text-purple-700',
  dismissed: 'bg-red-50 text-red-600',
}

export default function MatchCard({ match, opportunity, onGenerateApplication, busy }) {
  return (
    <div className="card">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-semibold text-slate-900">{opportunity?.title || 'Opportunity'}</h3>
          <p className="text-sm text-slate-500">{opportunity?.organization} · {opportunity?.location}</p>
        </div>
        <span className={`badge ${STATUS_STYLES[match.status] || 'bg-slate-100 text-slate-600'}`}>
          {match.status.replace('_', ' ')}
        </span>
      </div>

      <div className="mt-3">
        <div className="flex items-center gap-2 mb-1">
          <div className="flex-1 h-2 rounded-full bg-slate-100 overflow-hidden">
            <div className="h-full bg-emerald-500" style={{ width: `${match.score}%` }} />
          </div>
          <span className="text-sm font-semibold text-slate-700">{match.score}%</span>
        </div>
        <p className="text-xs text-slate-500">{match.rationale}</p>
      </div>

      <div className="mt-3 flex flex-wrap gap-1.5">
        {match.matched_skills?.map((s) => (
          <span key={s} className="badge bg-emerald-50 text-emerald-700">✓ {s}</span>
        ))}
        {match.missing_skills?.map((s) => (
          <span key={s} className="badge bg-red-50 text-red-500">✗ {s}</span>
        ))}
      </div>

      {onGenerateApplication && match.status !== 'application_ready' && (
        <button className="btn-primary mt-4 w-full" disabled={busy} onClick={() => onGenerateApplication(match.id)}>
          ✨ Generate Application Package
        </button>
      )}
      {match.status === 'application_ready' && (
        <p className="mt-4 text-sm text-emerald-600 font-medium">Application package ready — see Applications tab.</p>
      )}
    </div>
  )
}
