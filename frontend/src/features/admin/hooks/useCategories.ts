"use client";

import { useState, useEffect, useCallback } from "react";
import { categoriesApi } from "../api/categories.api";
import type {
    CategoryRead,
    CategoryCreate,
    CategoryUpdate,
    ListCategoriesParams,
} from "../types/admin.types";

// ─── useCategories ─────────────────────────────────────────────────────────

interface UseCategoriesReturn {
    categories: CategoryRead[];
    isLoading: boolean;
    error: string | null;
    refetch: () => void;
}

export function useCategories(params?: ListCategoriesParams): UseCategoriesReturn {
    const [categories, setCategories] = useState<CategoryRead[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchCategories = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            const data = await categoriesApi.list(params);
            setCategories(data);
        } catch (err: unknown) {
            const msg = err instanceof Error ? err.message : "Failed to load categories";
            setError(msg);
        } finally {
            setIsLoading(false);
        }
    }, [params?.include_inactive]); // eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        fetchCategories();
    }, [fetchCategories]);

    return { categories, isLoading, error, refetch: fetchCategories };
}

// ─── useCategoryMutations ──────────────────────────────────────────────────

interface UseCategoryMutationsReturn {
    createCategory: (data: CategoryCreate) => Promise<CategoryRead>;
    updateCategory: (id: string, data: CategoryUpdate) => Promise<CategoryRead>;
    deleteCategory: (id: string) => Promise<void>;
    isMutating: boolean;
    mutationError: string | null;
}

export function useCategoryMutations(onSuccess?: () => void): UseCategoryMutationsReturn {
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
                const msg = err instanceof Error ? err.message : "Operation failed";
                setMutationError(msg);
                throw err;
            } finally {
                setIsMutating(false);
            }
        },
        [onSuccess]
    );

    return {
        createCategory: (data) => run(() => categoriesApi.create(data)),
        updateCategory: (id, data) => run(() => categoriesApi.update(id, data)),
        deleteCategory: (id) => run(() => categoriesApi.delete(id)),
        isMutating,
        mutationError,
    };
}
