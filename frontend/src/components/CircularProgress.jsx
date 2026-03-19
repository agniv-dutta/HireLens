import React from 'react';

export default function CircularProgress({ score }) {
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;
  const strokeDashoffset = circumference - progress;

  let color = '#ef4444'; // red
  let bgColor = '#fee2e2';
  if (score >= 75) {
    color = '#22c55e'; // green
    bgColor = '#dcfce7';
  } else if (score >= 50) {
    color = '#f59e0b'; // amber
    bgColor = '#fef3c7';
  }

  return (
    <div className="relative flex-shrink-0" style={{ width: 88, height: 88 }}>
      <svg width="88" height="88" viewBox="0 0 88 88" className="rotate-[-90deg]">
        {/* Background circle */}
        <circle
          cx="44"
          cy="44"
          r={radius}
          fill="none"
          stroke={bgColor}
          strokeWidth="8"
        />
        {/* Progress arc */}
        <circle
          cx="44"
          cy="44"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          style={{ transition: 'stroke-dashoffset 0.6s ease' }}
        />
      </svg>
      {/* Center label */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-xl font-extrabold leading-none" style={{ color }}>{score}</span>
        <span className="text-[10px] font-semibold text-slate-400 leading-none mt-0.5">/ 100</span>
      </div>
    </div>
  );
}
