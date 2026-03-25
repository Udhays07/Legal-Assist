import { API_BASE_URL } from "@/features/admin/api/api.constants";
import { RAGQueryRequest, RAGQueryResponse, Conversation } from "../types/chat.types";

export const chatApi = {
    /**
     * Send a query to the RAG system to get an AI response
     */
    async query(request: RAGQueryRequest): Promise<RAGQueryResponse> {
        const response = await fetch(`${API_BASE_URL}/rag/query`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                ...request,
                // Set some default sensible values if not provided
                top_k: request.top_k ?? 5,
                min_similarity: request.min_similarity ?? 0.3,
                include_sources: request.include_sources ?? true,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || "Failed to process query");
        }

        return response.json();
    },

    /**
     * List conversations for a specific user
     */
    async listConversations(userId: string, limit: number = 20): Promise<{ conversations: Conversation[] }> {
        const response = await fetch(`${API_BASE_URL}/rag/conversations?user_id=${userId}&limit=${limit}`);

        if (!response.ok) {
            throw new Error("Failed to fetch conversations");
        }

        return response.json();
    },

    /**
     * Get full conversation history
     */
    async getConversation(conversationId: string, userId: string): Promise<{ conversation_id: string; messages: any[] }> {
        const response = await fetch(`${API_BASE_URL}/rag/conversations/${conversationId}?user_id=${userId}`);

        if (!response.ok) {
            throw new Error("Failed to fetch conversation history");
        }

        return response.json();
    }
};
