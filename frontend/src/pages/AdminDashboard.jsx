import React from 'react'
import { Link } from 'react-router-dom'
import RealtimeBanner from '../components/RealtimeBanner'

const QUICK_LINKS = [
  ['/discovery', '🔎', 'Discovery', 'Browse all newly-ingested student submissions and their AI categorization.'],
  ['/review', '🧑\u200d⚖️', 'Human Review', 'Approve or reject candidates the AI has flagged as pending review.'],
  ['/opportunities', '🎯', 'Opportunities', 'Manage internships, scholarships, and job postings.'],
  ['/matches', '🤝', 'Matches', 'See AI-generated matches between approved students and opportunities.'],
]

export default function AdminDashboard() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-1">Admin & Reviewer Dashboard</h1>
      <p className="text-slate-500 mb-6">Real-time overview of the talent pipeline.</p>

      <RealtimeBanner />

      <div className="grid sm:grid-cols-2 gap-4">
        {QUICK_LINKS.map(([path, icon, title, desc]) => (
          <Link key={path} to={path} className="card hover:shadow-md transition-shadow">
            <div className="text-2xl mb-2">{icon}</div>
            <h3 className="font-semibold text-slate-900 mb-1">{title}</h3>
            <p className="text-sm text-slate-600">{desc}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
