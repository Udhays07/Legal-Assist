import React from "react";

export default function UserLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-background">
            {/* Basic header for the user area */}
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                <div className="container flex h-14 items-center">
                    <div className="font-semibold px-4 cursor-pointer hover:opacity-80">
                        Legal Assistant
                    </div>
                    <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
                        <nav className="flex items-center space-x-6 text-sm font-medium">
                            <a href="/user/chat" className="transition-colors hover:text-foreground/80 text-foreground">Chat</a>
                        </nav>
                    </div>
                </div>
            </header>

            <main className="flex-1">
                {children}
            </main>
        </div>
    );
}
