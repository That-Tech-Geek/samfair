"use client";

export default function PpnlExplainer({ ppnl }: { ppnl: any }) {
  if (!ppnl) return null;

  return (
    <div className="p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-orange-500/30 shadow-2xl mt-6 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-orange-500/10 blur-3xl rounded-full -mr-20 -mt-20 pointer-events-none"></div>
      
      <div className="flex items-center gap-3 mb-6">
        <h2 className="text-2xl font-bold text-white">Post-Prediction Neural Linker</h2>
        <span className="bg-orange-500/20 text-orange-400 border border-orange-500/30 text-xs px-2 py-1 rounded font-bold uppercase tracking-wider">Explainability</span>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-black/40 p-4 rounded-xl border border-white/10">
          <h3 className="text-sm font-semibold text-gray-400 uppercase mb-3 tracking-wider">Extracted Surrogate Rule</h3>
          <div className="font-mono text-orange-300 text-sm leading-relaxed p-3 bg-orange-950/30 rounded-lg border border-orange-500/20">
            {ppnl.rule}
          </div>
          <div className="mt-4 flex justify-between text-xs text-gray-500">
            <span>Fidelity: {(ppnl.surrogate_fidelity * 100).toFixed(1)}%</span>
            <span>Surrogate: DecisionTree</span>
          </div>
        </div>

        <div className="bg-black/40 p-4 rounded-xl border border-white/10">
          <h3 className="text-sm font-semibold text-gray-400 uppercase mb-3 tracking-wider">Feature Contributions</h3>
          <div className="space-y-3">
            {Object.entries(ppnl.feature_contributions).map(([feat, val]: [string, any]) => (
              <div key={feat}>
                <div className="flex justify-between text-xs text-white mb-1">
                  <span>{feat}</span>
                  <span className="font-mono">{val}</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div className="bg-orange-500 h-2 rounded-full" style={{ width: `${Math.min(val * 100, 100)}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
