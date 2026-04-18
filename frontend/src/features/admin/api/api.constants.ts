/**
 * Base URL for the backend API.
 * Set NEXT_PUBLIC_API_URL in your .env.local file.
 * Defaults to http://localhost:8000 for local development.
 */
export const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

/**
 * All API endpoint paths, grouped by resource.
 * Use these constants throughout the API modules — never hardcode strings.
 */
export const API_ENDPOINTS = {
    health: "/health",
    auth: {
        login: "/auth/login",
        register: "/auth/register",
        me: "/auth/me",
    },

    categories: {
        list: "/categories/",
        create: "/categories/",
        get: (id: string) => `/categories/${id}`,
        update: (id: string) => `/categories/${id}`,
        delete: (id: string) => `/categories/${id}`,
    },

    documents: {
        list: "/documents/",
        create: "/documents/",
        get: (id: string) => `/documents/${id}`,
        update: (id: string) => `/documents/${id}`,
        delete: (id: string) => `/documents/${id}`,
    },
} as const;
