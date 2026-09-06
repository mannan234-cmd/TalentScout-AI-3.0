import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      const user = await login(email, password)
      navigate(user.role === 'student' ? '/student' : '/admin')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-16">
      <div className="card">
        <h1 className="text-xl font-bold text-slate-900 mb-1">Welcome back</h1>
        <p className="text-sm text-slate-500 mb-6">Log in to TalentScout AI 3.0</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Email</label>
            <input className="input" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <label className="label">Password</label>
            <input className="input" type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button className="btn-primary w-full" disabled={busy}>{busy ? 'Logging in…' : 'Login'}</button>
        </form>

        <p className="text-sm text-slate-500 mt-4">
          No account? <Link to="/signup" className="text-brand-600 font-medium">Sign up</Link>
        </p>

        <div className="mt-6 pt-4 border-t border-slate-100 text-xs text-slate-400">
          <p className="font-medium mb-1">Demo accounts:</p>
          <p>Admin — admin@talentscout.ai / admin123</p>
          <p>Student (Tech) — sara@student.com / student123</p>
          <p>Student (Non-Tech / Marketing) — ayesha@student.com / student123</p>
        </div>
      </div>
    </div>
  )
}
