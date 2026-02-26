"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Upload, Pencil, Trash2, AlertCircle } from "lucide-react";
import { useDocuments, useDocumentMutations } from "@/features/admin/hooks/useDocuments";
import { useCategories } from "@/features/admin/hooks/useCategories";
import DocumentFormModal from "@/features/admin/components/DocumentFormModal";
import DeleteConfirmDialog from "@/features/admin/components/DeleteConfirmDialog";
import type {
    DocumentRead,
    DocumentCreate,
    DocumentUpdate,
    DocumentStatus,
} from "@/features/admin/types/admin.types";

const STATUS_VARIANT: Record<string, "default" | "secondary" | "outline"> = {
    published: "default",
    draft: "secondary",
    review: "outline",
};

const STATUS_FILTER_OPTIONS = [
    { label: "All Statuses", value: "all" },
    { label: "Published", value: "published" },
    { label: "Draft", value: "draft" },
    { label: "Review", value: "review" },
];

export default function DocumentsPage() {
    const [statusFilter, setStatusFilter] = useState<string>("all");
    const { categories } = useCategories();

    const { documents, isLoading, error, refetch } = useDocuments(
        statusFilter !== "all" ? { status: statusFilter as DocumentStatus } : undefined
    );
    const { createDocument, updateDocument, deleteDocument, isMutating, mutationError } =
        useDocumentMutations(refetch);

    // Form modal state
    const [formOpen, setFormOpen] = useState(false);
    const [editTarget, setEditTarget] = useState<DocumentRead | null>(null);

    // Delete dialog state
    const [deleteTarget, setDeleteTarget] = useState<DocumentRead | null>(null);
    const [isDeleting, setIsDeleting] = useState(false);

    function openCreate() {
        setEditTarget(null);
        setFormOpen(true);
    }

    function openEdit(doc: DocumentRead) {
        setEditTarget(doc);
        setFormOpen(true);
    }

    async function handleFormSubmit(data: DocumentUpdate | FormData) {
        try {
            if (editTarget) {
                await updateDocument(editTarget.id, data as DocumentUpdate);
            } else {
                await createDocument(data as FormData);
            }
            setFormOpen(false);
        } catch (err) {
            // Error is handled by the hook (mutationError), which we pass to the modal
        }
    }

    async function handleDelete() {
        if (!deleteTarget) return;
        setIsDeleting(true);
        try {
            await deleteDocument(deleteTarget.id);
            setDeleteTarget(null);
        } finally {
            setIsDeleting(false);
        }
    }

    const getCategoryTitle = (id: string) =>
        categories.find((c) => c.id === id)?.title ?? id;

    return (
        <div className="flex flex-col gap-7 w-full">
            {/* Header */}
            <div className="flex items-start justify-between gap-4">
                <div>
                    <h1 className="text-[1.75rem] font-bold font-[family-name:var(--font-display)] text-[var(--foreground)]">
                        Documents
                    </h1>
                    <p className="text-sm text-[var(--muted-foreground)] mt-0.5">
                        Manage legal documents in the knowledge base.
                    </p>
                </div>
                <Button className="gap-2 cursor-pointer shrink-0" onClick={openCreate}>
                    <Upload size={15} /> Add Document
                </Button>
            </div>

            {/* Error */}
            {error && (
                <div className="flex items-center gap-2 text-sm text-red-400 bg-red-400/10 border border-red-400/20 rounded-lg px-4 py-3">
                    <AlertCircle size={16} />
                    <span>{error}</span>
                </div>
            )}

            {/* Table Card */}
            <Card className="bg-[var(--card)] border-[var(--glass-border)]">
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="text-base font-semibold text-[var(--foreground)]">
                        All Documents
                        {!isLoading && (
                            <span className="ml-2 text-xs font-normal text-[var(--muted-foreground)]">
                                ({documents.length})
                            </span>
                        )}
                    </CardTitle>
                    {/* Status filter */}
                    <Select value={statusFilter} onValueChange={setStatusFilter}>
                        <SelectTrigger className="w-40 bg-[var(--input)] border-[var(--glass-border)] text-[var(--foreground)] text-sm h-8">
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent className="bg-[var(--card)] border-[var(--glass-border)] text-[var(--foreground)]">
                            {STATUS_FILTER_OPTIONS.map((opt) => (
                                <SelectItem key={opt.value} value={opt.value}>
                                    {opt.label}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </CardHeader>

                <CardContent className="p-0">
                    {isLoading ? (
                        <div className="p-4 flex flex-col gap-3">
                            {Array.from({ length: 5 }).map((_, i) => (
                                <Skeleton key={i} className="h-10 w-full" />
                            ))}
                        </div>
                    ) : documents.length === 0 ? (
                        <p className="text-center text-[var(--muted-foreground)] text-sm py-10">
                            No documents found. Click &ldquo;Add Document&rdquo; to create one.
                        </p>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow className="border-[var(--glass-border)] hover:bg-transparent">
                                    <TableHead className="text-[var(--muted-foreground)]">Title</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Category</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Tags</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Status</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Created</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {documents.map((doc) => (
                                    <TableRow
                                        key={doc.id}
                                        className="border-[var(--glass-border)] hover:bg-white/[0.03]"
                                    >
                                        <TableCell className="font-medium text-[var(--foreground)] max-w-[200px] truncate">
                                            {doc.title}
                                        </TableCell>
                                        <TableCell className="text-[var(--muted-foreground)]">
                                            {getCategoryTitle(doc.category_id)}
                                        </TableCell>
                                        <TableCell className="text-[var(--muted-foreground)]">
                                            {doc.tags?.length ? (
                                                <div className="flex flex-wrap gap-1">
                                                    {doc.tags.slice(0, 2).map((tag) => (
                                                        <span
                                                            key={tag}
                                                            className="text-[0.65rem] px-1.5 py-0.5 rounded bg-white/5 border border-white/10"
                                                        >
                                                            {tag}
                                                        </span>
                                                    ))}
                                                    {doc.tags.length > 2 && (
                                                        <span className="text-[0.65rem] text-[var(--muted-foreground)]">
                                                            +{doc.tags.length - 2}
                                                        </span>
                                                    )}
                                                </div>
                                            ) : (
                                                <span className="italic opacity-40">—</span>
                                            )}
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant={STATUS_VARIANT[doc.status as string] ?? "secondary"}>
                                                {doc.status ?? "—"}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-[var(--muted-foreground)]">
                                            {new Date(doc.created_at).toLocaleDateString()}
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex gap-2">
                                                <Button
                                                    size="sm"
                                                    variant="ghost"
                                                    onClick={() => openEdit(doc)}
                                                    className="text-[var(--primary)] hover:bg-blue-500/10 cursor-pointer"
                                                >
                                                    <Pencil size={14} />
                                                </Button>
                                                <Button
                                                    size="sm"
                                                    variant="ghost"
                                                    onClick={() => setDeleteTarget(doc)}
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
            <DocumentFormModal
                open={formOpen}
                onOpenChange={setFormOpen}
                document={editTarget}
                categories={categories}
                onSubmit={handleFormSubmit}
                isSubmitting={isMutating}
                error={mutationError}
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
