"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Sparkles, ArrowRight, Loader2, Scale, ShieldCheck, UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { saveAuth, getToken, getRole, isAdmin, clearAuth } from "@/lib/auth";
import { apiLogin, apiRegister } from "@/lib/api/auth";

type Tab = "login" | "signup";

export default function AuthPage() {
  const router = useRouter();

  // Tab state
  const [tab, setTab] = useState<Tab>("login");

  // Form fields
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // UI state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [guestLoading, setGuestLoading] = useState(false);

  // Auto-redirect if already authenticated
  useEffect(() => {
    const token = getToken();
    if (token) {
      const role = getRole();
      if (role === "admin") {
        router.replace("/admin");
      } else {
        router.replace("/user");
      }
    }
  }, [router]);

  const resetError = () => setError(null);

  // ── Login ──────────────────────────────────────────────────────────────
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await apiLogin(email, password);
      saveAuth({
        token: data.access_token,
        role: data.role,
        name: data.name,
        userId: data.user_id,
      });
      if (data.role === "admin") {
        router.push("/admin");
      } else {
        router.push("/user");
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // ── Register ───────────────────────────────────────────────────────────
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Please enter your full name.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await apiRegister(name, email, password);
      saveAuth({
        token: data.access_token,
        role: data.role,
        name: data.name,
        userId: data.user_id,
      });
      router.push("/user");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // ── Guest ──────────────────────────────────────────────────────────────
  const handleGuest = () => {
    setGuestLoading(true);
    clearAuth(); // clear any stale state
    router.push("/user");
  };

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-background px-4">
      {/* Theme toggle */}
      <div className="absolute right-0 top-0 p-6 z-20">
        <ThemeToggle />
      </div>

      {/* Decorative background glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-10 overflow-hidden"
      >
        <div className="absolute -top-32 left-1/2 h-[500px] w-[700px] -translate-x-1/2 rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-[300px] w-[400px] rounded-full bg-blue-500/5 blur-3xl" />
      </div>

      {/* Header */}
      <div className="mb-8 flex flex-col items-center gap-3 text-center">
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
          <Scale className="h-8 w-8 text-primary" />
        </div>
        <h1 className="text-4xl font-bold tracking-tight text-foreground md:text-5xl">
          Legal Assistant AI
        </h1>
        <p className="max-w-sm text-base text-muted-foreground">
          Your AI-powered know-your-rights companion. Sign in or continue as a guest.
        </p>
      </div>

      {/* Card */}
      <div className="w-full max-w-md rounded-2xl border border-border bg-card p-8 shadow-lg">
        {/* Tab switcher */}
        <div className="mb-6 flex rounded-xl bg-muted p-1">
          <button
            id="tab-login"
            onClick={() => { setTab("login"); resetError(); }}
            className={`flex flex-1 items-center justify-center gap-2 rounded-lg py-2 text-sm font-medium transition-all ${tab === "login"
              ? "bg-background text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground"
              }`}
          >
            <ShieldCheck className="h-4 w-4" />
            Login
          </button>
          <button
            id="tab-signup"
            onClick={() => { setTab("signup"); resetError(); }}
            className={`flex flex-1 items-center justify-center gap-2 rounded-lg py-2 text-sm font-medium transition-all ${tab === "signup"
              ? "bg-background text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground"
              }`}
          >
            <UserPlus className="h-4 w-4" />
            Sign Up
          </button>
        </div>

        {/* Form */}
        <form
          id={tab === "login" ? "form-login" : "form-signup"}
          onSubmit={tab === "login" ? handleLogin : handleRegister}
          className="flex flex-col gap-4"
        >
          {/* Name — sign up only */}
          {tab === "signup" && (
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="input-name">Full Name</Label>
              <Input
                id="input-name"
                type="text"
                placeholder="John Doe"
                value={name}
                onChange={(e) => { setName(e.target.value); resetError(); }}
                required
                autoComplete="name"
              />
            </div>
          )}

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="input-email">Email</Label>
            <Input
              id="input-email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => { setEmail(e.target.value); resetError(); }}
              required
              autoComplete="email"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="input-password">Password</Label>
            <Input
              id="input-password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => { setPassword(e.target.value); resetError(); }}
              required
              autoComplete={tab === "login" ? "current-password" : "new-password"}
            />
          </div>

          {/* Inline error */}
          {error && (
            <p
              id="auth-error"
              className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive"
            >
              {error}
            </p>
          )}

          <Button
            id="btn-submit"
            type="submit"
            disabled={loading}
            className="mt-1 w-full gap-2 py-5 text-base"
          >
            {loading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <>
                {tab === "login" ? "Login" : "Create Account"}
                <Sparkles className="h-4 w-4" />
              </>
            )}
          </Button>
        </form>

        {/* Divider */}
        <div className="my-6 flex items-center gap-4">
          <div className="h-px flex-1 bg-border" />
          <span className="text-xs text-muted-foreground">or</span>
          <div className="h-px flex-1 bg-border" />
        </div>

        {/* Guest CTA */}
        <Button
          id="btn-guest"
          variant="outline"
          disabled={guestLoading}
          onClick={handleGuest}
          className="w-full gap-2 py-5 text-base text-white"
        >
          {guestLoading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <>
              Continue without login
              <ArrowRight className="h-4 w-4" />
            </>
          )}
        </Button>

        <p className="mt-4 text-center text-xs text-muted-foreground">
          Guest access provides limited features. Sign up for a full experience.
        </p>
      </div>
    </div>
  );
}
