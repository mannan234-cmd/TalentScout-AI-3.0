import React from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  if (!user) return null

  const linkClass = (path) =>
    `px-3 py-2 rounded-lg text-sm font-medium ${
      location.pathname === path ? 'bg-brand-600 text-white' : 'text-slate-600 hover:bg-slate-100'
    }`

  const adminLinks = [
    ['/admin', 'Dashboard'],
    ['/discovery', 'Discovery'],
    ['/review', 'Human Review'],
    ['/opportunities', 'Opportunities'],
    ['/matches', 'Matches'],
  ]
  const studentLinks = [
    ['/student', 'My Dashboard'],
    ['/student/profile', 'My Profile'],
    ['/opportunities', 'Opportunities'],
    ['/matches', 'My Matches'],
    ['/applications', 'Applications'],
  ]

  const links = isAdmin ? adminLinks : studentLinks

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between h-16">
        <div className="flex items-center gap-6">
          <Link to="/" className="font-bold text-brand-700 text-lg">
            TalentScout <span className="text-slate-400 font-normal">AI 3.0</span>
          </Link>
          <div className="hidden md:flex gap-1">
            {links.map(([path, label]) => (
              <Link key={path} to={path} className={linkClass(path)}>{label}</Link>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-slate-500 hidden sm:block">{user.full_name} · {user.role}</span>
          <button
            className="btn-secondary"
            onClick={() => { logout(); navigate('/login') }}
          >
            Logout
          </button>
        </div>
      </div>
      <div className="md:hidden flex gap-1 px-4 pb-2 overflow-x-auto">
        {links.map(([path, label]) => (
          <Link key={path} to={path} className={linkClass(path) + ' whitespace-nowrap'}>{label}</Link>
        ))}
      </div>
    </nav>
  )
}
