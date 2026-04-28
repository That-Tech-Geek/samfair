"use client";

import { useState } from "react";
import AedtDiscovery from "@/components/AedtDiscovery";
import AuditResultGrid from "@/components/AuditResultGrid";
import PpnlExplainer from "@/components/PpnlExplainer";
import RemediationSlider from "@/components/RemediationSlider";
import { db } from "@/lib/firebase";
import { collection, addDoc } from "firebase/firestore";
import { useAuth } from "@/lib/AuthContext";
import AuthScreen from "@/components/AuthScreen";
import toast from "react-hot-toast";
import { LogOut } from "lucide-react";
import { AuditResult, PpnlOutput } from "@/types";

export default function Home() {
  const { user, loading, logout } = useAuth();
  
  const [aedts, setAedts] = useState<any[]>([]);
  const [selectedAedt, setSelectedAedt] = useState<string>("");
  const [auditResults, setAuditResults] = useState<AuditResult[]>([]);
  const [ppnl, setPpnl] = useState<PpnlOutput | null>(null);
  const [reportPath, setReportPath] = useState<string>("");
  const [auditing, setAuditing] = useState(false);
  const [showPpnl, setShowPpnl] = useState(false);
  const [currentSeed, setCurrentSeed] = useState<number | null>(null);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center bg-[#0a0a0a]"><div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div></div>;
  }

  if (!user) {
    return <AuthScreen />;
  }

  const handleAudit = async () => {
    if (!selectedAedt) return;
    setAuditing(true);
    setShowPpnl(false);
    const toastId = toast.loading("Running 4/5ths Bias Audit...");
    try {
      const res = await fetch("/_/backend/audit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ aedt_endpoint: selectedAedt }),
      });
      if (!res.ok) throw new Error("Audit execution failed");
      
      const data = await res.json();
      setAuditResults(data.audit_results);
      setPpnl(data.ppnl);
      setReportPath(data.report_path);
      setCurrentSeed(data.seed);

      toast.success("Audit Complete", { id: toastId });

      // Log to Firestore asynchronously
      try {
        await addDoc(collection(db, "samfair_audits"), {
          endpoint: selectedAedt,
          timestamp: new Date().toISOString(),
          user: user.email || user.uid,
          results_count: data.audit_results?.length || 0,
          flagged_count: data.audit_results?.filter((r:any) => r.flagged).length || 0
        });
      } catch (e) {
        console.error("Firestore logging skipped.", e);
      }

    } catch (e: any) {
      toast.error(e.message || "Audit failed", { id: toastId });
    } finally {
      setAuditing(false);
    }
  };

  const handleRemediate = async (feature: string, weight: number) => {
    if (!currentSeed) {
      toast.error("Must run audit first");
      return;
    }
    
    const toastId = toast.loading(`Remediating ${feature}...`);
    try {
      const res = await fetch("/_/backend/remediate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feature, weight, seed: currentSeed }),
      });
      if (!res.ok) throw new Error("Remediation failed");
      
      const data = await res.json();
      setAuditResults(data.audit_results);
      toast.success(`Weights updated`, { id: toastId });
    } catch (e: any) {
      toast.error(e.message || "Remediation failed", { id: toastId });
    }
  };

  const handleDownload = () => {
    toast.success("Downloading DPIA Report...");
    window.location.href = "/_/backend/download_report";
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.15),rgba(255,255,255,0))] selection:bg-purple-500/30">
      
      <nav className="border-b border-white/10 bg-black/20 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center shadow-lg shadow-purple-500/30">
              <span className="font-bold text-white text-sm">SF</span>
            </div>
            <span className="font-bold text-white tracking-wide">SamFair Cloud</span>
            {user.isEvaluator && (
              <span className="ml-2 bg-yellow-500/20 text-yellow-400 text-xs px-2 py-0.5 rounded border border-yellow-500/30 font-medium">EVALUATOR</span>
            )}
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-400">{user.email || user.displayName}</span>
            <button onClick={logout} className="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <header className="mb-10 text-center">
          <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/60 mb-3 tracking-tight">Compliance Dashboard</h1>
          <p className="text-gray-400 max-w-xl mx-auto text-sm">Discover, Audit, and Explain opaque AI decisions locally.</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 space-y-8">
            <AedtDiscovery onDiscovered={(tools) => {
              setAedts(tools);
              if (tools.length > 0) toast.success(`Found ${tools.length} AEDT models`);
            }} />

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
                <button onClick={handleDownload} className="bg-green-600 hover:bg-green-500 text-white px-6 py-2 rounded-lg font-medium shadow-[0_0_15px_rgba(22,163,74,0.4)] transition-all">
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
