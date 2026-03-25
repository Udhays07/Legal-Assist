import React from "react";

export default function UserLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-background">
            <main className="flex-1 w-full h-full">
                {children}
            </main>
        </div>
    );
}
