import React from "react";
import { ChatInterface } from "@/features/user/components/ChatInterface";

export default function ChatPage() {
    return (
        <div className="flex flex-col h-screen w-full">
            <main className="flex-1 relative w-full overflow-hidden">
                <ChatInterface />
            </main>
        </div>
    );
}
