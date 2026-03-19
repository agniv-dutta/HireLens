import React from 'react';

const FILTERS = ['All', 'Strong Fit', 'Moderate Fit', 'Not Fit'];
const SORTS = [
  { value: 'score_desc', label: 'Score: High → Low' },
  { value: 'score_asc', label: 'Score: Low → High' },
  { value: 'name_asc', label: 'Name: A → Z' },
];

export default function FilterBar({ filter, setFilter, sort, setSort }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 px-4 py-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
      {/* Filter pills */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest mr-1">Filter</span>
        {FILTERS.map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-all duration-150 ${
              filter === f
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Sort select */}
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest flex-shrink-0">Sort</span>
        <select
          value={sort}
          onChange={e => setSort(e.target.value)}
          className="text-sm text-slate-700 font-medium bg-slate-100 border-0 rounded-xl px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-400 cursor-pointer"
        >
          {SORTS.map(s => (
            <option key={s.value} value={s.value}>{s.label}</option>
          ))}
        </select>
      </div>
    </div>
  );
}
