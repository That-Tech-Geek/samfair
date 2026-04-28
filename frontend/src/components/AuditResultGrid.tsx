"use client";

export default function AuditResultGrid({ results }: { results: any[] }) {
  if (!results || results.length === 0) return null;

  return (
    <div className="p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 shadow-2xl mt-6">
      <h2 className="text-2xl font-bold text-white mb-6">4/5ths Rule Bias Audit</h2>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-white/10">
              <th className="pb-3 text-sm font-semibold text-gray-400 uppercase tracking-wider">Protected Attribute</th>
              <th className="pb-3 text-sm font-semibold text-gray-400 uppercase tracking-wider">Group</th>
              <th className="pb-3 text-sm font-semibold text-gray-400 uppercase tracking-wider">Selection Rate</th>
              <th className="pb-3 text-sm font-semibold text-gray-400 uppercase tracking-wider">Impact Ratio</th>
              <th className="pb-3 text-sm font-semibold text-gray-400 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {results.map((r, i) => (
              <tr key={i} className="text-white hover:bg-white/5 transition-colors">
                <td className="py-4 text-sm font-medium">{r.attribute}</td>
                <td className="py-4 text-sm text-gray-300">{r.group}</td>
                <td className="py-4 text-sm font-mono">{(r.selection_rate * 100).toFixed(1)}%</td>
                <td className="py-4 text-sm font-mono">
                  {r.impact_ratio.toFixed(2)}
                </td>
                <td className="py-4">
                  {r.flagged ? (
                    <span className="inline-flex items-center gap-1.5 py-1 px-3 rounded-full text-xs font-medium bg-red-500/20 text-red-400 border border-red-500/20">
                      <div className="w-1.5 h-1.5 rounded-full bg-red-400"></div>
                      Flagged (Bias)
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1.5 py-1 px-3 rounded-full text-xs font-medium bg-green-500/20 text-green-400 border border-green-500/20">
                      <div className="w-1.5 h-1.5 rounded-full bg-green-400"></div>
                      Pass
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
