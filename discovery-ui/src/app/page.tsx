"use client";
import React from "react";
import { HttpProvider } from "@/lib/provider";
import DiscoveryChat, { Chat } from "@/components/DiscoveryChat";
import { Button } from "@/components/ui/button";
import { Mic, AudioLines, Plus } from "lucide-react";

export default function HomePage() {
  const [chats, setChats] = React.useState<Chat[] | null>(null);
  const [enteredChat, setEnteredChat] = React.useState(false);

  React.useEffect(() => {
    const ac = new AbortController();
    HttpProvider.listChats(ac.signal).then(setChats).catch(() => setChats([]));
    return () => ac.abort();
  }, []);

  const showHero = (chats?.length === 0) && !enteredChat;

  // After switching to chat view, ask the chat to create a new chat and focus the composer
  React.useEffect(() => {
    if (!showHero && enteredChat) {
      const t = setTimeout(() => {
        try {
          window.dispatchEvent(new Event("discovery:new-chat"));
          window.dispatchEvent(new Event("discovery:focus-composer"));
        } catch {}
      }, 150);
      return () => clearTimeout(t);
    }
  }, [showHero, enteredChat]);

  return (
    <main className="h-dvh bg-background text-foreground bg-chat-pattern">
      {showHero ? (
        <div className="h-full w-full flex items-center justify-center">
          <div className="text-center px-6">
            <h1 className="text-3xl sm:text-4xl font-semibold mb-8 text-foreground">Hey, Saty. Ready to dive in?</h1>
            <div className="mx-auto max-w-xl">
              <div className="flex items-center gap-3 rounded-full bg-muted/50 border px-4 py-3 shadow-sm">
                <div className="flex items-center gap-3 text-muted-foreground">
                  <Plus className="h-4 w-4" />
                  <span className="text-sm">Ask anything</span>
                </div>
                <div className="ml-auto flex items-center gap-2 text-muted-foreground">
                  <Mic className="h-4 w-4" />
                  <AudioLines className="h-4 w-4" />
                </div>
              </div>
              <div className="mt-4 text-xs text-muted-foreground">Tip: Press ⌘⏎ to send</div>
              <div className="mt-6">
                <Button onClick={() => setEnteredChat(true)}>Start chatting</Button>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <DiscoveryChat provider={HttpProvider} />
      )}
    </main>
  );
}
