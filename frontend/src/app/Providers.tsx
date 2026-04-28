"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "@/lib/AuthContext";
import { Toaster } from "react-hot-toast";

const queryClient = new QueryClient();

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        {children}
        <Toaster position="bottom-right" toastOptions={{
          style: { background: '#333', color: '#fff', borderRadius: '10px' },
          success: { iconTheme: { primary: '#22c55e', secondary: '#fff' } }
        }}/>
      </AuthProvider>
    </QueryClientProvider>
  );
}
