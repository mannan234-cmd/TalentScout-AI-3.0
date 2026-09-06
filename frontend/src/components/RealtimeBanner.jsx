import React, { useEffect, useState } from 'react'
import api from '../services/api'

const STATS = [
  ['total_students', 'Total Students'],
  ['pending_human_reviews', 'Pending Reviews'],
  ['high_potential_candidates', 'High-Potential'],
  ['active_opportunities', 'Active Opportunities'],
  ['approved_matches', 'Approved Matches'],
]

export default function RealtimeBanner() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    let mounted = true
    async function load() {
      try {
        const res = await api.get('/analytics')
        if (mounted) setStats(res.data)
      } catch {
        // silently ignore — user may not have admin rights, or backend is warming up
      }
    }
    load()
    const id = setInterval(load, 8000) // poll every 8s for a "real-time" feel
    return () => { mounted = false; clearInterval(id) }
  }, [])

  if (!stats) return null

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-6">
      {STATS.map(([key, label]) => (
        <div key={key} className="card text-center">
          <div className="text-2xl font-bold text-brand-700">{stats[key]}</div>
          <div className="text-xs text-slate-500 mt-1">{label}</div>
        </div>
      ))}
    </div>
  )
}
