import React, { useEffect, useMemo, useState } from 'react';
import Header from './components/Header';
import SummaryBar from './components/SummaryBar';
import FilterBar from './components/FilterBar';
import CandidateCard from './components/CandidateCard';

export default function App() {
  const [candidatesData, setCandidatesData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState('');
  const [filter, setFilter] = useState('All');
  const [sort, setSort] = useState('score_desc');

  useEffect(() => {
    let isMounted = true;

    async function loadResults() {
      try {
        setIsLoading(true);
        setLoadError('');

        const response = await fetch('/api/results');
        if (!response.ok) {
          throw new Error(`Failed to load results (${response.status})`);
        }

        const data = await response.json();
        if (isMounted) {
          setCandidatesData(Array.isArray(data) ? data : []);
        }
      } catch (error) {
        if (isMounted) {
          setLoadError(error.message || 'Unable to load screening results.');
          setCandidatesData([]);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadResults();

    return () => {
      isMounted = false;
    };
  }, []);

  const stats = useMemo(() => {
    const total = candidatesData.length;
    const strongFit = candidatesData.filter(c => c.recommendation === 'Strong Fit').length;
    const avgScore = total
      ? Math.round(candidatesData.reduce((acc, c) => acc + c.match_score, 0) / total)
      : 0;
    return { total, strongFit, avgScore };
  }, [candidatesData]);

  const filteredAndSorted = useMemo(() => {
    let result = [...candidatesData];

    if (filter !== 'All') {
      result = result.filter(c => c.recommendation === filter);
    }

    switch (sort) {
      case 'score_desc':
        result.sort((a, b) => b.match_score - a.match_score);
        break;
      case 'score_asc':
        result.sort((a, b) => a.match_score - b.match_score);
        break;
      case 'name_asc':
        result.sort((a, b) => a.candidate_name.localeCompare(b.candidate_name));
        break;
      default:
        break;
    }

    return result;
  }, [filter, sort]);

  return (
    <div className="min-h-screen bg-slate-100">
      <Header totalCandidates={stats.total} />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <SummaryBar stats={stats} />
        <FilterBar filter={filter} setFilter={setFilter} sort={sort} setSort={setSort} />
        {isLoading && (
          <div className="rounded-2xl bg-white border border-slate-200 p-6 text-slate-500">
            Loading latest screening results...
          </div>
        )}
        {loadError && (
          <div className="rounded-2xl bg-red-50 border border-red-200 p-6 text-red-700">
            {loadError}. Start the backend API server and retry.
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredAndSorted.map((candidate, index) => (
            <CandidateCard key={candidate.candidate_name + index} candidate={candidate} />
          ))}
          {filteredAndSorted.length === 0 && (
            <div className="col-span-full flex flex-col items-center justify-center py-24 text-slate-400">
              <svg className="w-16 h-16 mb-4 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-lg font-medium">No candidates match this filter</p>
              <p className="text-sm mt-1">Try selecting a different recommendation category</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
