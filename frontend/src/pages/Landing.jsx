import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const FEATURES = [
  ['🔎', 'Discovery Agent', 'Automatically filters and categorizes new student submissions the moment they arrive.'],
  ['🧬', 'Evidence & Signals Agent', 'Extracts real technical signals from profiles, portfolios, and raw evidence text.'],
  ['🎯', 'Matching Agent', 'Auto-evaluates candidate skills against internships, scholarships, and job requirements.'],
  ['✉️', 'Application Agent', 'Drafts personalized cover letters for shortlisted candidates in seconds.'],
]

export default function Landing() {
  const { user, isAdmin } = useAuth()

  return (
    <div className="max-w-5xl mx-auto px-4 py-16">
      <div className="text-center mb-12">
        <span className="badge bg-brand-50 text-brand-700 mb-4">Multi-Agent Talent Platform</span>
        <h1 className="text-4xl font-bold text-slate-900 mb-4">TalentScout AI 3.0</h1>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          Combining AI-driven talent analytics with human decision-making to connect
          verified, deserving students — from every field, tech and non-tech alike —
          with the right academic and career opportunities.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          {user ? (
            <Link to={isAdmin ? '/admin' : '/student'} className="btn-primary px-6 py-3 text-base">
              Go to Dashboard
            </Link>
          ) : (
            <>
              <Link to="/signup" className="btn-primary px-6 py-3 text-base">Get Started</Link>
              <Link to="/login" className="btn-secondary px-6 py-3 text-base">Login</Link>
            </>
          )}
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        {FEATURES.map(([icon, title, desc]) => (
          <div key={title} className="card">
            <div className="text-3xl mb-2">{icon}</div>
            <h3 className="font-semibold text-slate-900 mb-1">{title}</h3>
            <p className="text-sm text-slate-600">{desc}</p>
          </div>
        ))}
      </div>

      <div className="card mt-8 bg-brand-50 border-brand-100">
        <h3 className="font-semibold text-brand-900 mb-1">Human-in-the-Loop Governance</h3>
        <p className="text-sm text-brand-800">
          AI agents produce advisory recommendations only. The Matching &amp;
          Application Support stages stay blocked until an admin or reviewer
          explicitly approves a candidate in Human Review.
        </p>
      </div>
    </div>
  )
}
