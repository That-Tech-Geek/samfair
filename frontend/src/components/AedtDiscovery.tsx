"use client";
import { useState } from "react";

export default function AedtDiscovery({ onDiscovered }: { onDiscovered: (aedts: any[]) => void }) {
  const [url, setUrl] = useState("http://localhost:8000/mock_hr.html");
  const [loading, setLoading] = useState(false);
  const [tools, setTools] = useState<any[]>([]);

  const handleScan = async () => {
    setLoading(true);
    try {
      const res = await fetch("/_/backend/discover", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, credentials: {} }),
      });
      const data = await res.json();
      setTools(data.aedts);
      onDiscovered(data.aedts);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div className="p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 shadow-2xl">
      <h2 className="text-2xl font-bold text-white mb-4">AEDT Discovery Scanner</h2>
      <div className="flex gap-4 mb-4">
        <input 
          type="text" 
          value={url} 
          onChange={e => setUrl(e.target.value)}
          className="flex-1 bg-black/40 text-white rounded-lg px-4 py-2 border border-white/10 focus:outline-none focus:ring-2 focus:ring-purple-500"
          placeholder="Enter HR Dashboard URL"
        />
        <button 
          onClick={handleScan}
          disabled={loading}
          className="bg-purple-600 hover:bg-purple-500 text-white px-6 py-2 rounded-lg font-medium transition-all shadow-lg shadow-purple-500/30"
        >
          {loading ? "Scanning..." : "Scan URL"}
        </button>
      </div>
      {tools.length > 0 && (
        <div className="mt-4 animate-in fade-in slide-in-from-bottom-4">
          <h3 className="text-sm font-semibold text-gray-400 mb-2 uppercase tracking-wider">Discovered Models</h3>
          <ul className="space-y-2">
            {tools.map((t, i) => (
              <li key={i} className="bg-white/5 p-4 rounded-xl border border-white/10 text-white flex justify-between items-center hover:bg-white/10 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-green-400 shadow-[0_0_10px_rgba(74,222,128,0.8)]"></div>
                  <span className="font-medium">{t.name}</span>
                </div>
                <span className="text-xs text-purple-300 font-mono bg-purple-500/20 px-2 py-1 rounded">{t.endpoint}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
