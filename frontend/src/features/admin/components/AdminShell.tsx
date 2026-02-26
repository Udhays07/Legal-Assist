import AdminSidebar from "./AdminSidebar";

interface AdminShellProps {
    children: React.ReactNode;
}

export default function AdminShell({ children }: AdminShellProps) {
    return (
        <div className="flex min-h-screen bg-[var(--background)]">
            <AdminSidebar />
            <main className="flex-1 overflow-y-auto p-8 min-w-0">
                {children}
            </main>
        </div>
    );
}
