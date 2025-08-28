"use client";
import { HttpProvider } from "@/lib/provider";
import DiscoveryChat from "@/components/DiscoverChat";

export default function HomePage() {
  return (
    <main className="h-dvh bg-background text-foreground bg-chat-pattern">
      <DiscoveryChat provider={HttpProvider} />
    </main>
  );
}
