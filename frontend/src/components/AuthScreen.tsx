"use client";

import { useAuth } from "@/lib/AuthContext";
import { Shield, LockKeyhole, UserCog } from "lucide-react";

export default function AuthScreen() {
  const { loginWithGoogle, loginAsEvaluator } = useAuth();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#0a0a0a] bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.15),rgba(255,255,255,0))]">
      <div className="w-full max-w-md p-8 bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 shadow-2xl text-center relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/10 blur-3xl rounded-full -mr-20 -mt-20 pointer-events-none"></div>
        
        <div className="inline-flex items-center justify-center p-4 bg-white/5 rounded-2xl border border-white/10 shadow-2xl mb-8 relative z-10">
          <Shield className="w-12 h-12 text-white" />
        </div>
        
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/60 mb-3 tracking-tight relative z-10">
          SamFair Cloud
        </h1>
        <p className="text-gray-400 mb-8 relative z-10">
          Enterprise AI Bias Auditing and DPDP Compliance Platform.
        </p>

        <div className="space-y-4 relative z-10">
          <button
            onClick={loginWithGoogle}
            className="w-full flex items-center justify-center gap-3 bg-white text-black hover:bg-gray-200 px-6 py-3.5 rounded-xl font-bold transition-all"
          >
            <LockKeyhole className="w-5 h-5" />
            Sign in with Google
          </button>
          
          <div className="relative py-4">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-white/10"></div>
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="bg-[#121212] px-2 text-gray-500 uppercase tracking-widest rounded">or</span>
            </div>
          </div>

          <button
            onClick={loginAsEvaluator}
            className="w-full flex items-center justify-center gap-3 bg-black/40 text-gray-300 hover:text-white border border-white/10 hover:border-white/20 hover:bg-white/5 px-6 py-3.5 rounded-xl font-medium transition-all"
          >
            <UserCog className="w-5 h-5" />
            Evaluation Backdoor
          </button>
        </div>
      </div>
      
      <p className="mt-8 text-xs text-gray-600">
        By signing in, you agree to the SamFair Terms of Service.
      </p>
    </div>
  );
}
