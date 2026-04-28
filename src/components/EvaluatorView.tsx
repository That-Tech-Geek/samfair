"use client";

import { useEffect, useState } from "react";

export default function EvaluatorView() {
  const [goldenPreview, setGoldenPreview] = useState<string[][]>([]);
  const [modelPreview, setModelPreview] = useState<string[][]>([]);

  useEffect(() => {
    // Fetch and parse first 5 rows of CSVs
    const fetchCsv = async (url: string, setter: any) => {
      try {
        const res = await fetch(url);
        const text = await res.text();
        const rows = text.split('\n').slice(0, 6).map(row => row.split(','));
        setter(rows);
      } catch (e) {
        console.error("Failed to load CSV preview", e);
      }
    };
    fetchCsv("/mockups/mock_golden_set.csv", setGoldenPreview);
    fetchCsv("/mockups/mock_model_output.csv", setModelPreview);
  }, []);

  const renderTable = (data: string[][]) => {
    if (data.length < 2) return <div className="text-gray-400 text-sm">Loading preview...</div>;
    const headers = data[0];
    const rows = data.slice(1, -1); // exclude empty last row if any
    return (
      <div className="overflow-x-auto rounded-lg border border-white/10">
        <table className="w-full text-sm text-left text-gray-300">
          <thead className="text-xs text-gray-400 uppercase bg-black/40 border-b border-white/10">
            <tr>
              {headers.map((h, i) => <th key={i} className="px-4 py-3 whitespace-nowrap">{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                {row.map((cell, j) => <td key={j} className="px-4 py-3 whitespace-nowrap">{cell}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="space-y-12 animate-in fade-in slide-in-from-bottom-8">
      <header className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Evaluator Dashboard</h2>
        <p className="text-gray-400">Inspect the raw artifacts demonstrating SamFair's offline batch-processing capabilities.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* CSV Previews */}
        <div className="space-y-8">
          <div className="p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 shadow-xl">
            <div className="flex justify-between items-center mb-4">
              <div>
                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-blue-500"></span> Golden Set Features
                </h3>
                <p className="text-xs text-gray-400 mt-1">First 5 rows of 1,500 candidates</p>
              </div>
              <a href="/mockups/mock_golden_set.csv" download className="text-sm bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded-md transition-colors font-medium">Download CSV</a>
            </div>
            {renderTable(goldenPreview)}
          </div>

          <div className="p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 shadow-xl">
            <div className="flex justify-between items-center mb-4">
              <div>
                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-purple-500"></span> Model Predictions
                </h3>
                <p className="text-xs text-gray-400 mt-1">AEDT output mapped to candidates</p>
              </div>
              <a href="/mockups/mock_model_output.csv" download className="text-sm bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded-md transition-colors font-medium">Download CSV</a>
            </div>
            {renderTable(modelPreview)}
          </div>
        </div>

        {/* PDF Embed */}
        <div className="h-full min-h-[600px] flex flex-col p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-green-500/20 shadow-xl shadow-green-900/10">
          <div className="flex justify-between items-center mb-4">
             <div>
                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.8)]"></span> Generated DPIA Report
                </h3>
                <p className="text-xs text-gray-400 mt-1">Cryptographically hashed compliance artifact</p>
              </div>
            <a href="/mockups/offline_audit_report.pdf" download className="text-sm bg-green-600/80 hover:bg-green-500 text-white px-3 py-1.5 rounded-md transition-colors font-medium">Download PDF</a>
          </div>
          <div className="flex-1 rounded-lg overflow-hidden border border-white/10 bg-black/40">
            <iframe 
              src="/mockups/offline_audit_report.pdf" 
              className="w-full h-full min-h-[600px] bg-white"
              title="DPIA Report PDF"
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  );
}
