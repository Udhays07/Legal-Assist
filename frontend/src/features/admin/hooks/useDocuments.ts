"use client";

import { useState, useEffect, useCallback } from "react";
import { documentsApi } from "../api/documents.api";
import type {
    DocumentRead,
    DocumentCreate,
    DocumentUpdate,
    DocumentFilters,
} from "../types/admin.types";

// ─── useDocuments ──────────────────────────────────────────────────────────

interface UseDocumentsReturn {
    documents: DocumentRead[];
    isLoading: boolean;
    error: string | null;
    refetch: () => void;
}

export function useDocuments(filters?: DocumentFilters): UseDocumentsReturn {
    const [documents, setDocuments] = useState<DocumentRead[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchDocuments = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            const data = await documentsApi.list(filters);
            setDocuments(data);
        } catch (err: unknown) {
            const msg = err instanceof Error ? err.message : "Failed to load documents";
            setError(msg);
        } finally {
            setIsLoading(false);
        }
    }, [filters?.category_id, filters?.status]); // eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        fetchDocuments();
    }, [fetchDocuments]);

    return { documents, isLoading, error, refetch: fetchDocuments };
}

// ─── useDocumentMutations ──────────────────────────────────────────────────

interface UseDocumentMutationsReturn {
    createDocument: (data: FormData) => Promise<DocumentRead>;
    updateDocument: (id: string, data: DocumentUpdate) => Promise<DocumentRead>;
    deleteDocument: (id: string) => Promise<void>;
    isMutating: boolean;
    mutationError: string | null;
}

export function useDocumentMutations(onSuccess?: () => void): UseDocumentMutationsReturn {
    const [isMutating, setIsMutating] = useState(false);
    const [mutationError, setMutationError] = useState<string | null>(null);

    const run = useCallback(
        async <T>(fn: () => Promise<T>): Promise<T> => {
            setIsMutating(true);
            setMutationError(null);
            try {
                const result = await fn();
                onSuccess?.();
                return result;
            } catch (err: unknown) {
                // If it's a structured ApiError (like 422), use its message directly
                const msg = (err as any).message || (err instanceof Error ? err.message : "Operation failed");
                setMutationError(msg);
                throw err;
            } finally {
                setIsMutating(false);
            }
        },
        [onSuccess]
    );

    return {
        createDocument: (data: FormData) => run(() => documentsApi.create(data)),
        updateDocument: (id, data) => run(() => documentsApi.update(id, data)),
        deleteDocument: (id) => run(() => documentsApi.delete(id)),
        isMutating,
        mutationError,
    };
}
