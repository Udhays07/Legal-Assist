"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Shield, Sparkles, User, ArrowRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { API_BASE_URL, API_ENDPOINTS } from "@/features/admin/api/api.constants";

interface MockUser {
  id: string;
  name: string;
  role: string;
}

export default function LoginGateway() {
  const router = useRouter();
  const [isNavigating, setIsNavigating] = useState<string | null>(null);
  const [users, setUsers] = useState<MockUser[]>([]);
  const [loadingUsers, setLoadingUsers] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE_URL}${API_ENDPOINTS.auth.users}`)
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoadingUsers(false);
      })
      .catch(err => {
        console.error("Failed to load users:", err);
        setLoadingUsers(false);
      });
  }, []);

  const handleLogin = (role: "user" | "admin") => {
    setIsNavigating(role);
    const userMatched = users.find(u => u.role === role);
    const validId = userMatched?.id || "123e4567-e89b-12d3-a456-426614174000"; // Fallback safety
    
    // Set the corresponding ID in localStorage based on role
    localStorage.setItem("legal_assist_user_id", validId);
    
    if (role === "admin") {
      router.push("/admin");
    } else {
      router.push("/user");
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-background relative overflow-hidden">
      {/* Top Bar for Theme Toggle */}
      <div className="absolute top-0 right-0 p-6 z-20">
        <ThemeToggle />
      </div>

      <main className="flex-1 flex flex-col items-center justify-center relative p-6 w-full max-w-5xl mx-auto z-10">
        <div className="text-center mb-12 space-y-4">
          <div className="inline-flex items-center justify-center p-4 bg-primary/10 rounded-2xl mb-2">
            <Sparkles className="h-10 w-10 text-primary" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-foreground font-[family-name:var(--font-headline)]">
            Legal Assistant AI
          </h1>
          <p className="text-muted-foreground text-lg max-w-md mx-auto">
            Select your role to access the intelligent know-your-rights framework.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl">
          {/* User Card */}
          <div className="relative group rounded-2xl border border-border bg-card p-8 hover:border-primary/50 transition-all shadow-sm hover:shadow-md flex flex-col items-center text-center">
            <div className="h-16 w-16 bg-blue-500/10 text-blue-500 rounded-full flex items-center justify-center mb-6">
              <User className="h-8 w-8" />
            </div>
            <h2 className="text-2xl font-semibold text-foreground mb-3">Login as User</h2>
            <p className="text-muted-foreground text-sm mb-8 flex-1">
              Access the AI Chat Assistant, query legal documents, and explore your rights securely.
            </p>
            <Button 
              onClick={() => handleLogin("user")} 
              disabled={isNavigating !== null || loadingUsers}
              className="w-full gap-2 transition-all p-6 text-base"
              variant={isNavigating === "admin" ? "secondary" : "default"}
            >
              {isNavigating === "user" || loadingUsers ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <>
                  Continue as User <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </div>

          {/* Admin Card */}
          <div className="relative group rounded-2xl border border-border bg-card p-8 hover:border-primary/50 transition-all shadow-sm hover:shadow-md flex flex-col items-center text-center">
            <div className="h-16 w-16 bg-purple-500/10 text-purple-500 rounded-full flex items-center justify-center mb-6">
              <Shield className="h-8 w-8" />
            </div>
            <h2 className="text-2xl font-semibold text-foreground mb-3">Login as Admin</h2>
            <p className="text-muted-foreground text-sm mb-8 flex-1">
              Access the Dashboard, manage legal categories, view system metrics, and upload documents.
            </p>
            <Button 
              onClick={() => handleLogin("admin")} 
              disabled={isNavigating !== null || loadingUsers}
              className="w-full gap-2 transition-all p-6 text-base"
              variant={isNavigating === "user" ? "secondary" : "default"}
            >
              {isNavigating === "admin" || loadingUsers ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <>
                  Continue as Admin <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}
