"use client";

import { useState, useEffect } from "react";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import type { CategoryRead, CategoryCreate, CategoryUpdate } from "../types/admin.types";

interface CategoryFormModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    /** Pass an existing category to switch to edit mode */
    category?: CategoryRead | null;
    onSubmit: (data: CategoryCreate | CategoryUpdate) => Promise<void>;
    isSubmitting: boolean;
}

export default function CategoryFormModal({
    open,
    onOpenChange,
    category,
    onSubmit,
    isSubmitting,
}: CategoryFormModalProps) {
    const isEditing = !!category;

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [isActive, setIsActive] = useState(true);

    // Sync form state when the target category changes
    useEffect(() => {
        if (category) {
            setTitle(category.title);
            setDescription(category.description ?? "");
            setIsActive(category.is_active ?? true);
        } else {
            setTitle("");
            setDescription("");
            setIsActive(true);
        }
    }, [category, open]);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        const payload: CategoryCreate | CategoryUpdate = {
            title: title.trim(),
            description: description.trim() || null,
            is_active: isActive,
        };
        await onSubmit(payload);
    }

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="bg-[var(--card)] border-[var(--glass-border)] text-[var(--foreground)] sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>{isEditing ? "Edit Category" : "Add Category"}</DialogTitle>
                </DialogHeader>

                <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-2">
                    {/* Title */}
                    <div className="flex flex-col gap-1.5">
                        <Label htmlFor="cat-title">Title <span className="text-red-400">*</span></Label>
                        <Input
                            id="cat-title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            placeholder="e.g. Contract Law"
                            required
                            className="bg-[var(--input)] border-[var(--glass-border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)]"
                        />
                    </div>

                    {/* Description */}
                    <div className="flex flex-col gap-1.5">
                        <Label htmlFor="cat-desc">Description</Label>
                        <Textarea
                            id="cat-desc"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Optional description…"
                            rows={3}
                            className="bg-[var(--input)] border-[var(--glass-border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] resize-none"
                        />
                    </div>

                    {/* Active toggle */}
                    <div className="flex items-center gap-2">
                        <input
                            id="cat-active"
                            type="checkbox"
                            checked={isActive}
                            onChange={(e) => setIsActive(e.target.checked)}
                            className="accent-[var(--primary)]"
                        />
                        <Label htmlFor="cat-active" className="cursor-pointer">Active</Label>
                    </div>

                    <DialogFooter className="mt-2">
                        <Button type="button" variant="ghost" onClick={() => onOpenChange(false)} disabled={isSubmitting}>
                            Cancel
                        </Button>
                        <Button type="submit" disabled={isSubmitting || !title.trim()} className="cursor-pointer">
                            {isSubmitting ? "Saving…" : isEditing ? "Save Changes" : "Create Category"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
