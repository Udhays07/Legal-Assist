"use client";

import { useState, useEffect, useRef } from "react";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from "@/components/ui/dialog";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { FileText, Upload, AlertCircle, X, File } from "lucide-react";
import type {
    DocumentRead,
    DocumentUpdate,
    CategoryRead,
} from "../types/admin.types";

interface DocumentFormModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    /** Pass an existing document to switch to edit mode */
    document?: DocumentRead | null;
    categories: CategoryRead[];
    onSubmit: (data: DocumentUpdate | FormData) => Promise<void>;
    isSubmitting: boolean;
    error?: string | null;
}

const STATUS_OPTIONS = ["published", "draft", "review"] as const;

export default function DocumentFormModal({
    open,
    onOpenChange,
    document,
    categories,
    onSubmit,
    isSubmitting,
    error: propError,
}: DocumentFormModalProps) {
    const isEditing = !!document;
    const fileInputRef = useRef<HTMLInputElement>(null);

    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [categoryId, setCategoryId] = useState("");
    const [status, setStatus] = useState<string>("published");
    const [tagsRaw, setTagsRaw] = useState(""); // comma-separated
    const [activeTab, setActiveTab] = useState<string>("text");
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    useEffect(() => {
        if (open) {
            if (document) {
                setTitle(document.title);
                setContent(document.content);
                setCategoryId(document.category_id);
                setStatus(document.status ?? "published");
                setTagsRaw(document.tags?.join(", ") ?? "");
                setActiveTab("text");
                setSelectedFile(null);
            } else {
                setTitle("");
                setContent("");
                setCategoryId(categories[0]?.id ?? "");
                setStatus("published");
                setTagsRaw("");
                setActiveTab("text");
                setSelectedFile(null);
            }
        }
    }, [document, open, categories]);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        const tags = tagsRaw
            .split(",")
            .map((t) => t.trim())
            .filter(Boolean);

        if (isEditing) {
            const payload: DocumentUpdate = {
                title: title.trim(),
                content: content.trim(),
                status,
                tags: tags.length ? tags : null,
            };
            await onSubmit(payload);
        } else {
            const formData = new FormData();
            formData.append('title', title.trim());
            formData.append('category_id', categoryId);
            formData.append('status', status);
            formData.append('tags', JSON.stringify(tags));

            if (activeTab === "file" && selectedFile) {
                formData.append('file', selectedFile);
            } else {
                formData.append('content', content.trim());
            }

            await onSubmit(formData);
        }
    }

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0]) {
            setSelectedFile(e.target.files[0]);
            // Auto-set title from filename if title is empty
            if (!title.trim()) {
                const nameWithoutExt = e.target.files[0].name.replace(/\.[^/.]+$/, "");
                setTitle(nameWithoutExt);
            }
        }
    };

    const clearFile = () => {
        setSelectedFile(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="bg-[var(--card)] border-[var(--glass-border)] text-[var(--foreground)] sm:max-w-2xl max-h-[90vh] flex flex-col">
                <DialogHeader>
                    <DialogTitle>{isEditing ? "Edit Document" : "Add Document"}</DialogTitle>
                </DialogHeader>

                {propError && (
                    <div className="flex items-center gap-2 text-sm text-red-400 bg-red-400/10 border border-red-400/20 rounded-lg px-4 py-3 mb-2">
                        <AlertCircle size={16} />
                        <span>{propError}</span>
                    </div>
                )}

                <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-2 overflow-y-auto pr-1">
                    {/* Title */}
                    <div className="flex flex-col gap-1.5">
                        <Label htmlFor="doc-title">Title <span className="text-red-400">*</span></Label>
                        <Input
                            id="doc-title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            placeholder="e.g. Contract Law Guidelines"
                            required
                            className="bg-[var(--input)] border-[var(--glass-border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)]"
                        />
                    </div>

                    {/* Category — only required when creating */}
                    {!isEditing && (
                        <div className="flex flex-col gap-1.5">
                            <Label htmlFor="doc-cat">Category <span className="text-red-400">*</span></Label>
                            <Select value={categoryId} onValueChange={setCategoryId} required>
                                <SelectTrigger
                                    id="doc-cat"
                                    className="bg-[var(--input)] border-[var(--glass-border)] text-[var(--foreground)]"
                                >
                                    <SelectValue placeholder="Select category" />
                                </SelectTrigger>
                                <SelectContent className="bg-[var(--card)] border-[var(--glass-border)] text-[var(--foreground)]">
                                    {categories.map((c) => (
                                        <SelectItem key={c.id} value={c.id}>
                                            {c.title}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                    )}

                    {/* Content Section */}
                    {isEditing ? (
                        <div className="flex flex-col gap-1.5">
                            <Label htmlFor="doc-content">Content <span className="text-red-400">*</span></Label>
                            <Textarea
                                id="doc-content"
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                placeholder="Document content…"
                                required
                                className="bg-[var(--input)] border-[var(--glass-border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] resize-none h-44 overflow-y-auto whitespace-pre-wrap break-words"
                            />
                        </div>
                    ) : (
                        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                            <TabsList className="grid w-full grid-cols-2 bg-[var(--input)] border border-[var(--glass-border)] h-9 p-1">
                                <TabsTrigger value="text" className="gap-2 text-xs">
                                    <FileText size={14} /> Type Content
                                </TabsTrigger>
                                <TabsTrigger value="file" className="gap-2 text-xs">
                                    <Upload size={14} /> Upload File
                                </TabsTrigger>
                            </TabsList>
                            <TabsContent value="text" className="mt-4">
                                <Textarea
                                    id="doc-content"
                                    value={content}
                                    onChange={(e) => setContent(e.target.value)}
                                    placeholder="Paste or type legal text here…"
                                    required={activeTab === "text"}
                                    className="bg-[var(--input)] border-[var(--glass-border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] resize-none h-44 overflow-y-auto whitespace-pre-wrap break-words"
                                />
                            </TabsContent>
                            <TabsContent value="file" className="mt-4">
                                <div
                                    className="border-2 border-dashed border-[var(--glass-border)] rounded-lg p-8 flex flex-col items-center justify-center gap-3 bg-[var(--input)] hover:border-[var(--primary)] transition-colors cursor-pointer relative"
                                    onClick={() => fileInputRef.current?.click()}
                                >
                                    <Input
                                        type="file"
                                        ref={fileInputRef}
                                        className="hidden"
                                        onChange={handleFileChange}
                                        accept=".pdf,.docx,.xlsx,.pptx,.txt,.md"
                                    />

                                    {selectedFile ? (
                                        <div className="flex flex-col items-center gap-2">
                                            <div className="bg-[var(--primary)]/10 p-3 rounded-full text-[var(--primary)]">
                                                <File size={24} />
                                            </div>
                                            <div className="text-center">
                                                <p className="text-sm font-medium truncate max-w-[200px]">{selectedFile.name}</p>
                                                <p className="text-xs text-[var(--muted-foreground)]">{(selectedFile.size / 1024).toFixed(1)} KB</p>
                                            </div>
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                className="text-red-400 hover:text-red-300 gap-1 h-7"
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    clearFile();
                                                }}
                                            >
                                                <X size={14} /> Change File
                                            </Button>
                                        </div>
                                    ) : (
                                        <>
                                            <div className="bg-[var(--foreground)]/5 p-3 rounded-full text-[var(--muted-foreground)]">
                                                <Upload size={24} />
                                            </div>
                                            <div className="text-center">
                                                <p className="text-sm font-medium">Click to upload document</p>
                                                <p className="text-xs text-[var(--muted-foreground)] mt-1">
                                                    PDF, Word, Excel, PPTX, TXT, MD
                                                </p>
                                            </div>
                                        </>
                                    )}
                                </div>
                            </TabsContent>
                        </Tabs>
                    )}

                    {/* Status & Tags row */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {/* Status */}
                        <div className="flex flex-col gap-1.5">
                            <Label htmlFor="doc-status">Status</Label>
                            <Select value={status} onValueChange={setStatus}>
                                <SelectTrigger
                                    id="doc-status"
                                    className="bg-[var(--input)] border-[var(--glass-border)] text-[var(--foreground)]"
                                >
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent className="bg-[var(--card)] border-[var(--glass-border)] text-[var(--foreground)]">
                                    {STATUS_OPTIONS.map((s) => (
                                        <SelectItem key={s} value={s} className="capitalize">
                                            {s.charAt(0).toUpperCase() + s.slice(1)}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        {/* Tags */}
                        <div className="flex flex-col gap-1.5">
                            <Label htmlFor="doc-tags">Tags <span className="text-[var(--muted-foreground)] text-xs font-normal">(comma-separated)</span></Label>
                            <Input
                                id="doc-tags"
                                value={tagsRaw}
                                onChange={(e) => setTagsRaw(e.target.value)}
                                placeholder="e.g. tort, liability, 2024"
                                className="bg-[var(--input)] border-[var(--glass-border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)]"
                            />
                        </div>
                    </div>

                    <DialogFooter className="mt-4">
                        <Button type="button" variant="ghost" onClick={() => onOpenChange(false)} disabled={isSubmitting}>
                            Cancel
                        </Button>
                        <Button
                            type="submit"
                            disabled={
                                isSubmitting ||
                                !title.trim() ||
                                (!isEditing && activeTab === "text" && !content.trim()) ||
                                (!isEditing && activeTab === "file" && !selectedFile) ||
                                (!isEditing && !categoryId) ||
                                (isEditing && !content.trim())
                            }
                            className="cursor-pointer min-w-[120px]"
                        >
                            {isSubmitting ? (
                                <span className="flex items-center gap-2">
                                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/20 border-t-white" />
                                    {activeTab === "file" ? "Extracting..." : "Saving..."}
                                </span>
                            ) : (
                                isEditing ? "Save Changes" : "Create Document"
                            )}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
