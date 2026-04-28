"use client";
import { useState } from "react";

export default function RemediationSlider({ ppnl, onRemediate }: { ppnl: any, onRemediate: (feature: string, weight: number) => void }) {
  if (!ppnl) return null;

  const [weights, setWeights] = useState<Record<string, number>>(() => {
    const init: Record<string, number> = {};
    Object.keys(ppnl.feature_contributions).forEach(k => { init[k] = 1.0; });
    return init;
  });

  const handleSliderChange = (feat: string, val: number) => {
    setWeights({ ...weights, [feat]: val });
    onRemediate(feat, val);
  };

  return (
    <div className="p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-blue-500/30 shadow-2xl mt-6 relative overflow-hidden">
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-500/10 blur-3xl rounded-full -ml-20 -mb-20 pointer-events-none"></div>

      <div className="flex items-center gap-3 mb-6">
        <h2 className="text-2xl font-bold text-white">Algorithmic Remediation</h2>
        <span className="bg-blue-500/20 text-blue-400 border border-blue-500/30 text-xs px-2 py-1 rounded font-bold uppercase tracking-wider">Intervention</span>
      </div>

      <p className="text-gray-400 text-sm mb-6">
        Adjust the reliance on biased proxy variables to observe real-time impact.
      </p>

      <div className="space-y-6">
        {Object.entries(weights).map(([feat, val]) => (
          <div key={feat} className="bg-black/30 p-4 rounded-xl border border-white/5">
            <div className="flex justify-between text-sm text-white mb-3">
              <span className="font-medium">{feat}</span>
              <span className="font-mono text-blue-300">{val.toFixed(2)}x</span>
            </div>
            <input 
              type="range" min="0" max="1" step="0.05" value={val}
              onChange={(e) => handleSliderChange(feat, parseFloat(e.target.value))}
              className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
          </div>
        ))}
      </div>
    </div>
  );
}
