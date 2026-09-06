import React from 'react'

export default function LoadingState({ label = 'Loading…' }) {
  return (
    <div className="flex items-center justify-center py-16 text-slate-500 gap-3">
      <span className="h-5 w-5 rounded-full border-2 border-brand-500 border-t-transparent animate-spin" />
      <span>{label}</span>
    </div>
  )
}
