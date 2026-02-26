"use client";

import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface DeleteConfirmDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    /** The resource name to display in the message */
    itemName: string;
    /** Called when the user confirms deletion */
    onConfirm: () => Promise<void> | void;
    isDeleting?: boolean;
}

export default function DeleteConfirmDialog({
    open,
    onOpenChange,
    itemName,
    onConfirm,
    isDeleting,
}: DeleteConfirmDialogProps) {
    return (
        <AlertDialog open={open} onOpenChange={onOpenChange}>
            <AlertDialogContent className="bg-[var(--card)] border-[var(--glass-border)] text-[var(--foreground)]">
                <AlertDialogHeader>
                    <AlertDialogTitle>Delete &ldquo;{itemName}&rdquo;?</AlertDialogTitle>
                    <AlertDialogDescription className="text-[var(--muted-foreground)]">
                        This action cannot be undone. The record will be soft-deleted and removed from the
                        active list.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel
                        className="bg-transparent border-[var(--glass-border)] text-[var(--foreground)] hover:bg-white/5"
                        disabled={isDeleting}
                    >
                        Cancel
                    </AlertDialogCancel>
                    <AlertDialogAction
                        onClick={onConfirm}
                        disabled={isDeleting}
                        className="bg-red-600 hover:bg-red-700 text-white cursor-pointer"
                    >
                        {isDeleting ? "Deleting…" : "Delete"}
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    );
}
