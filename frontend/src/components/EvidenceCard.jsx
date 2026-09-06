import React from 'react'

export default function EvidenceCard({ item }) {
  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <h4 className="font-medium text-slate-900">{item.title}</h4>
        <span className="badge bg-slate-100 text-slate-600">{item.type}</span>
      </div>
      <p className="text-sm text-slate-600 mt-2 whitespace-pre-wrap">{item.description}</p>
      {item.extracted_keywords?.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {item.extracted_keywords.map((k) => (
            <span key={k} className="badge bg-brand-50 text-brand-700">{k}</span>
          ))}
        </div>
      )}
    </div>
  )
}
