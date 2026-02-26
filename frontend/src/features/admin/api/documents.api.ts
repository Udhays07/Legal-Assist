import { apiClient } from "./api.client";
import { API_ENDPOINTS } from "./api.constants";
import type {
    DocumentRead,
    DocumentCreate,
    DocumentUpdate,
    DocumentFilters,
} from "../types/admin.types";

export const documentsApi = {
    /** List documents with optional category_id and status filters. */
    list(filters?: DocumentFilters): Promise<DocumentRead[]> {
        return apiClient.get<DocumentRead[]>(API_ENDPOINTS.documents.list, {
            category_id: filters?.category_id,
            status: filters?.status,
        });
    },

    /** Retrieve a single document by id. */
    get(id: string): Promise<DocumentRead> {
        return apiClient.get<DocumentRead>(API_ENDPOINTS.documents.get(id));
    },

    /** Create a new document. */
    create(data: FormData): Promise<DocumentRead> {
        return apiClient.post<DocumentRead>(API_ENDPOINTS.documents.create, data);
    },

    /** Partially update a document. All fields are optional. */
    update(id: string, data: DocumentUpdate): Promise<DocumentRead> {
        return apiClient.put<DocumentRead>(API_ENDPOINTS.documents.update(id), data);
    },

    /** Soft-delete a document. */
    delete(id: string): Promise<void> {
        return apiClient.delete<void>(API_ENDPOINTS.documents.delete(id));
    },
};
