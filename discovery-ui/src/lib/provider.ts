export type Role = "user" | "agent" | "tool";
export type Artifact = { id: string; type: "chart.vegaLite" | "table.json" | "file"; title: string; uri?: string; json?: unknown; pinned?: boolean };
export type Message = { id: string; role: Role; text: string; createdAt: string; artifacts?: Artifact[] };
export type Chat = { id: string; title: string; lastActivity?: string };

export interface DiscoveryAgentDataProvider {
  listChats(signal?: AbortSignal): Promise<Chat[]>;
  listMessages(chatId: string, signal?: AbortSignal): Promise<Message[]>;
  sendMessage(params: { chatId: string; text: string }, signal?: AbortSignal): Promise<void>;
  togglePin(params: { chatId: string; artifactId: string }, signal?: AbortSignal): Promise<void>;
}

export const HttpProvider: DiscoveryAgentDataProvider = {
  async listChats(signal) {
    const res = await fetch("/api/chats", { signal, cache: "no-store" });
    return res.json();
  },
  async listMessages(chatId, signal) {
    const res = await fetch(`/api/messages?chatId=${encodeURIComponent(chatId)}`, { signal, cache: "no-store" });
    return res.json();
  },
  async sendMessage(body, signal) {
    await fetch("/api/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal
    });
  },
  async togglePin() {
    // no-op demo implementation
  }
};
