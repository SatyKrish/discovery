export type Role = "user" | "agent" | "tool";
export type Artifact = { id: string; type: "chart.vegaLite" | "table.json" | "file"; title: string; uri?: string; json?: unknown; pinned?: boolean };
export type Message = { id: string; role: Role; text: string; createdAt: string; artifacts?: Artifact[] };
export type Chat = { id: string; title: string; lastActivity?: string };

export interface DiscoveryAgentDataProvider {
  listChats(signal?: AbortSignal): Promise<Chat[]>;
  listMessages(chatId: string, signal?: AbortSignal): Promise<Message[]>;
  sendMessage(params: { chatId: string; text: string }, signal?: AbortSignal): Promise<void>;
  togglePin?(params: { chatId: string; artifactId: string }, signal?: AbortSignal): Promise<void>;
  createChat?(params: { title?: string }, signal?: AbortSignal): Promise<Chat | null>;
  deleteChat?(chatId: string, signal?: AbortSignal): Promise<void>;
}

export const HttpProvider: DiscoveryAgentDataProvider = {
  async listChats(signal) {
    try {
      const res = await fetch("/api/chats", { signal, cache: "no-store" });
      if (!res.ok) return [];
      const data: unknown = await res.json().catch(() => [] as unknown);
      const list = extractArray(data, ["chats", "data"]);
      return list.map(normalizeChat).filter(isDefined);
    } catch (e: any) {
      // Swallow aborts; return an empty list on cancellation or network failure
      if (e?.name === "AbortError") return [];
      return [];
    }
  },
  async listMessages(chatId, signal) {
    try {
      const res = await fetch(`/api/messages?chatId=${encodeURIComponent(chatId)}`, { signal, cache: "no-store" });
      if (!res.ok) return [];
      const data: unknown = await res.json().catch(() => [] as unknown);
      const list = extractArray(data, ["messages", "data"]);
      return list.map(normalizeMessage).filter(isDefined);
    } catch (e: any) {
      if (e?.name === "AbortError") return [];
      return [];
    }
  },
  async sendMessage(body, signal) {
    try {
      await fetch("/api/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal
      });
    } catch (e: any) {
      // Ignore aborts and network errors for demo
      return;
    }
  },
  async togglePin() {
    // no-op demo implementation
  },
  async createChat(params, signal) {
    try {
      const res = await fetch("/api/chats", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params ?? {}),
        signal
      });
      if (!res.ok) return null;
      const data: unknown = await res.json().catch(() => ({} as unknown));
      // Try to normalize from either the response root or nested under `chat`
      const candidate = (data as any)?.chat ?? data;
      return normalizeChat(candidate);
    } catch (e: any) {
      if (e?.name === "AbortError") return null;
      return null;
    }
  }
  ,
  async deleteChat(chatId, signal) {
    try {
      await fetch(`/api/chats/${encodeURIComponent(chatId)}`, { method: "DELETE", signal });
    } catch (e: any) {
      // ignore abort/network errors for demo
      return;
    }
  }
};

type Dict = Record<string, unknown>;

function isRecord(x: unknown): x is Dict {
  return typeof x === "object" && x !== null;
}

function extractArray(data: unknown, keys: string[]): unknown[] {
  if (Array.isArray(data)) return data;
  if (!isRecord(data)) return [];
  for (const k of keys) {
    const v = (data as Dict)[k];
    if (Array.isArray(v)) return v;
  }
  return [];
}

function isDefined<T>(x: T | null | undefined): x is T {
  return x !== null && x !== undefined;
}

function normalizeChat(x: unknown): Chat | null {
  if (!isRecord(x)) return null;
  const id = (x as Dict)["id"] ?? (x as Dict)["chat_id"] ?? (x as Dict)["uuid"] ?? (x as Dict)["_id"];
  const title = (x as Dict)["title"] ?? (x as Dict)["name"] ?? (id ? `Chat ${id}` : undefined);
  const lastActivity = (x as Dict)["lastActivity"] ?? (x as Dict)["last_activity"] ?? (x as Dict)["updatedAt"] ?? (x as Dict)["updated_at"];
  if (!id || !title) return null;
  return { id: String(id), title: String(title), lastActivity: lastActivity ? String(lastActivity) : undefined };
}

function normalizeMessage(x: unknown): Message | null {
  if (!isRecord(x)) return null;
  const id = (x as Dict)["id"] ?? (x as Dict)["message_id"] ?? (x as Dict)["uuid"] ?? (x as Dict)["_id"] ?? Date.now().toString();
  const role = (((x as Dict)["role"] ?? (x as Dict)["sender"]) as Role | undefined) ?? "agent";
  const text = (x as Dict)["text"] ?? (x as Dict)["content"] ?? "";
  const createdAt = (x as Dict)["createdAt"] ?? (x as Dict)["created_at"] ?? new Date().toISOString();
  const artifacts = Array.isArray((x as Dict)["artifacts"]) ? ((x as Dict)["artifacts"] as Artifact[]) : undefined;
  if (!text) return null;
  return { id: String(id), role, text: String(text), createdAt: String(createdAt), artifacts };
}
