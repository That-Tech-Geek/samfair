"use client";
import { Bar } from 'react-chartjs-2';
import { useState } from 'react';

export default function PpnlExplainer({ ppnl }: { ppnl: any }) {
  const [showDetails, setShowDetails] = useState(false);

  if (!ppnl) return null;

  const data = {
    labels: Object.keys(ppnl.feature_contributions),
    datasets: [{
      label: 'Feature Contribution',
      data: Object.values(ppnl.feature_contributions),
      backgroundColor: 'rgba(249, 115, 22, 0.8)'
    }]
  };

  const options = { indexAxis: 'y' as const, responsive: true };

  return (
    <div className="p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-orange-500/30 shadow-2xl mt-6 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-orange-500/10 blur-3xl rounded-full -mr-20 -mt-20 pointer-events-none"></div>
      
      <div className="flex items-center gap-3 mb-6">
        <h2 className="text-2xl font-bold text-white">Post-Prediction Neural Linker</h2>
        <span className="bg-orange-500/20 text-orange-400 border border-orange-500/30 text-xs px-2 py-1 rounded font-bold uppercase tracking-wider">Explainability</span>
      </div>
      
      <div className="bg-black/40 p-4 rounded-xl border border-white/10 mb-6">
        <h3 className="text-sm font-semibold text-gray-400 uppercase mb-3 tracking-wider">Extracted Surrogate Rule</h3>
        <div className="font-mono text-orange-300 text-sm leading-relaxed p-3 bg-orange-950/30 rounded-lg border border-orange-500/20">
          {ppnl.rule}
        </div>
      </div>

      <div className="bg-black/40 p-4 rounded-xl border border-white/10 mb-6">
        <h3 className="text-sm font-semibold text-gray-400 uppercase mb-3 tracking-wider">Feature Contributions</h3>
        <div className="h-48">
           <Bar data={data} options={options} />
        </div>
      </div>

      <button onClick={() => setShowDetails(!showDetails)} className="text-xs text-orange-400 underline">
        {showDetails ? "Hide Details" : "Show Details"}
      </button>

      {showDetails && (
        <div className="mt-4 text-xs text-gray-400 bg-black/20 p-3 rounded">
          <p>Group Impacted: <span className="font-mono text-white">{ppnl.group_impacted}</span></p>
          <p>Surrogate Accuracy: <span className="font-mono text-white">{(ppnl.surrogate_accuracy * 100).toFixed(1)}%</span></p>
        </div>
      )}
    </div>
  );
}
