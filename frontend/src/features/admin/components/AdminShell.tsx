import AdminSidebar from "./AdminSidebar";

interface AdminShellProps {
    children: React.ReactNode;
}

export default function AdminShell({ children }: AdminShellProps) {
    return (
        <div className="flex min-h-screen bg-background text-foreground relative">
            <AdminSidebar />
            <main className="flex-1 min-w-0 flex flex-col relative h-screen">
                <div className="flex-1 overflow-y-auto w-full h-full p-8 pb-32">
                    {children}
                </div>
            </main>
        </div>
    );
}
