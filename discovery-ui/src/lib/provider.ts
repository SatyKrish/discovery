export type Role = "user" | "agent" | "tool";
export type Artifact = { id: string; type: "chart.vegaLite" | "table.json" | "file"; title: string; uri?: string; json?: unknown; pinned?: boolean };
export type Message = { id: string; role: Role; text: string; createdAt: string; artifacts?: Artifact[] };
export type Chat = { id: string; title: string; lastActivity?: string };

export interface DiscoveryAgentDataProvider {
  listChats(signal?: AbortSignal): Promise<Chat[]>;
  listMessages(chatId: string, signal?: AbortSignal): Promise<Message[]>;
  sendMessage(params: { chatId: string; text: string; attachments?: { id: string; title: string; uri: string; mime?: string; size?: number }[] }, signal?: AbortSignal): Promise<void>;
  togglePin?(params: { chatId: string; artifactId: string }, signal?: AbortSignal): Promise<void>;
  createChat?(params: { title?: string }, signal?: AbortSignal): Promise<Chat | null>;
  deleteChat?(chatId: string, signal?: AbortSignal): Promise<void>;
  uploadFiles?(files: File[], signal?: AbortSignal): Promise<Array<{ id: string; title: string; uri: string; mime?: string; size?: number }>>;
}

export const HttpProvider: DiscoveryAgentDataProvider = {
  async listChats(signal) {
    try {
      const res = await fetch("/api/chats", { signal, cache: "no-store" });
      if (!res.ok) return [];
      const data: unknown = await res.json().catch(() => [] as unknown);
      const list = extractArray(data, ["chats", "data"]);
      return list.map(normalizeChat).filter(isDefined);
    } catch (e: unknown) {
      // Swallow aborts; return an empty list on cancellation or network failure
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return [];
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
    } catch (e: unknown) {
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return [];
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
  } catch {
      // Ignore aborts and network errors for demo
      return;
    }
  },
  async uploadFiles(files, signal) {
    const fd = new FormData();
    files.forEach((f) => fd.append("files", f));
    try {
      const res = await fetch("/api/uploads", { method: "POST", body: fd, signal });
      if (!res.ok) return [];
      const data: unknown = await res.json().catch(() => ({} as unknown));
      // Normalize response to array of { id, title, uri, mime, size }
      const rec = data as Record<string, unknown>;
      const filesArr = Array.isArray(data)
        ? (data as unknown[])
        : (Array.isArray(rec["files"]) ? (rec["files"] as unknown[]) : (Array.isArray(rec["data"]) ? (rec["data"] as unknown[]) : []));
      const norm = filesArr
        .map(normalizeUploadItem)
        .filter((x): x is { id: string; title: string; uri: string; mime?: string; size?: number } => Boolean(x));
      return norm;
    } catch (e: unknown) {
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return [];
      return [];
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
    const candidate = (data as Record<string, unknown>)["chat"] ?? data;
      return normalizeChat(candidate);
    } catch (e: unknown) {
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return null;
      return null;
    }
  }
  ,
  async deleteChat(chatId, signal) {
    try {
      await fetch(`/api/chats/${encodeURIComponent(chatId)}`, { method: "DELETE", signal });
  } catch {
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

export function normalizeUploadItem(x: unknown): { id: string; title: string; uri: string; mime?: string; size?: number } | null {
  if (!x || typeof x !== "object") return null;
  const r = x as Record<string, unknown>;
  const id = (r["id"] ?? r["fileId"] ?? r["uuid"] ?? r["_id"]) as string | undefined;
  const title = (r["title"] ?? r["name"] ?? r["filename"]) as string | undefined;
  const uri = (r["uri"] ?? r["url"] ?? r["path"]) as string | undefined;
  const mime = (r["mime"] ?? r["mimetype"] ?? r["contentType"]) as string | undefined;
  const size = typeof r["size"] === "number" ? (r["size"] as number) : undefined;
  if (!uri) return null;
  return { id: String(id ?? Math.random().toString(36).slice(2)), title: String(title ?? "file"), uri: String(uri), mime, size };
}
