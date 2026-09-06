import React from 'react'

export default function SignalCard({ report }) {
  if (!report) return null
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-slate-900">AI Signal Report</h3>
        <span className="badge bg-brand-50 text-brand-700">
          Potential Score: {report.potential_score}
        </span>
      </div>
      <p className="text-sm text-slate-600 mb-4">{report.summary}</p>

      <div className="grid sm:grid-cols-2 gap-4">
        <div>
          <h4 className="text-sm font-medium text-slate-700 mb-2">Detected Skills</h4>
          <div className="space-y-1.5">
            {report.detected_skills?.map((d) => (
              <div key={d.skill} className="flex items-center gap-2">
                <div className="w-24 text-xs text-slate-600 truncate">{d.skill}</div>
                <div className="flex-1 h-2 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full bg-brand-500"
                    style={{ width: `${Math.round(d.confidence * 100)}%` }}
                  />
                </div>
                <div className="text-xs text-slate-400 w-8 text-right">{Math.round(d.confidence * 100)}%</div>
              </div>
            ))}
            {(!report.detected_skills || report.detected_skills.length === 0) && (
              <p className="text-xs text-slate-400">No skills detected yet.</p>
            )}
          </div>
        </div>

        <div>
          <h4 className="text-sm font-medium text-slate-700 mb-2">Strengths</h4>
          <ul className="text-sm text-slate-600 list-disc list-inside mb-3">
            {report.strengths?.map((s) => <li key={s}>{s}</li>)}
          </ul>
          {report.gaps?.length > 0 && (
            <>
              <h4 className="text-sm font-medium text-slate-700 mb-2">Gaps</h4>
              <ul className="text-sm text-amber-600 list-disc list-inside">
                {report.gaps.map((g) => <li key={g}>{g}</li>)}
              </ul>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
