// ─── Category Types ────────────────────────────────────────────────────────

export interface CategoryRead {
    id: string;
    title: string;
    description: string | null;
    is_active: boolean | null;
    created_at: string;
    updated_at: string | null;
    deleted_at: string | null;
}

export interface CategoryCreate {
    title: string;
    description?: string | null;
    is_active?: boolean | null;
}

export interface CategoryUpdate {
    title?: string | null;
    description?: string | null;
    is_active?: boolean | null;
}

// ─── Document Types ────────────────────────────────────────────────────────

export type DocumentStatus = "published" | "draft" | "review" | string;

export interface DocumentRead {
    id: string;
    category_id: string;
    title: string;
    content: string;
    tags: string[] | null;
    metadata: Record<string, unknown> | null;
    status: DocumentStatus | null;
    created_by: string | null;
    created_at: string;
    updated_at: string | null;
    deleted_at: string | null;
}

export interface DocumentCreate {
    category_id: string;
    title: string;
    content?: string | null;
    file?: File;
    tags?: string[] | null;
    metadata?: Record<string, unknown> | null;
    status?: DocumentStatus | null;
    created_by?: string | null;
}

export interface DocumentUpdate {
    title?: string | null;
    content?: string | null;
    tags?: string[] | null;
    metadata?: Record<string, unknown> | null;
    status?: DocumentStatus | null;
}

// ─── Error Types ───────────────────────────────────────────────────────────

export interface ValidationErrorDetail {
    loc: (string | number)[];
    msg: string;
    type: string;
}

export interface ApiError {
    status: number;
    message: string;
    detail?: ValidationErrorDetail[];
}

// ─── Filter Types ──────────────────────────────────────────────────────────

export interface DocumentFilters {
    category_id?: string;
    status?: DocumentStatus;
}

export interface ListCategoriesParams {
    include_inactive?: boolean;
}