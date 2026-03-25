import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { SendHorizontal } from "lucide-react";

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
        <div className="relative flex w-full items-end gap-2 bg-background border shadow-sm rounded-2xl p-2 px-3 focus-within:ring-1 focus-within:ring-primary/50 transition-shadow">
            <textarea
                ref={textareaRef}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Message Legal Assistant..."
                className="flex min-h-[44px] max-h-[200px] w-full bg-transparent px-3 py-3 text-sm placeholder:text-muted-foreground focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 resize-none overflow-y-auto"
                disabled={isLoading}
                rows={1}
            />
            <div className="flex h-[44px] shrink-0 items-center">
                <Button
                    onClick={handleSend}
                    disabled={!content.trim() || isLoading}
                    size="icon"
                    variant={content.trim() ? "default" : "secondary"}
                    className="h-8 w-8 rounded-full transition-all"
                >
                    <SendHorizontal className="h-4 w-4" />
                    <span className="sr-only">Send</span>
                </Button>
            </div>
        </div>
    );
}
