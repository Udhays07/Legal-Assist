"use client";

import { useCategories } from "@/features/admin/hooks/useCategories";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import Link from "next/link";
import { ArrowRight, MessageSquare, Scale, BookOpen, Search, ShieldCheck, Sparkles } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";

export default function UserCategoriesPage() {
  const { categories, isLoading, error } = useCategories();

  return (
    <div className="min-h-screen bg-background relative selection:bg-primary/20">
      
      {/* Top Navigation */}
      <div className="absolute top-0 w-full p-6 z-50 flex justify-between items-center max-w-7xl mx-auto left-0 right-0">
        <div className="flex items-center gap-2 font-bold text-lg text-foreground tracking-wide flex-shrink-0">
          <Sparkles className="w-5 h-5 text-primary" />
          Legal Assistant AI
        </div>
        <div className="flex items-center gap-4">
           <Link href="/user/chat">
             <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground h-10 w-10">
               <MessageSquare className="w-5 h-5" />
             </Button>
           </Link>
           <Link href="/">
             <Button variant="ghost" className="text-muted-foreground hover:text-foreground">Logout</Button>
           </Link>
           <ThemeToggle />
        </div>
      </div>

      {/* Hero Section */}
      <section className="relative pt-40 pb-24 px-8 overflow-hidden">
        {/* Background glow effects */}
        <div className="absolute top-0 right-0 -mr-32 -mt-32 w-96 h-96 bg-primary/10 rounded-full blur-[100px] pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 -ml-32 w-80 h-80 bg-secondary/10 rounded-full blur-[100px] pointer-events-none"></div>
        
        <div className="max-w-7xl mx-auto relative z-10 flex flex-col lg:flex-row items-center gap-16">
          <div className="flex-1 text-center lg:text-left">
            <span className="inline-block text-primary font-bold text-sm tracking-widest mb-6 uppercase bg-primary/10 px-4 py-2 rounded-full border border-primary/20">
              Explore Legal Knowledge
            </span>
            <h1 className="font-headline text-5xl md:text-7xl text-foreground font-extrabold leading-tight mb-8">
              Understand Your <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">Legal Rights.</span>
            </h1>
            <p className="text-muted-foreground text-lg md:text-xl max-w-lg mb-10 leading-relaxed mx-auto lg:mx-0">
              Browse through a comprehensive list of legal categories to understand your rights, identify legal remedies, and get immediate guidance tailored to your concerns.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
               <Link href="/user/chat">
                 <Button className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 py-6 rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(59,130,246,0.3)] hover:shadow-[0_0_30px_rgba(59,130,246,0.5)] hover:-translate-y-1 transition-all duration-300 group">
                   Start Consulting
                   <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform inline" />
                 </Button>
               </Link>
            </div>
          </div>
          
          <div className="hidden lg:flex flex-1 justify-center relative w-full perspective-1000">
             {/* Floating UI Elements Grid */}
             <div className="grid grid-cols-2 gap-6 relative max-w-md w-full">
                <div className="bg-card/40 backdrop-blur-xl border border-white/10 dark:border-white/5 p-8 rounded-3xl shadow-2xl flex flex-col items-center justify-center translate-y-8 hover:translate-y-4 hover:shadow-primary/20 transition-all duration-500">
                   <div className="w-16 h-16 rounded-full bg-blue-500/10 flex items-center justify-center mb-4">
                     <Scale className="w-8 h-8 text-blue-500" />
                   </div>
                   <span className="text-foreground font-bold text-center text-lg">Civil Law</span>
                </div>
                <div className="bg-card/40 backdrop-blur-xl border border-white/10 dark:border-white/5 p-8 rounded-3xl shadow-2xl flex flex-col items-center justify-center -translate-y-4 hover:-translate-y-8 hover:shadow-primary/20 transition-all duration-500">
                   <div className="w-16 h-16 rounded-full bg-emerald-500/10 flex items-center justify-center mb-4">
                     <ShieldCheck className="w-8 h-8 text-emerald-500" />
                   </div>
                   <span className="text-foreground font-bold text-center text-lg">Rights</span>
                </div>
                <div className="bg-card/40 backdrop-blur-xl border border-white/10 dark:border-white/5 p-8 rounded-3xl shadow-2xl flex flex-col items-center justify-center translate-y-4 hover:translate-y-0 hover:shadow-primary/20 transition-all duration-500">
                   <div className="w-16 h-16 rounded-full bg-purple-500/10 flex items-center justify-center mb-4">
                     <BookOpen className="w-8 h-8 text-purple-500" />
                   </div>
                   <span className="text-foreground font-bold text-center text-lg">Guides</span>
                </div>
                <div className="bg-card/40 backdrop-blur-xl border border-white/10 dark:border-white/5 p-8 rounded-3xl shadow-2xl flex flex-col items-center justify-center -translate-y-8 hover:-translate-y-12 hover:shadow-primary/20 transition-all duration-500">
                   <div className="w-16 h-16 rounded-full bg-rose-500/10 flex items-center justify-center mb-4">
                     <Search className="w-8 h-8 text-rose-500" />
                   </div>
                   <span className="text-foreground font-bold text-center text-lg">Research</span>
                </div>
             </div>
          </div>
        </div>
      </section>

      {/* Categories Grid */}
      <section className="py-24 px-8 max-w-7xl mx-auto relative z-10">
         <div className="mb-16 text-center md:text-left">
            <h2 className="font-headline text-4xl font-bold text-foreground mb-4">Browse by Area of Law</h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto md:mx-0">
              Select a category below to explore specific guides and provisions, or ask our intelligent assistant directly.
            </p>
         </div>

         {error && (
            <div className="bg-destructive/10 text-destructive border border-destructive/20 p-6 rounded-xl mb-12">
               Failed to load categories: {error}
            </div>
         )}
         
         <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {isLoading ? (
               Array.from({ length: 6 }).map((_, i) => (
                 <div key={i} className="bg-muted/30 p-8 rounded-3xl border border-border flex flex-col gap-4">
                     <Skeleton className="h-6 w-3/4 mb-2 bg-muted/50" />
                     <Skeleton className="h-24 w-full bg-muted/50" />
                 </div>
               ))
            ) : categories.length === 0 ? (
                 <div className="col-span-full py-20 text-center text-muted-foreground bg-muted/20 rounded-3xl border border-border/50">
                     No categories available at the moment.
                 </div>
            ) : (
               categories.map(category => (
                 <div key={category.id} className="bg-card hover:bg-muted/30 transition-all duration-300 p-8 rounded-3xl border border-border group shadow-sm hover:shadow-xl hover:-translate-y-1 cursor-pointer">
                    <h3 className="font-headline text-2xl font-bold text-foreground mb-4 group-hover:text-primary transition-colors">
                       {category.title}
                    </h3>
                    {category.description && (
                       <p className="text-muted-foreground line-clamp-3 leading-relaxed mb-6">
                          {category.description}
                       </p>
                    )}
                    <div className="mt-auto flex items-center text-primary font-bold text-sm tracking-widest uppercase">
                       Explore <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform" />
                    </div>
                 </div>
               ))
            )}
         </div>
      </section>

      {/* How Chat Works Demo */}
      <section className="bg-muted/10 py-32 px-8 border-t border-border mt-12 relative overflow-hidden">
         <div className="max-w-7xl mx-auto grid xl:grid-cols-2 gap-16 items-center relative z-10">
            <div>
               <h2 className="font-headline text-4xl md:text-5xl font-bold text-foreground mb-6 leading-tight">
                 Experience the <br className="hidden xl:block" />
                 <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">Legal Chatbot</span>
               </h2>
               <p className="text-muted-foreground text-lg mb-10 leading-relaxed max-w-xl">
                 Don't know where to start? Our advanced Legal Assistant is ready to help. Describe your situation in plain language, and the chatbot will instantly analyze it, identify the relevant legal guidelines, and provide clear next steps.
               </p>
               
               <div className="space-y-8 mb-12">
                  <div className="flex gap-6 items-start">
                     <div className="bg-primary/10 p-4 rounded-2xl text-primary mt-1 shadow-sm border border-primary/10">
                        <MessageSquare className="w-6 h-6" />
                     </div>
                     <div>
                        <h4 className="font-bold text-foreground text-xl mb-2">Natural Conversations</h4>
                        <p className="text-muted-foreground leading-relaxed">Ask questions as if you were talking to an expert. Our AI understands legal nuance naturally.</p>
                     </div>
                  </div>
                  <div className="flex gap-6 items-start">
                     <div className="bg-accent/10 p-4 rounded-2xl text-accent mt-1 shadow-sm border border-accent/10">
                        <Search className="w-6 h-6" />
                     </div>
                     <div>
                        <h4 className="font-bold text-foreground text-xl mb-2">Actionable Guidance</h4>
                        <p className="text-muted-foreground leading-relaxed">Get specific, actionable information on laws and practical steps to take instantly.</p>
                     </div>
                  </div>
               </div>

               <Link href="/user/chat">
                 <Button size="lg" className="h-16 px-10 rounded-2xl font-bold text-lg shadow-lg shadow-primary/20 hover:-translate-y-1 transition-all group flex items-center gap-3 w-full sm:w-auto">
                   Launch Legal Chat
                   <ArrowRight className="w-5 h-5 group-hover:translate-x-2 transition-transform" />
                 </Button>
               </Link>
            </div>

            {/* Chat Demo Interaction Mockup */}
            <div className="relative w-full max-w-xl mx-auto xl:mx-0 xl:ml-auto">
               <div className="absolute inset-0 bg-gradient-to-tr from-primary/30 to-accent/30 rounded-[3rem] blur-3xl transform rotate-3 scale-105 pointer-events-none"></div>
               <div className="relative bg-card border border-border rounded-3xl shadow-2xl overflow-hidden flex flex-col h-[600px] z-10 backdrop-blur-sm">
                  {/* Chat Header */}
                  <div className="bg-background/80 backdrop-blur-md px-6 py-5 flex items-center gap-4 border-b border-border z-20 sticky top-0">
                     <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold shadow-md shadow-primary/20">
                        LA
                     </div>
                     <div>
                        <div className="font-bold text-foreground text-lg">Legal Assistant</div>
                        <div className="text-xs text-muted-foreground font-medium tracking-wide flex items-center gap-2">
                           <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-[pulse_2s_ease-in-out_infinite] shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span> ONLINE
                        </div>
                     </div>
                  </div>
                  
                  {/* Chat Messages */}
                  <div className="flex-1 p-6 flex flex-col gap-6 overflow-hidden relative bg-[url('/noise.png')] bg-repeat bg-opacity-5">
                     {/* User Message */}
                     <div className="self-end bg-primary text-primary-foreground px-6 py-4 rounded-2xl rounded-tr-sm max-w-[85%] shadow-md">
                        <p className="text-[15px] leading-relaxed">My landlord is keeping my security deposit unfairly. What can I do?</p>
                     </div>
                     
                     {/* Assistant Answer */}
                     <div className="self-start bg-muted/50 border border-border text-foreground px-6 py-5 rounded-2xl rounded-tl-sm max-w-[90%] shadow-sm">
                        <p className="mb-5 text-[15px] leading-relaxed">Under standard tenancy laws, a landlord cannot withhold a security deposit without valid documented reasons (like unpaid rent or severe damages).</p>
                        <div className="bg-background px-5 py-4 rounded-xl border-l-4 border-primary text-[14px] leading-relaxed shadow-sm">
                           <strong className="block text-primary mb-3 font-bold uppercase tracking-wider text-xs">Recommended Action</strong>
                           <ul className="space-y-3 text-muted-foreground">
                             <li className="flex gap-3 items-start"><span className="text-primary font-bold h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center shrink-0 text-xs">1</span> Send a formal written legal notice demanding recovery.</li>
                             <li className="flex gap-3 items-start"><span className="text-primary font-bold h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center shrink-0 text-xs">2</span> If unresolved within 15 days, approach the local Rent Control Court or Small Claims Court.</li>
                           </ul>
                        </div>
                     </div>

                     {/* Typing indicator */}
                     <div className="self-start bg-muted/50 border border-border px-6 py-4 rounded-2xl rounded-tl-sm shadow-sm mt-auto mb-2 flex items-center gap-3">
                         <span className="text-xs font-semibold text-muted-foreground uppercase tracking-widest">Compiling Context</span>
                        <div className="flex gap-1.5 items-center bg-background px-2 py-1 rounded-full border border-border">
                           <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce"></span>
                           <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                           <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                        </div>
                     </div>
                     
                     {/* Fade out absolute overlay */}
                     <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-card to-transparent pointer-events-none z-10"></div>
                  </div>
                  
                  {/* Chat Input Dummy */}
                  <div className="p-6 border-t border-border bg-card/90 backdrop-blur-md relative z-20">
                     <div className="bg-background border border-border rounded-full pl-6 pr-2 py-2.5 text-muted-foreground text-sm flex justify-between items-center shadow-inner hover:border-primary/50 transition-colors">
                        <span className="opacity-70 font-medium">Explain employment contract termination...</span>
                        <div className="bg-primary hover:bg-primary/90 transition-colors text-primary-foreground p-3 rounded-full shadow-md cursor-not-allowed opacity-80">
                           <ArrowRight className="w-4 h-4" />
                        </div>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </section>
    </div>
  );
}
