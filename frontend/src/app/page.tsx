"use client";

import { useState } from "react";
import AedtDiscovery from "@/components/AedtDiscovery";
import AuditResultGrid from "@/components/AuditResultGrid";
import PpnlExplainer from "@/components/PpnlExplainer";
import RemediationSlider from "@/components/RemediationSlider";
import { db } from "@/lib/firebase";
import { collection, addDoc } from "firebase/firestore";

export default function Home() {
  const [aedts, setAedts] = useState<any[]>([]);
  const [selectedAedt, setSelectedAedt] = useState<string>("");
  const [auditResults, setAuditResults] = useState<any[]>([]);
  const [ppnl, setPpnl] = useState<any>(null);
  const [reportPath, setReportPath] = useState<string>("");
  const [auditing, setAuditing] = useState(false);
  const [showPpnl, setShowPpnl] = useState(false);

  const handleAudit = async () => {
    if (!selectedAedt) return;
    setAuditing(true);
    setShowPpnl(false);
    try {
      const res = await fetch("http://localhost:8000/audit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ aedt_endpoint: selectedAedt }),
      });
      const data = await res.json();
      setAuditResults(data.audit_results);
      setPpnl(data.ppnl);
      setReportPath(data.report_path);

      // Log to Firestore
      try {
        await addDoc(collection(db, "samfair_audits"), {
          endpoint: selectedAedt,
          timestamp: new Date().toISOString(),
          results_count: data.audit_results?.length || 0,
          flagged_count: data.audit_results?.filter((r:any) => r.flagged).length || 0
        });
      } catch (e) {
        console.error("Firestore error (ignore if keys not configured):", e);
      }

    } catch (e) {
      console.error(e);
    }
    setAuditing(false);
  };

  const handleRemediate = async (feature: string, weight: number) => {
    try {
      const res = await fetch("http://localhost:8000/remediate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feature, weight }),
      });
      const data = await res.json();
      setAuditResults(data.audit_results);
    } catch (e) {
      console.error(e);
    }
  };

  const handleDownload = () => {
    window.location.href = "http://localhost:8000/download_report";
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.15),rgba(255,255,255,0))] selection:bg-purple-500/30">
      <main className="max-w-6xl mx-auto px-4 py-12">
        <header className="mb-12 text-center">
          <div className="inline-flex items-center justify-center p-3 bg-white/5 rounded-2xl border border-white/10 shadow-2xl mb-6">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          </div>
          <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/60 mb-4 tracking-tight">SamFair Audit Suite</h1>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">DPDP Act & AI Bill 2025 Compliance Dashboard. Discover, Audit, and Explain opaque AI decisions locally.</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 space-y-8">
            <AedtDiscovery onDiscovered={setAedts} />

            {aedts.length > 0 && (
              <div className="p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 shadow-2xl animate-in fade-in">
                <h3 className="text-xl font-bold text-white mb-4">Run Audit</h3>
                <select 
                  className="w-full bg-black/40 text-white rounded-lg px-4 py-3 border border-white/10 focus:outline-none focus:ring-2 focus:ring-purple-500 mb-4"
                  onChange={e => setSelectedAedt(e.target.value)}
                  value={selectedAedt}
                >
                  <option value="" disabled>Select an AEDT...</option>
                  {aedts.map(a => (
                    <option key={a.endpoint} value={a.endpoint}>{a.name}</option>
                  ))}
                </select>
                <button 
                  onClick={handleAudit}
                  disabled={!selectedAedt || auditing}
                  className="w-full bg-white text-black hover:bg-gray-200 px-6 py-3 rounded-lg font-bold transition-all disabled:opacity-50"
                >
                  {auditing ? "Auditing Model..." : "Commence Audit"}
                </button>
              </div>
            )}
          </div>

          <div className="lg:col-span-2 space-y-8">
            {auditResults.length > 0 && (
              <div className="animate-in fade-in slide-in-from-bottom-8">
                <AuditResultGrid results={auditResults} onFlagClicked={() => setShowPpnl(true)} />
              </div>
            )}

            {showPpnl && ppnl && (
              <div className="animate-in fade-in slide-in-from-bottom-8">
                <PpnlExplainer ppnl={ppnl} />
                <RemediationSlider ppnl={ppnl} onRemediate={handleRemediate} />
              </div>
            )}

            {reportPath && (
              <div className="p-6 bg-white/5 backdrop-blur-lg rounded-2xl border border-green-500/20 flex justify-between items-center animate-in fade-in">
                <div>
                  <h3 className="text-lg font-bold text-white">DPIA Report Ready</h3>
                  <p className="text-sm text-gray-400">PDF generated with cryptographic hash log.</p>
                </div>
                <button onClick={handleDownload} className="bg-green-600 hover:bg-green-500 text-white px-6 py-2 rounded-lg font-medium shadow-[0_0_15px_rgba(22,163,74,0.4)]">
                  Download PDF
                </button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
