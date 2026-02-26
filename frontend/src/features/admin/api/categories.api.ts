import { apiClient } from "./api.client";
import { API_ENDPOINTS } from "./api.constants";
import type {
    CategoryRead,
    CategoryCreate,
    CategoryUpdate,
    ListCategoriesParams,
} from "../types/admin.types";

export const categoriesApi = {
    /** Return all categories. Pass `include_inactive: true` to include disabled ones. */
    list(params?: ListCategoriesParams): Promise<CategoryRead[]> {
        return apiClient.get<CategoryRead[]>(API_ENDPOINTS.categories.list, {
            include_inactive: params?.include_inactive,
        });
    },

    /** Retrieve a single category by id. */
    get(id: string): Promise<CategoryRead> {
        return apiClient.get<CategoryRead>(API_ENDPOINTS.categories.get(id));
    },

    /** Create a new category. */
    create(data: CategoryCreate): Promise<CategoryRead> {
        return apiClient.post<CategoryRead>(API_ENDPOINTS.categories.create, data);
    },

    /** Update an existing category. All fields are optional. */
    update(id: string, data: CategoryUpdate): Promise<CategoryRead> {
        return apiClient.put<CategoryRead>(API_ENDPOINTS.categories.update(id), data);
    },

    /** Soft-delete a category and all its documents. */
    delete(id: string): Promise<void> {
        return apiClient.delete<void>(API_ENDPOINTS.categories.delete(id));
    },
};
