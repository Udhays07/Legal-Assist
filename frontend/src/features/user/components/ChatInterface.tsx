"use client";

import React, { useEffect, useRef, useState } from "react";
import { useChat } from "../hooks/useChat";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Loader2, Sparkles, FolderIcon } from "lucide-react";
import { categoriesApi } from "@/features/admin/api/categories.api";
import type { CategoryRead } from "@/features/admin/types/admin.types";

interface ChatInterfaceProps {
    userId?: string;
}

export function ChatInterface({ userId = "default-user" }: ChatInterfaceProps) {
    const { messages, isLoading, sendMessage } = useChat(userId);
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
        <div className="flex flex-col h-full overflow-hidden bg-background relative">
            {/* Header / Category Selector top bar */}
            <div className="flex h-14 shrink-0 items-center border-b px-4 justify-between bg-background/95 backdrop-blur z-10 w-full top-0">
                <div className="flex items-center gap-2">
                    <span className="font-semibold px-2 text-foreground flex items-center gap-2">
                        Legal Assistant AI
                    </span>
                    <div className="flex items-center gap-2 ml-4">
                        <FolderIcon className="w-4 h-4 text-muted-foreground" />
                        <select
                            value={selectedCategoryId}
                            onChange={(e) => setSelectedCategoryId(e.target.value)}
                            className="text-sm bg-transparent border-none outline-none focus:ring-0 text-muted-foreground hover:text-foreground cursor-pointer font-medium"
                        >
                            <option value="">All Categories</option>
                            {categories.map((cat) => (
                                <option key={cat.id} value={cat.id}>{cat.title}</option>
                            ))}
                        </select>
                    </div>
                </div>
            </div>

            {/* Chat Area */}
            <ScrollArea className="flex-1 w-full min-h-0">
                <div className="flex flex-col min-h-full pb-32">
                    {messages.length === 0 ? (
                        <div className="flex-1 flex flex-col items-center justify-center text-muted-foreground p-8 text-center gap-6 mt-32">
                            <div className="h-16 w-16 bg-muted rounded-2xl flex items-center justify-center shadow-sm border">
                                <Sparkles className="h-8 w-8 text-primary" />
                            </div>
                            <div>
                                <h2 className="text-2xl font-semibold text-foreground mb-2">How can I help you today?</h2>
                                <p className="text-sm">Ask anything about your legal documents or case files.</p>
                            </div>
                        </div>
                    ) : (
                        <div className="flex flex-col w-full">
                            {messages.map((msg) => (
                                <ChatMessage key={msg.id} message={msg} />
                            ))}

                            {isLoading && (
                                <div className="w-full flex justify-center px-4 py-8 bg-muted/40">
                                    <div className="flex w-full max-w-3xl gap-4 md:gap-6">
                                        <div className="h-8 w-8 shrink-0 rounded-md bg-primary text-primary-foreground flex items-center justify-center border border-primary shadow-sm">
                                            <Sparkles className="h-4 w-4" />
                                        </div>
                                        <div className="flex items-center text-sm text-muted-foreground font-medium">
                                            <Loader2 className="h-4 w-4 animate-spin mr-2" />
                                            Analyzing documents...
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
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-background via-background to-transparent pt-10 pb-6 px-4">
                <div className="max-w-3xl mx-auto w-full">
                    <ChatInput onSend={handleSend} isLoading={isLoading} />
                    <div className="text-center text-xs text-muted-foreground mt-3">
                        AI can make mistakes. Consider verifying important legal information.
                    </div>
                </div>
            </div>
        </div>
    );
}
