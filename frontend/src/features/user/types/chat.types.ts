import { z } from "zod";

export interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    created_at: string;
    sources?: Source[];
    rating?: number;
    feedback?: string;
}

export interface Source {
    title: string;
    content: string;
    similarity: number;
}

export interface Conversation {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
    messages: Message[];
}

export interface RAGQueryRequest {
    query: string;
    user_id: string;
    conversation_id?: string;
    top_k?: number;
    min_similarity?: number;
    category_id?: string;
    include_sources?: boolean;
}

export interface RAGQueryResponse {
    answer: string;
    sources?: any[];
    conversation_id: string;
    message_id: string;
    processing_time_ms: number;
    model_used: string;
}
