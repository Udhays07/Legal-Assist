import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { SendHorizontal } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
    onSend: (message: string) => void;
    isLoading: boolean;
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
    const [content, setContent] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    useEffect(() => {
        // Auto-resize textarea
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
            textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
        }
    }, [content]);

    const handleSend = () => {
        if (content.trim() && !isLoading) {
            onSend(content);
            setContent("");
            // Reset height
            if (textareaRef.current) {
                textareaRef.current.style.height = "auto";
            }
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="relative flex w-full items-end gap-2 bg-card/60 backdrop-blur-xl border border-border shadow-xl rounded-xl p-1.5 px-3 focus-within:ring-2 focus-within:ring-primary/20 focus-within:border-primary/30 transition-all duration-300 group">
            <textarea
                ref={textareaRef}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Enter your legal inquiry here..."
                className="flex min-h-[36px] max-h-[150px] w-full bg-transparent px-1.5 py-1.5 text-sm text-foreground dark:text-white placeholder:text-muted-foreground/60 dark:placeholder:text-muted-foreground/80 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 resize-none overflow-y-auto leading-relaxed"
                disabled={isLoading}
                rows={1}
            />
            <div className="flex h-[44px] shrink-0 items-center">
                <Button
                    onClick={handleSend}
                    disabled={!content.trim() || isLoading}
                    size="icon"
                    className={cn(
                        "h-8 w-8 rounded-xl transition-all duration-300 shadow-md",
                        content.trim() 
                            ? "bg-primary text-primary-foreground hover:scale-105 active:scale-95 shadow-primary/20" 
                            : "bg-muted text-muted-foreground opacity-40 shadow-none"
                    )}
                >
                    <SendHorizontal className={cn("h-5 w-5 transition-transform", content.trim() && "group-hover:translate-x-0.5 group-hover:-translate-y-0.5")} />
                    <span className="sr-only">Send</span>
                </Button>
            </div>
        </div>
    );
}
