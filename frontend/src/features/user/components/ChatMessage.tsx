import React from "react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Message } from "../types/chat.types";
import { cn } from "@/lib/utils";
import { User, Sparkles } from "lucide-react";

interface ChatMessageProps {
    message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
    const isUser = message.role === "user";

    return (
        <div
            className={cn(
                "group w-full text-foreground/90 flex justify-center px-4 py-8",
                !isUser && "bg-muted/40"
            )}
        >
            <div className="flex w-full max-w-3xl gap-4 md:gap-6">
                {/* Avatar */}
                <Avatar className={cn(
                    "h-8 w-8 shrink-0 rounded-md border shadow-sm",
                    isUser
                        ? "bg-background"
                        : "bg-primary text-primary-foreground border-primary"
                )}>
                    <AvatarFallback className={cn(
                        "rounded-md",
                        isUser ? "bg-background" : "bg-primary text-primary-foreground"
                    )}>
                        {isUser ? <User className="h-5 w-5 opacity-70" /> : <Sparkles className="h-4 w-4" />}
                    </AvatarFallback>
                </Avatar>

                {/* Message Content */}
                <div className="flex-1 space-y-2 overflow-hidden">
                    <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none break-words leading-relaxed text-foreground">
                        <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>

                    {/* Display sources if they exist and it's an assistant message */}
                    {!isUser && message.sources && message.sources.length > 0 && (
                        <div className="mt-4 flex flex-col gap-2 pt-2">
                            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1">
                                Sources
                            </span>
                            <div className="flex flex-wrap gap-2">
                                {message.sources.map((source, idx) => (
                                    <a
                                        key={idx}
                                        href="#"
                                        className="bg-background hover:bg-muted transition-colors rounded-lg border px-3 py-1.5 text-xs truncate max-w-[200px] shadow-sm flex items-center gap-1"
                                        title={source.title}
                                    >
                                        <span className="truncate">{source.title}</span>
                                    </a>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
