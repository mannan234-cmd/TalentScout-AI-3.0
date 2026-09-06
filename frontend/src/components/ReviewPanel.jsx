import React, { useState } from 'react'

export default function ReviewPanel({ student, onApprove, onReject, busy }) {
  const [notes, setNotes] = useState('')

  return (
    <div className="card">
      <h3 className="font-semibold text-slate-900 mb-3">Human Review Decision</h3>
      <p className="text-sm text-slate-500 mb-3">
        AI agents have produced advisory recommendations only. Matching &amp;
        Application Support stay blocked until you approve this candidate.
      </p>
      <textarea
        className="input mb-3"
        rows={3}
        placeholder="Optional review notes…"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
      />
      <div className="flex gap-3">
        <button className="btn-success flex-1" disabled={busy} onClick={() => onApprove(notes)}>
          ✅ Approve
        </button>
        <button className="btn-danger flex-1" disabled={busy} onClick={() => onReject(notes)}>
          ❌ Reject
        </button>
      </div>
    </div>
  )
}
