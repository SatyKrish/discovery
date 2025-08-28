"use client";
import { HttpProvider } from "@/lib/provider";
import DiscoveryAgentUI from "@/components/DiscoveryAgentUI";

export default function HomePage() {
  return (
    <main className="h-dvh bg-background text-foreground bg-chat-pattern">
      <DiscoveryAgentUI provider={HttpProvider} />
    </main>
  );
}
