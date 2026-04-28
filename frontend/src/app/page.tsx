"use client";
import { useState } from "react";
import AedtDiscovery from "@/components/AedtDiscovery";
import AuditResultGrid from "@/components/AuditResultGrid";
import PpnlExplainer from "@/components/PpnlExplainer";
import RemediationSlider from "@/components/RemediationSlider";

export default function Home() {
  const [discoveredTools, setDiscoveredTools] = useState<any[]>([]);
  const [selectedTool, setSelectedTool] = useState<string | null>(null);
  const [auditData, setAuditData] = useState<any>(null);
  const [loadingAudit, setLoadingAudit] = useState(false);

  const runAudit = async (weights = null) => {
    if (!selectedTool) return;
    setLoadingAudit(true);
    try {
      const res = await fetch("http://localhost:8000/audit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ aedt_endpoint: selectedTool, feature_weights: weights }),
      });
      const data = await res.json();
      setAuditData(data);
    } catch (e) {
      console.error(e);
    }
    setLoadingAudit(false);
  };

  const downloadReport = () => {
    window.open("http://localhost:8000/download-report", "_blank");
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white selection:bg-purple-500/30 font-sans p-8 md:p-12 pb-24">
      {/* Background gradients */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-900/20 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-900/20 rounded-full blur-[120px]"></div>
      </div>

      <div className="max-w-5xl mx-auto relative z-10">
        <header className="mb-12 flex justify-between items-end">
          <div>
            <h1 className="text-5xl font-extrabold tracking-tight mb-2 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-blue-500">
              SamFair
            </h1>
            <p className="text-gray-400 text-lg">AI Bias Audit & Remediation Platform</p>
          </div>
          {auditData?.report_ready && (
            <button 
              onClick={downloadReport}
              className="bg-white/10 hover:bg-white/20 border border-white/20 text-white px-5 py-2 rounded-lg font-medium transition-all shadow-lg flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              Download DPIA PDF
            </button>
          )}
        </header>

        <AedtDiscovery onDiscovered={(tools) => {
          setDiscoveredTools(tools);
          if (tools.length > 0) setSelectedTool(tools[0].endpoint);
        }} />

        {discoveredTools.length > 0 && (
          <div className="mt-8 flex justify-center animate-in fade-in zoom-in duration-500">
            <button 
              onClick={() => runAudit(null)}
              disabled={loadingAudit}
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-[0_0_40px_rgba(168,85,247,0.4)] transition-all disabled:opacity-50"
            >
              {loadingAudit ? "Auditing Neural Pathways..." : "Run Deep Bias Audit"}
            </button>
          </div>
        )}

        {auditData && (
          <div className="animate-in fade-in slide-in-from-bottom-8 duration-700">
            <AuditResultGrid results={auditData.audit_results} />
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
              {auditData.ppnl && <PpnlExplainer ppnl={auditData.ppnl} />}
              {auditData.ppnl && <RemediationSlider ppnl={auditData.ppnl} onRemediate={(weights) => runAudit(weights)} />}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
