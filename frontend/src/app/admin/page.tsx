"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { FileText, Tag, Users, BrainCircuit } from "lucide-react";
import { useCategories } from "@/features/admin/hooks/useCategories";
import { useDocuments } from "@/features/admin/hooks/useDocuments";
import type { DocumentStatus } from "@/features/admin/types/admin.types";
import { ThemeToggle } from "@/components/ThemeToggle";

const STATUS_VARIANT: Record<string, "default" | "secondary" | "outline"> = {
    published: "default",
    draft: "secondary",
    review: "outline",
};

function StatCardSkeleton() {
    return (
        <Card className="bg-card border-border">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                <Skeleton className="h-3 w-24" />
                <Skeleton className="h-4 w-4 rounded" />
            </CardHeader>
            <CardContent>
                <Skeleton className="h-8 w-16 mb-1" />
                <Skeleton className="h-3 w-28" />
            </CardContent>
        </Card>
    );
}

export default function AdminDashboard() {
    const { categories, isLoading: catsLoading } = useCategories();
    const { documents, isLoading: docsLoading } = useDocuments();

    const isLoading = catsLoading || docsLoading;

    const stats = [
        { label: "Total Documents", value: documents.length, change: "Live from API", icon: FileText },
        { label: "Categories", value: categories.length, change: "Live from API", icon: Tag },
        { label: "Published Docs", value: documents.filter((d) => d.status === "published").length, change: "Active in KB", icon: Users },
        { label: "Draft Docs", value: documents.filter((d) => d.status === "draft").length, change: "Pending review", icon: BrainCircuit },
    ];

    const recentDocuments = [...documents]
        .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .slice(0, 5);

    const getCategoryTitle = (id: string) =>
        categories.find((c) => c.id === id)?.title ?? id;

    return (
        <div className="flex flex-col gap-7 w-full relative">
            <div className="absolute top-0 right-0 z-50">
                <ThemeToggle />
            </div>
            <div>
                <h1 className="text-[1.75rem] font-bold font-[family-name:var(--font-display)] text-[var(--foreground)]">
                    Digital Know Your Rights Framework
                </h1>
                <p className="text-sm text-[var(--muted-foreground)] mt-0.5">
                    A framework for Know Your Rights Database creation and empowering the community.
                </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {isLoading
                    ? Array.from({ length: 4 }).map((_, i) => <StatCardSkeleton key={i} />)
                    : stats.map(({ label, value, change, icon: Icon }) => (
                        <Card
                            key={label}
                            className="bg-card border-border hover:border-white/20 transition-colors"
                        >
                            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                                <CardTitle className="text-xs font-semibold uppercase tracking-widest text-[var(--muted-foreground)]">
                                    {label}
                                </CardTitle>
                                <Icon size={16} className="text-[var(--muted-foreground)]" />
                            </CardHeader>
                            <CardContent>
                                <p className="text-3xl font-bold font-[family-name:var(--font-display)] text-[var(--foreground)]">
                                    {value}
                                </p>
                                <p className="text-xs mt-1 text-[var(--muted-foreground)]">{change}</p>
                            </CardContent>
                        </Card>
                    ))}
            </div>

            {/* Recent Documents */}
            <Card className="bg-card border-border">
                <CardHeader>
                    <CardTitle className="text-base font-semibold text-[var(--foreground)]">
                        Recent Documents
                    </CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                    {docsLoading ? (
                        <div className="p-4 flex flex-col gap-3">
                            {Array.from({ length: 4 }).map((_, i) => (
                                <Skeleton key={i} className="h-10 w-full" />
                            ))}
                        </div>
                    ) : recentDocuments.length === 0 ? (
                        <p className="text-center text-[var(--muted-foreground)] text-sm py-10">
                            No documents yet. Add one from the Documents page.
                        </p>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow className="border-[var(--glass-border)] hover:bg-transparent">
                                    <TableHead className="text-[var(--muted-foreground)]">Document</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Category</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Status</TableHead>
                                    <TableHead className="text-[var(--muted-foreground)]">Created</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {recentDocuments.map((doc) => (
                                    <TableRow key={doc.id} className="border-[var(--glass-border)] hover:bg-white/[0.03]">
                                        <TableCell className="font-medium text-[var(--foreground)]">{doc.title}</TableCell>
                                        <TableCell className="text-[var(--muted-foreground)]">
                                            {getCategoryTitle(doc.category_id)}
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant={STATUS_VARIANT[doc.status as DocumentStatus] ?? "secondary"}>
                                                {doc.status ?? "—"}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-[var(--muted-foreground)]">
                                            {new Date(doc.created_at).toLocaleDateString()}
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
