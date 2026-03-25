"use client";

import React, { useEffect, useRef, useState } from "react";
import { useChat } from "../hooks/useChat";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Loader2, Sparkles, FolderIcon, Home, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { categoriesApi } from "@/features/admin/api/categories.api";
import type { CategoryRead } from "@/features/admin/types/admin.types";
import { ThemeToggle } from "@/components/ThemeToggle";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface ChatInterfaceProps {
    userId?: string;
}

export function ChatInterface({ userId }: ChatInterfaceProps) {
    const [activeUserId, setActiveUserId] = useState<string>("");

    useEffect(() => {
        // Retrieve ID from localStorage, fallback to valid Test User ID if accessed directly without gateway
        let storedId = localStorage.getItem("legal_assist_user_id");
        if (!storedId) {
            storedId = "123e4567-e89b-12d3-a456-426614174000";
            localStorage.setItem("legal_assist_user_id", storedId);
        }
        setActiveUserId(userId || storedId);
    }, [userId]);

    const { messages, isLoading, sendMessage } = useChat(activeUserId);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [categories, setCategories] = useState<CategoryRead[]>([]);
    const [selectedCategoryId, setSelectedCategoryId] = useState<string>("");

    useEffect(() => {
        // Fetch categories when component mounts
        categoriesApi.list().then(setCategories).catch(console.error);
    }, []);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isLoading]);

    const handleSend = (content: string) => {
        sendMessage(content, selectedCategoryId || undefined);
    };

    return (
        <div className="flex flex-col h-full overflow-hidden bg-background relative selection:bg-primary/20">
            {/* Background Aesthetic Elements */}
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.03] pointer-events-none"></div>
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-[120px] pointer-events-none"></div>

            {/* Header / Category Selector top bar */}
            <div className="flex h-14 shrink-0 items-center border-b px-5 justify-between bg-background/60 backdrop-blur-xl z-20 w-full sticky top-0 border-border/50 shadow-sm">
                <div className="flex items-center gap-2">
                    <Link href="/user">
                        <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground h-8 w-8 rounded-lg hover:bg-muted transition-all">
                            <Home className="w-4 h-4" />
                        </Button>
                    </Link>
                    <div className="h-5 w-px bg-border mx-1"></div>
                    <span className="font-bold text-base tracking-tight text-foreground flex items-center gap-2">
                        Legal Assistant AI
                    </span>
                    <div className="flex items-center gap-2 ml-4 px-2 py-1 rounded-lg hover:bg-muted/50 transition-colors group">
                        <FolderIcon className="w-3.5 h-3.5 text-muted-foreground group-hover:text-primary transition-colors" />
                        <Select value={selectedCategoryId || "all"} onValueChange={(val) => setSelectedCategoryId(val === "all" ? "" : val)}>
                            <SelectTrigger className="w-auto min-w-[120px] h-6 text-[11px] bg-transparent border-none shadow-none focus:ring-0 text-muted-foreground group-hover:text-foreground font-bold px-0 uppercase tracking-wider">
                                <SelectValue placeholder="All Categories" />
                            </SelectTrigger>
                            <SelectContent className="rounded-2xl border-border/50 shadow-2xl">
                                <SelectItem value="all">All Categories</SelectItem>
                                {categories.map((cat) => (
                                    <SelectItem key={cat.id} value={cat.id}>{cat.title}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                </div>
                <div className="flex items-center gap-1">
                    <ThemeToggle />
                </div>
            </div>

            {/* Chat Area */}
            <ScrollArea className="flex-1 w-full min-h-0 relative z-10 transition-all duration-300">
                <div className="flex flex-col min-h-full pb-40 max-w-3xl mx-auto pt-6">
                    {messages.length === 0 ? (
                        <div className="flex-1 flex flex-col items-center justify-center text-muted-foreground p-12 text-center gap-8 mt-20 animate-in fade-in zoom-in-95 duration-700">
                            <div className="h-24 w-24 bg-gradient-to-br from-primary/20 to-accent/20 rounded-[2.5rem] flex items-center justify-center shadow-2xl border border-white/20 dark:border-white/5 relative group">
                                <div className="absolute inset-0 bg-primary/20 rounded-[2.5rem] blur-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                <Sparkles className="h-12 w-12 text-primary relative z-10" />
                            </div>
                            <div className="max-w-md text-center">
                                <h2 className="text-3xl font-extrabold text-foreground mb-3 tracking-tight font-headline">How can I help you today?</h2>
                                <p className="text-muted-foreground leading-relaxed text-[15px] font-medium opacity-80 decoration-primary/30">
                                    Consult with the Legal Assistant AI to analyze case files, interpret statutes, and receive automated, document-backed insights to support your research.
                                </p>
                            </div>
                        </div>
                    ) : (
                        <div className="flex flex-col w-full space-y-2">
                            {messages.map((msg) => (
                                <ChatMessage key={msg.id} message={msg} />
                            ))}

                            {isLoading && (
                                <div className="w-full flex justify-start px-4 py-8 animate-in fade-in slide-in-from-left-2 duration-500">
                                    <div className="flex max-w-3xl gap-4 md:gap-5 items-center bg-card/60 backdrop-blur-md rounded-2xl px-5 py-3 border border-border/50 shadow-xl relative overflow-hidden group">
                                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/5 to-transparent -translate-x-full animate-[shimmer_2s_infinite] pointer-events-none"></div>
                                        <div className="relative">
                                            <div className="h-8 w-8 rounded-xl bg-primary/10 flex items-center justify-center border border-primary/20 shadow-inner">
                                                <Sparkles className="h-4 w-4 text-primary animate-pulse" />
                                            </div>
                                            <div className="absolute -top-1 -right-1 flex h-3 w-3">
                                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                                                <span className="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
                                            </div>
                                        </div>
                                        <div className="flex flex-col gap-0.5">
                                            <div className="flex items-center gap-1.5 h-5 px-1">
                                                <span className="text-[11px] font-bold text-foreground/80 uppercase tracking-[0.15em] animate-pulse">
                                                    Thinking
                                                </span>
                                                <span className="flex gap-1 h-3 items-end pb-1">
                                                    <span className="w-1 h-1 rounded-full bg-primary/60 animate-bounce [animation-delay:-0.3s]"></span>
                                                    <span className="w-1 h-1 rounded-full bg-primary/60 animate-bounce [animation-delay:-0.15s]"></span>
                                                    <span className="w-1 h-1 rounded-full bg-primary/60 animate-bounce"></span>
                                                </span>
                                            </div>
                                            <div className="text-[10px] font-bold text-muted-foreground/60 uppercase tracking-widest pl-1">
                                                Consulting specialized legal records
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            <div ref={messagesEndRef} />
                        </div>
                    )}
                </div>
            </ScrollArea>

            {/* Input Area Overlay */}
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-background via-background/90 to-transparent pt-10 pb-4 px-4 z-20 pointer-events-none">
                <div className="max-w-3xl mx-auto w-full pointer-events-auto">
                    <ChatInput onSend={handleSend} isLoading={isLoading} />
                    <div className="flex items-center justify-center gap-2 text-[9px] text-muted-foreground font-bold uppercase tracking-[0.2em] mt-2.5 opacity-40">
                        <ShieldCheck className="w-2.5 h-2.5" /> Secure Legal Consultation v1.0
                    </div>
                </div>
            </div>
        </div>
    );
}
