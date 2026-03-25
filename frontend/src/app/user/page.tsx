"use client";

import { useCategories } from "@/features/admin/hooks/useCategories";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import Link from "next/link";
import { ArrowRight, MessageSquare, Scale, BookOpen, Search, ShieldCheck } from "lucide-react";

export default function UserCategoriesPage() {
  const { categories, isLoading, error } = useCategories();

  return (
    <div className="min-h-screen bg-surface-container-lowest">
      {/* Hero Section */}
      <section className="hero-gradient relative pt-32 pb-24 px-8 overflow-hidden">
        <div className="max-w-7xl mx-auto relative z-10 flex flex-col md:flex-row items-center gap-12">
          <div className="flex-1">
            <span className="inline-block text-tertiary-fixed-dim font-label text-sm uppercase tracking-widest mb-4">
              Explore Legal Knowledge
            </span>
            <h1 className="font-headline text-5xl md:text-7xl text-on-primary leading-tight mb-8">
              Legal Categories <br />
              <span className="serif-italic">&amp; Resources.</span>
            </h1>
            <p className="text-on-primary-container text-lg md:text-xl max-w-lg mb-10 leading-relaxed">
              Browse through a comprehensive list of legal categories to understand your rights, identify legal remedies, and get immediate guidance tailored to your concerns.
            </p>
            <div className="flex gap-4">
               <Link href="/user/chat">
                 <Button className="bg-tertiary-fixed text-on-tertiary-fixed hover:bg-tertiary-fixed/90 px-8 py-6 rounded-lg font-bold text-lg shadow-xl hover:-translate-y-1 transition-transform group">
                   Start Consulting
                   <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform inline" />
                 </Button>
               </Link>
            </div>
          </div>
          
          <div className="hidden md:flex flex-1 justify-center relative">
            <div className="absolute inset-0 bg-secondary/20 rounded-full blur-3xl"></div>
             {/* Some visual graphic for categories */}
             <div className="grid grid-cols-2 gap-4 relative">
                <div className="bg-white/10 backdrop-blur-xl border border-white/20 p-6 rounded-2xl shadow-2xl flex flex-col items-center justify-center translate-y-8 hover:scale-105 transition-transform duration-500">
                   <Scale className="w-12 h-12 text-tertiary-fixed-dim mb-4" />
                   <span className="text-on-primary font-bold text-center">Civil Law</span>
                </div>
                <div className="bg-white/10 backdrop-blur-xl border border-white/20 p-6 rounded-2xl shadow-2xl flex flex-col items-center justify-center -translate-y-4 hover:scale-105 transition-transform duration-500">
                   <ShieldCheck className="w-12 h-12 text-secondary-fixed mb-4" />
                   <span className="text-on-primary font-bold text-center">Rights</span>
                </div>
                <div className="bg-white/10 backdrop-blur-xl border border-white/20 p-6 rounded-2xl shadow-2xl flex flex-col items-center justify-center translate-y-4 hover:scale-105 transition-transform duration-500">
                   <BookOpen className="w-12 h-12 text-primary-fixed mb-4" />
                   <span className="text-on-primary font-bold text-center">Guides</span>
                </div>
                <div className="bg-white/10 backdrop-blur-xl border border-white/20 p-6 rounded-2xl shadow-2xl flex flex-col items-center justify-center -translate-y-8 hover:scale-105 transition-transform duration-500">
                   <Search className="w-12 h-12 text-error mb-4" />
                   <span className="text-on-primary font-bold text-center">Research</span>
                </div>
             </div>
          </div>
        </div>
      </section>

      {/* Categories Grid */}
      <section className="py-24 px-8 max-w-7xl mx-auto">
         <div className="mb-12">
            <h2 className="font-headline text-4xl text-primary mb-4">Browse by Area of Law</h2>
            <p className="text-on-surface-variant max-w-2xl">
              Select a category below to explore specific guides and provisions, or ask our intelligent assistant directly.
            </p>
         </div>

         {error && (
            <div className="bg-error/10 text-error p-6 rounded-xl mb-12">
               Failed to load categories: {error}
            </div>
         )}
         
         <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {isLoading ? (
               Array.from({ length: 6 }).map((_, i) => (
                 <div key={i} className="bg-surface-container-low p-6 rounded-2xl border border-outline-variant/20 flex flex-col gap-4">
                     <Skeleton className="h-6 w-3/4" />
                     <Skeleton className="h-20 w-full" />
                 </div>
               ))
            ) : categories.length === 0 ? (
                 <div className="col-span-full py-12 text-center text-on-surface-variant bg-surface-container-low rounded-2xl border border-outline-variant/10">
                     No categories available at the moment.
                 </div>
            ) : (
               categories.map(category => (
                 <div key={category.id} className="bg-surface-container-low hover:bg-surface-container transition-colors p-8 rounded-2xl border border-outline-variant/20 group cursor-pointer shadow-sm hover:shadow-md">
                    <h3 className="font-headline text-2xl text-primary mb-3 group-hover:text-secondary transition-colors">
                       {category.title}
                    </h3>
                    {category.description && (
                       <p className="text-on-surface-variant line-clamp-3 leading-relaxed">
                          {category.description}
                       </p>
                    )}
                    <div className="mt-6 flex items-center text-secondary font-bold text-sm tracking-widest uppercase">
                       Explore <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform" />
                    </div>
                 </div>
               ))
            )}
         </div>
      </section>

      {/* How Chat Works Demo */}
      <section className="bg-surface-container-low py-32 px-8 border-t border-outline-variant/10">
         <div className="max-w-7xl mx-auto grid xl:grid-cols-2 gap-16 items-center">
            <div>
               <h2 className="font-headline text-4xl md:text-5xl text-primary mb-6">
                 Experience the <br className="hidden md:block" />
                 <span className="serif-italic">Legal Chatbot</span>
               </h2>
               <p className="text-on-surface-variant text-lg mb-8 leading-relaxed max-w-xl">
                 Don't know where to start? Our advanced Legal Assistant is ready to help. Describe your situation in plain language, and the chatbot will instantly analyze it, identify the relevant legal guidelines, and provide clear next steps.
               </p>
               
               <div className="space-y-8 mb-12">
                  <div className="flex gap-5 items-start">
                     <div className="bg-primary/10 p-4 rounded-2xl text-primary mt-1 shadow-sm">
                        <MessageSquare className="w-6 h-6" />
                     </div>
                     <div>
                        <h4 className="font-bold text-primary text-xl mb-1">Natural Conversations</h4>
                        <p className="text-on-surface-variant">Ask questions as if you were talking to a regular person or an expert.</p>
                     </div>
                  </div>
                  <div className="flex gap-5 items-start">
                     <div className="bg-secondary/10 p-4 rounded-2xl text-secondary mt-1 shadow-sm">
                        <Search className="w-6 h-6" />
                     </div>
                     <div>
                        <h4 className="font-bold text-primary text-xl mb-1">Actionable Guidance</h4>
                        <p className="text-on-surface-variant">Get specific, actionable information on laws and practical steps to take.</p>
                     </div>
                  </div>
               </div>

               <Link href="/user/chat">
                 <Button className="bg-primary hover:bg-primary/90 text-on-primary px-10 py-7 rounded-xl font-bold text-xl shadow-xl hover:-translate-y-1 transition-transform group flex items-center gap-3">
                   Go to Legal Chat
                   <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
                 </Button>
               </Link>
            </div>

            {/* Chat Demo Interaction Mockup */}
            <div className="relative w-full max-w-lg mx-auto xl:mx-0 xl:ml-auto">
               <div className="absolute inset-0 bg-primary/20 rounded-[2.5rem] blur-3xl transform rotate-3"></div>
               <div className="relative bg-surface-container-lowest border border-outline-variant/20 rounded-3xl shadow-2xl overflow-hidden flex flex-col h-[550px]">
                  {/* Chat Header */}
                  <div className="bg-surface-container px-6 py-5 flex items-center gap-4 border-b border-outline-variant/20">
                     <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center text-on-primary font-bold shadow-inner">
                        LA
                     </div>
                     <div>
                        <div className="font-bold text-primary text-lg">Legal Assistant</div>
                        <div className="text-xs text-secondary font-medium tracking-wide flex items-center gap-2">
                           <span className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse"></span> ONLINE
                        </div>
                     </div>
                  </div>
                  
                  {/* Chat Messages */}
                  <div className="flex-1 p-6 flex flex-col gap-6 overflow-hidden relative">
                     {/* User Message */}
                     <div className="self-end bg-primary text-on-primary px-6 py-4 rounded-2xl rounded-tr-sm max-w-[85%] shadow-md transform transition-all translate-y-0 opacity-100">
                        <p className="text-[15px] leading-relaxed">My landlord is keeping my security deposit unfairly. What can I do?</p>
                     </div>
                     
                     {/* Assistant Answer */}
                     <div className="self-start bg-surface-container-low border border-outline-variant/10 text-on-surface px-6 py-5 rounded-2xl rounded-tl-sm max-w-[90%] shadow-md transform transition-all translate-y-0 opacity-100">
                        <p className="mb-4 text-[15px] leading-relaxed">Under Indian tenancy laws, a landlord cannot withhold a security deposit without valid reasons (like unpaid rent or damages).</p>
                        <div className="bg-surface-container px-5 py-4 rounded-xl border-l-4 border-secondary text-[14px] leading-relaxed shadow-sm">
                           <strong className="block text-primary mb-2 font-bold uppercase tracking-wider text-xs">Recommended Action</strong>
                           <ul className="space-y-2 text-on-surface-variant">
                             <li className="flex gap-2 items-start"><span className="text-secondary font-bold">1.</span> Send a formal legal notice for recovery.</li>
                             <li className="flex gap-2 items-start"><span className="text-secondary font-bold">2.</span> If unresolved, approach a Rent Control Court.</li>
                           </ul>
                        </div>
                     </div>

                     {/* Typing indicator */}
                     <div className="self-start bg-surface-container-low border border-outline-variant/10 px-6 py-4 rounded-2xl rounded-tl-sm shadow-md mt-auto mb-2 flex items-center gap-2">
                         <span className="text-xs font-medium text-on-surface-variant uppercase tracking-widest mr-1">Generating</span>
                        <div className="flex gap-1.5 items-center">
                           <span className="w-1.5 h-1.5 bg-secondary rounded-full animate-bounce"></span>
                           <span className="w-1.5 h-1.5 bg-secondary rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                           <span className="w-1.5 h-1.5 bg-secondary rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                        </div>
                     </div>
                     
                     <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-surface-container-lowest to-transparent pointer-events-none"></div>
                  </div>
                  
                  {/* Chat Input Dummy */}
                  <div className="p-5 border-t border-outline-variant/20 bg-surface-container/50">
                     <div className="bg-surface-container-lowest border border-outline-variant/20 rounded-full pl-6 pr-2 py-2 text-on-surface-variant text-sm flex justify-between items-center shadow-inner">
                        <span className="opacity-50 font-medium">Type your legal query here...</span>
                        <div className="bg-primary hover:bg-primary/90 transition-colors text-on-primary p-3 rounded-full shadow-md cursor-pointer">
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
