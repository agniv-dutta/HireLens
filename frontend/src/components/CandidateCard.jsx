import React from 'react';
import CircularProgress from './CircularProgress';

const BADGE_STYLES = {
  'Strong Fit': 'bg-emerald-100 text-emerald-700 border border-emerald-200',
  'Moderate Fit': 'bg-amber-100 text-amber-700 border border-amber-200',
  'Not Fit': 'bg-red-100 text-red-700 border border-red-200',
};

const CHECK_ICON = (
  <svg className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
  </svg>
);

const X_ICON = (
  <svg className="w-4 h-4 text-red-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
  </svg>
);

export default function CandidateCard({ candidate }) {
  const { candidate_name, match_score, strengths, gaps, recommendation, summary } = candidate;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow duration-200 overflow-hidden flex flex-col">
      {/* Card Header */}
      <div className="px-5 pt-5 pb-4 flex items-start gap-4 border-b border-slate-50">
        {/* Avatar */}
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center text-white font-bold text-sm flex-shrink-0 mt-1">
          {candidate_name.charAt(0)}
        </div>

        {/* Name + Badge */}
        <div className="flex-1 min-w-0">
          <h3 className="text-base font-bold text-slate-900 truncate">{candidate_name}</h3>
          <span className={`inline-block mt-1 text-xs font-semibold px-2.5 py-0.5 rounded-full ${BADGE_STYLES[recommendation]}`}>
            {recommendation}
          </span>
        </div>

        {/* Score Ring */}
        <CircularProgress score={match_score} />
      </div>

      {/* Strengths & Gaps */}
      <div className="px-5 py-4 grid grid-cols-1 gap-4 flex-1">
        <div>
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">Strengths</p>
          <ul className="space-y-1.5">
            {strengths.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-slate-700 leading-snug">
                {CHECK_ICON}
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">Gaps</p>
          <ul className="space-y-1.5">
            {gaps.map((g, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-slate-600 leading-snug">
                {X_ICON}
                <span>{g}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Divider */}
        <div className="border-t border-slate-200"></div>

        {/* AI Summary */}
        <div>
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">AI Summary</p>
          <p className="text-sm text-gray-500 italic leading-relaxed">{summary}</p>
        </div>
      </div>
    </div>
  );
}
