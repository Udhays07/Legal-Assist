import React from "react";
import { ChatInterface } from "@/features/user/components/ChatInterface";

export default function ChatPage() {
    // Mock user id
    const mockUserId = "123e4567-e89b-12d3-a456-426614174000";

    return (
        <div className="flex flex-col h-[calc(100vh-4rem)] w-full">
            <main className="flex-1 relative w-full overflow-hidden">
                <ChatInterface userId={mockUserId} />
            </main>
        </div>
    );
}
