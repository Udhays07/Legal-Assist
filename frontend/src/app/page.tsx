export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 md:p-24 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px] -z-10" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-accent/20 rounded-full blur-[120px] -z-10" />

      <div className="w-full max-w-5xl flex flex-col items-center gap-12 text-center">
        {/* Badge */}
        <div className="glass px-4 py-1.5 rounded-full border border-glass-border animate-fade-in">
          <span className="text-xs font-semibold tracking-wider uppercase text-accent">
            AI-Powered Legal Intelligence
          </span>
        </div>

        {/* Hero Content */}
        <div className="space-y-6">
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight font-display gradient-text pb-2">
            S8 Legal Assistant
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            The next generation of legal research, document analysis, and case intelligence.
            Empowering professionals with precision and speed.
          </p>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 items-center">
          <button className="px-8 py-4 bg-primary text-white rounded-xl font-semibold shadow-[0_0_20px_rgba(59,130,246,0.5)] hover:bg-primary/90 transition-all hover:scale-105 active:scale-95 cursor-pointer">
            Get Started Free
          </button>
          <button className="px-8 py-4 glass text-foreground rounded-xl font-semibold hover:bg-white/[0.05] transition-all hover:scale-105 active:scale-95 cursor-pointer">
            View Case Studies
          </button>
        </div>

        {/* glass feature mockup */}
        <div className="w-full aspect-video glass rounded-2xl border border-glass-border mt-12 shadow-2xl relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-accent/10 opacity-50" />
          <div className="p-8 flex flex-col h-full gap-4">
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500/50" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
              <div className="w-3 h-3 rounded-full bg-green-500/50" />
            </div>
            <div className="flex-1 flex items-center justify-center border-t border-glass-border pt-4">
              <span className="text-muted-foreground font-mono text-sm">
                Initialize Case Intelligence Engine... [Ready]
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer hint */}
      <footer className="mt-24 text-muted-foreground/40 text-sm">
        &copy; 2026 S8 Legal Solutions. Built with Next.js & AI.
      </footer>
    </main>
  );
}
