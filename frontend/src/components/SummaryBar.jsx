import React from 'react';

function StatCard({ icon, label, value, accent }) {
  return (
    <div className={`bg-white rounded-2xl shadow-sm border border-slate-100 px-6 py-5 flex items-center gap-4 flex-1 min-w-0`}>
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${accent}`}>
        {icon}
      </div>
      <div className="min-w-0">
        <p className="text-sm font-medium text-slate-500 truncate">{label}</p>
        <p className="text-3xl font-extrabold text-slate-900 mt-0.5 tracking-tight">{value}</p>
      </div>
    </div>
  );
}

export default function SummaryBar({ stats }) {
  return (
    <div className="flex flex-col sm:flex-row gap-4">
      <StatCard
        accent="bg-indigo-50"
        label="Total Candidates"
        value={stats.total}
        icon={
          <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        }
      />
      <StatCard
        accent="bg-emerald-50"
        label="Strong Fit"
        value={stats.strongFit}
        icon={
          <svg className="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        }
      />
      <StatCard
        accent="bg-amber-50"
        label="Average Match Score"
        value={`${stats.avgScore}%`}
        icon={
          <svg className="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        }
      />
    </div>
  );
}
