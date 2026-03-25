import React from "react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Message } from "../types/chat.types";
import { cn } from "@/lib/utils";
import { User, Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatMessageProps {
    message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
    const isUser = message.role === "user";

    return (
        <div
            className={cn(
                "w-full flex px-2 py-4 animate-in fade-in slide-in-from-bottom-2 duration-300",
                isUser ? "justify-end" : "justify-start"
            )}
        >
            <div className={cn(
                "flex max-w-[92%] md:max-w-[90%] gap-2 md:gap-3",
                isUser ? "flex-row-reverse" : "flex-row"
            )}>
                {/* Avatar */}
                <Avatar className={cn(
                    "h-8 w-8 shrink-0 rounded-xl border shadow-sm mt-0.5",
                    isUser
                        ? "bg-muted border-border"
                        : "bg-primary text-primary-foreground border-primary shadow-primary/20"
                )}>
                    <AvatarFallback className="rounded-xl">
                        {isUser ? <User className="h-4 w-4 opacity-70" /> : <Sparkles className="h-4 w-4" />}
                    </AvatarFallback>
                </Avatar>

                {/* Message Content */}
                <div className={cn(
                    "flex flex-col gap-1.5",
                    isUser ? "items-end text-right" : "items-start"
                )}>
                    <div className={cn(
                        "rounded-2xl px-4 py-2.5 shadow-sm border leading-relaxed break-words",
                        isUser 
                            ? "bg-gradient-to-br from-primary to-blue-600 text-primary-foreground border-primary/20 rounded-tr-none shadow-md" 
                            : "bg-card/90 dark:bg-card/95 backdrop-blur-md text-foreground border-border/50 rounded-tl-none shadow-xl shadow-black/5"
                    )}>
                        <div className={cn(
                            "prose prose-sm dark:prose-invert max-w-none break-words text-[13.5px]",
                            isUser ? "text-primary-foreground font-medium" : "text-foreground dark:text-white"
                        )}>
                            {isUser ? (
                                <p className="whitespace-pre-wrap">{message.content}</p>
                            ) : (
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                    {message.content}
                                </ReactMarkdown>
                            )}
                        </div>
                    </div>

                    {/* Display sources if they exist and it's an assistant message */}
                    {!isUser && message.sources && message.sources.length > 0 && (
                        <div className="mt-3 flex flex-col gap-2 pt-1">
                            <span className="text-[10px] font-bold text-muted-foreground dark:text-muted-foreground/90 uppercase tracking-[0.1em] ml-1">
                                References & Legal Sources
                            </span>
                            <div className="flex flex-wrap gap-2">
                                {message.sources.map((source, idx) => (
                                    <a
                                        key={idx}
                                        href="#"
                                        className="bg-card hover:bg-muted/80 backdrop-blur-sm transition-all rounded-full border border-border/50 px-4 py-1.5 text-[11px] font-medium truncate max-w-[200px] shadow-sm flex items-center gap-2 group text-foreground dark:text-white"
                                        title={source.title}
                                    >
                                        <div className="w-1.5 h-1.5 rounded-full bg-primary/60 group-hover:bg-primary transition-colors"></div>
                                        <span className="truncate opacity-90 group-hover:opacity-100">{source.title}</span>
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
