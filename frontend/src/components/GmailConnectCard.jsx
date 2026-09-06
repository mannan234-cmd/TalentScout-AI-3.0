import React, { useState } from 'react'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function GmailConnectCard() {
  const { user, refreshUser } = useAuth()
  const [gmail, setGmail] = useState('')
  const [appPassword, setAppPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [expanded, setExpanded] = useState(false)

  const connected = user?.gmail_connected

  async function handleConnect(e) {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      await api.post('/email/connect', { gmail_address: gmail, app_password: appPassword })
      await refreshUser()
      setExpanded(false)
      setAppPassword('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not connect Gmail')
    } finally {
      setBusy(false)
    }
  }

  async function handleDisconnect() {
    setBusy(true)
    try {
      await api.delete('/email/connect')
      await refreshUser()
    } finally {
      setBusy(false)
    }
  }

  if (connected && !expanded) {
    return (
      <div className="card bg-emerald-50 border-emerald-100 mb-6 flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-emerald-800">📧 Gmail connected: {user.email}</p>
          <p className="text-xs text-emerald-700">"Send Application" will email companies directly from your inbox.</p>
        </div>
        <button className="btn-secondary" disabled={busy} onClick={handleDisconnect}>Disconnect</button>
      </div>
    )
  }

  return (
    <div className="card mb-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-slate-900">📧 Connect Gmail to auto-send applications</h3>
          <p className="text-sm text-slate-500">
            Use a Gmail <strong>App Password</strong> (not your normal password) — generate one at
            {' '}<a href="https://myaccount.google.com/apppasswords" target="_blank" rel="noreferrer" className="text-brand-600 underline">myaccount.google.com/apppasswords</a>.
          </p>
        </div>
        {!expanded && (
          <button className="btn-primary whitespace-nowrap" onClick={() => setExpanded(true)}>Connect Gmail</button>
        )}
      </div>

      {expanded && (
        <form onSubmit={handleConnect} className="mt-4 space-y-3">
          <div>
            <label className="label">Gmail Address</label>
            <input className="input" type="email" required value={gmail} onChange={(e) => setGmail(e.target.value)} placeholder="you@gmail.com" />
          </div>
          <div>
            <label className="label">App Password (16 characters)</label>
            <input className="input" type="password" required value={appPassword} onChange={(e) => setAppPassword(e.target.value)} placeholder="xxxx xxxx xxxx xxxx" />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="flex gap-3">
            <button className="btn-primary flex-1" disabled={busy}>{busy ? 'Connecting…' : 'Connect'}</button>
            <button type="button" className="btn-secondary" onClick={() => setExpanded(false)}>Cancel</button>
          </div>
          <p className="text-xs text-slate-400">
            Stored only in memory for this session — never written to disk, never shown again. For production, this would use Gmail OAuth instead.
          </p>
        </form>
      )}
    </div>
  )
}
