import { useState, useCallback } from "react";
import { chatApi } from "../api/chat.api";
import { Message } from "../types/chat.types";

export function useChat(userId: string) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [conversationId, setConversationId] = useState<string | undefined>();
    const [isLoading, setIsLoading] = useState(false);

    const sendMessage = useCallback(async (content: string, categoryId?: string) => {
        if (!content.trim()) return;

        // Add user message immediately for optimistic UI
        const userMessage: Message = {
            id: crypto.randomUUID(),
            role: "user",
            content,
            created_at: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);

        try {
            const response = await chatApi.query({
                query: content,
                user_id: userId,
                conversation_id: conversationId,
                category_id: categoryId,
            });

            // If this is the first message, save the new conversation ID
            if (!conversationId && response.conversation_id) {
                setConversationId(response.conversation_id);
            }

            // Add assistant message
            const assistantMessage: Message = {
                id: response.message_id || crypto.randomUUID(),
                role: "assistant",
                content: response.answer,
                created_at: new Date().toISOString(),
                sources: response.sources,
            };

            setMessages((prev) => [...prev, assistantMessage]);
        } catch (err: unknown) {
            console.error("Chat error:", err);

            const errorMessage: Message = {
                id: crypto.randomUUID(),
                role: "assistant",
                content: "Unexpected error, try after sometime",
                created_at: new Date().toISOString(),
            };

            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    }, [userId, conversationId]);

    const loadConversation = useCallback(async (id: string) => {
        setIsLoading(true);
        try {
            const data = await chatApi.getConversation(id, userId);
            setConversationId(data.conversation_id);

            const formattedMessages = data.messages.map((m: any) => ({
                id: m.id || crypto.randomUUID(),
                role: m.role || (m.is_user ? "user" : "assistant"),
                content: m.content || m.text,
                created_at: m.created_at || new Date().toISOString(),
                sources: m.sources,
            }));

            setMessages(formattedMessages);
        } catch (err: unknown) {
            console.error("Failed to load conversation:", err);
        } finally {
            setIsLoading(false);
        }
    }, [userId]);

    const clearChat = useCallback(() => {
        setMessages([]);
        setConversationId(undefined);
    }, []);

    return {
        messages,
        conversationId,
        isLoading,
        sendMessage,
        loadConversation,
        clearChat,
    };
}
