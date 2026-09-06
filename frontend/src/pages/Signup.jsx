import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Signup() {
  const { signup } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ full_name: '', email: '', password: '', role: 'student' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      const user = await signup(form.full_name, form.email, form.password, form.role)
      navigate(user.role === 'student' ? '/student' : '/admin')
    } catch (err) {
      setError(err.response?.data?.detail || 'Signup failed')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-16">
      <div className="card">
        <h1 className="text-xl font-bold text-slate-900 mb-1">Create an account</h1>
        <p className="text-sm text-slate-500 mb-6">Join TalentScout AI 3.0</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Full Name</label>
            <input className="input" required value={form.full_name} onChange={(e) => update('full_name', e.target.value)} />
          </div>
          <div>
            <label className="label">Email</label>
            <input className="input" type="email" required value={form.email} onChange={(e) => update('email', e.target.value)} />
          </div>
          <div>
            <label className="label">Password</label>
            <input className="input" type="password" required minLength={6} value={form.password} onChange={(e) => update('password', e.target.value)} />
          </div>
          <div>
            <label className="label">I am a…</label>
            <select className="input" value={form.role} onChange={(e) => update('role', e.target.value)}>
              <option value="student">Student / Candidate</option>
              <option value="admin">Admin / Reviewer</option>
            </select>
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button className="btn-primary w-full" disabled={busy}>{busy ? 'Creating account…' : 'Sign up'}</button>
        </form>

        <p className="text-sm text-slate-500 mt-4">
          Already have an account? <Link to="/login" className="text-brand-600 font-medium">Login</Link>
        </p>
      </div>
    </div>
  )
}
