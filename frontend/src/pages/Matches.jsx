import React, { useEffect, useState } from 'react'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import MatchCard from '../components/MatchCard'
import LoadingState from '../components/LoadingState'

export default function Matches() {
  const { isAdmin } = useAuth()
  const [matches, setMatches] = useState([])
  const [opportunities, setOpportunities] = useState({})
  const [loading, setLoading] = useState(true)
  const [busyId, setBusyId] = useState(null)

  async function load() {
    setLoading(true)
    try {
      const [mRes, oRes] = await Promise.all([
        api.get('/matches'),
        api.get('/opportunities'),
      ])
      setMatches(mRes.data)
      const map = {}
      oRes.data.forEach((o) => { map[o.id] = o })
      setOpportunities(map)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  async function handleGenerateApplication(matchId) {
    setBusyId(matchId)
    try {
      await api.post(`/applications/generate/${matchId}`)
      load()
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to generate application')
    } finally {
      setBusyId(null)
    }
  }

  if (loading) return <LoadingState />

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-1">{isAdmin ? 'All Matches' : 'My Matches'}</h1>
      <p className="text-slate-500 mb-6">
        Generated automatically by the Matching Agent once a candidate is approved.
      </p>

      {matches.length === 0 ? (
        <p className="text-slate-500">No matches yet. {isAdmin ? 'Approve a candidate to generate matches.' : 'Once your profile is approved, matches will appear here.'}</p>
      ) : (
        <div className="grid sm:grid-cols-2 gap-4">
          {matches.map((m) => (
            <MatchCard
              key={m.id}
              match={m}
              opportunity={opportunities[m.opportunity_id]}
              onGenerateApplication={handleGenerateApplication}
              busy={busyId === m.id}
            />
          ))}
        </div>
      )}
    </div>
  )
}
