import { API_BASE_URL } from "./api.constants";
import type { ApiError } from "../types/admin.types";

// ─── Internal helpers ──────────────────────────────────────────────────────

async function parseError(res: Response): Promise<ApiError> {
    let detail;
    try {
        const body = await res.json();
        detail = body?.detail;
    } catch {
        // response body was not JSON
    }
    return {
        status: res.status,
        message: `Request failed with status ${res.status}: ${res.statusText}`,
        detail,
    };
}

function buildUrl(path: string, params?: Record<string, string | boolean | undefined>): string {
    const url = new URL(`${API_BASE_URL}${path}`);
    if (params) {
        Object.entries(params).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                url.searchParams.set(key, String(value));
            }
        });
    }
    return url.toString();
}

// ─── Generic request handler ───────────────────────────────────────────────

async function request<T>(
    path: string,
    options: RequestInit & { params?: Record<string, string | boolean | undefined> } = {}
): Promise<T> {
    const { params, ...fetchOptions } = options;
    const url = buildUrl(path, params);

    const res = await fetch(url, {
        ...fetchOptions,
        headers: {
            ...(fetchOptions.body instanceof FormData
                ? {}
                : { "Content-Type": "application/json" }),
            ...fetchOptions.headers,
        },
    });

    // 204 No Content — return undefined cast as T
    if (res.status === 204) {
        return undefined as T;
    }

    if (!res.ok) {
        throw await parseError(res);
    }

    return res.json() as Promise<T>;
}

// ─── Public API client ─────────────────────────────────────────────────────

export const apiClient = {
    get<T>(path: string, params?: Record<string, string | boolean | undefined>): Promise<T> {
        return request<T>(path, { method: "GET", params });
    },

    post<T>(path: string, body: unknown): Promise<T> {
        return request<T>(path, {
            method: "POST",
            body: body instanceof FormData ? body : JSON.stringify(body),
        });
    },

    put<T>(path: string, body: unknown): Promise<T> {
        return request<T>(path, {
            method: "PUT",
            body: body instanceof FormData ? body : JSON.stringify(body),
        });
    },

    delete<T = void>(path: string): Promise<T> {
        return request<T>(path, { method: "DELETE" });
    },
};
