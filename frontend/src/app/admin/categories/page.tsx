"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Plus, Pencil, Trash2, AlertCircle } from "lucide-react";
import { useCategories, useCategoryMutations } from "@/features/admin/hooks/useCategories";
import CategoryFormModal from "@/features/admin/components/CategoryFormModal";
import DeleteConfirmDialog from "@/features/admin/components/DeleteConfirmDialog";
import type { CategoryRead, CategoryCreate, CategoryUpdate } from "@/features/admin/types/admin.types";

export default function CategoriesPage() {
    const { categories, isLoading, error, refetch } = useCategories({ include_inactive: true });
    const { createCategory, updateCategory, deleteCategory, isMutating } =
        useCategoryMutations(refetch);

    // Form modal state
    const [formOpen, setFormOpen] = useState(false);
    const [editTarget, setEditTarget] = useState<CategoryRead | null>(null);

    // Delete dialog state
    const [deleteTarget, setDeleteTarget] = useState<CategoryRead | null>(null);
    const [isDeleting, setIsDeleting] = useState(false);

    function openCreate() {
        setEditTarget(null);
        setFormOpen(true);
    }

    function openEdit(cat: CategoryRead) {
        setEditTarget(cat);
        setFormOpen(true);
    }

    async function handleFormSubmit(data: CategoryCreate | CategoryUpdate) {
        if (editTarget) {
            await updateCategory(editTarget.id, data as CategoryUpdate);
        } else {
            await createCategory(data as CategoryCreate);
        }
        setFormOpen(false);
    }

    async function handleDelete() {
        if (!deleteTarget) return;
        setIsDeleting(true);
        try {
            await deleteCategory(deleteTarget.id);
            setDeleteTarget(null);
        } finally {
            setIsDeleting(false);
        }
    }

    return (
        <div className="flex flex-col gap-7 w-full">
            {/* Header */}
            <div className="flex items-start justify-between">
                <div>
                    <h1 className="text-[1.75rem] font-bold font-[family-name:var(--font-display)] text-[var(--foreground)]">
                        Categories
                    </h1>
                    <p className="text-sm text-[var(--muted-foreground)] mt-0.5">
                        Manage and organise legal document categories.
                    </p>
                </div>
                <Button className="gap-2 cursor-pointer" onClick={openCreate}>
                    <Plus size={15} /> Add Category
                </Button>
            </div>

            {/* Error */}
            {error && (
                <div className="flex items-center gap-2 text-sm text-red-400 bg-red-400/10 border border-red-400/20 rounded-lg px-4 py-3">
                    <AlertCircle size={16} />
                    <span>{error}</span>
                </div>
            )}

            {/* Table */}
            <Card className="bg-[var(--card)] border-[var(--glass-border)]">
                <CardHeader>
                    <CardTitle className="text-base font-semibold text-[var(--foreground)]">
                        All Categories
                        {!isLoading && (
                            <span className="ml-2 text-xs font-normal text-[var(--muted-foreground)]">
                                ({categories.length})
                            </span>
                        )}
                    </CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                    {isLoading ? (
                        <div className="p-4 flex flex-col gap-3">
                            {Array.from({ length: 4 }).map((_, i) => (
                                <Skeleton key={i} className="h-10 w-full" />
                            ))}
                        </div>
                    ) : categories.length === 0 ? (
                        <p className="text-center text-[var(--muted-foreground)] text-sm py-10">
                            No categories yet. Click &ldquo;Add Category&rdquo; to create one.
                        </p>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow className="border-[var(--glass-border)] hover:bg-transparent">
                                    <TableHead className="text-[var(--muted-foreground)]">Name</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Description</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Status</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Created</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {categories.map((cat) => (
                                    <TableRow
                                        key={cat.id}
                                        className="border-[var(--glass-border)] hover:bg-white/[0.03]"
                                    >
                                        <TableCell className="font-medium text-[var(--foreground)]">
                                            {cat.title}
                                        </TableCell>
                                        <TableCell className="text-[var(--muted-foreground)] max-w-xs truncate">
                                            {cat.description ?? <span className="italic opacity-50">—</span>}
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant={cat.is_active ? "default" : "secondary"}>
                                                {cat.is_active ? "Active" : "Inactive"}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-[var(--muted-foreground)]">
                                            {new Date(cat.created_at).toLocaleDateString()}
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex gap-2">
                                                <Button
                                                    size="sm"
                                                    variant="ghost"
                                                    onClick={() => openEdit(cat)}
                                                    className="text-[var(--primary)] hover:bg-blue-500/10 cursor-pointer"
                                                >
                                                    <Pencil size={14} />
                                                </Button>
                                                <Button
                                                    size="sm"
                                                    variant="ghost"
                                                    onClick={() => setDeleteTarget(cat)}
                                                    className="text-red-400 hover:bg-red-500/10 cursor-pointer"
                                                >
                                                    <Trash2 size={14} />
                                                </Button>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>

            {/* Modals */}
            <CategoryFormModal
                open={formOpen}
                onOpenChange={setFormOpen}
                category={editTarget}
                onSubmit={handleFormSubmit}
                isSubmitting={isMutating}
            />
            <DeleteConfirmDialog
                open={!!deleteTarget}
                onOpenChange={(open) => !open && setDeleteTarget(null)}
                itemName={deleteTarget?.title ?? ""}
                onConfirm={handleDelete}
                isDeleting={isDeleting}
            />
        </div>
    );
}
