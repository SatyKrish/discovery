export type Role = "user" | "agent" | "tool";
export type ArtifactType = "chart.vegaLite" | "chart.recharts" | "table.json" | "file";
export type Artifact = {
  id: string;
  type: ArtifactType;
  title: string;
  uri?: string;
  json?: unknown;
  pinned?: boolean;
  chatId?: string;
};
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
  listArtifacts?(params?: { filter?: "pinned" | "recent"; type?: ArtifactType }, signal?: AbortSignal): Promise<Artifact[]>;
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
  async togglePin(params, signal) {
    try {
      await fetch("/api/artifacts/toggle-pin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params ?? {}),
        signal,
      });
    } catch {
      return;
    }
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
  },
  async listArtifacts(params, signal) {
    try {
      const qs = new URLSearchParams();
      if (params?.filter) qs.set(params.filter, "true");
      if (params?.type) qs.set("type", params.type);
      const res = await fetch(`/api/artifacts${qs.toString() ? `?${qs.toString()}` : ""}`, { signal, cache: "no-store" });
      if (!res.ok) return [];
      const data: unknown = await res.json().catch(() => [] as unknown);
      const list = extractArray(data, ["artifacts", "data", "items"]);
      return list.map(normalizeArtifact).filter(isDefined);
    } catch (e: unknown) {
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return [];
      return [];
    }
  }
};

// ---------------------------------------------------------------------------
// FastAPI-backed provider (via Next.js API proxies)
// ---------------------------------------------------------------------------

const fastApiChats: Chat[] = [];

export const FastApiProvider: DiscoveryAgentDataProvider = {
  async listChats(_signal?: AbortSignal) {
    return fastApiChats;
  },
  async createChat(params, _signal?: AbortSignal) {
    try {
  const res = await fetch(`/api/workflow/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: params?.title ?? undefined }),
      });
      if (!res.ok) return null;
      const data = (await res.json().catch(() => ({}))) as { workflow_id?: unknown };
      const id = typeof data.workflow_id === "string" ? data.workflow_id : undefined;
      if (!id) return null;
      const chat: Chat = { id, title: params?.title || `Chat ${id}` };
      fastApiChats.push(chat);
      return chat;
    } catch {
      return null;
    }
  },
  async listMessages(chatId, _signal?: AbortSignal) {
    try {
  const res = await fetch(`/api/workflow/${encodeURIComponent(chatId)}/history`);
      if (!res.ok) return [];
      const data = (await res.json().catch(() => ({}))) as { history?: unknown };
      const history = Array.isArray(data.history) ? data.history : [];
      const messages: Message[] = [];
      history.forEach((h, i) => {
        if (isRecord(h)) {
          const [[role, text]] = Object.entries(h);
          if (typeof text === "string") {
            messages.push({ id: `${i}`, role: role === "user" ? "user" : "agent", text, createdAt: new Date().toISOString() });
          }
        }
      });
      return messages;
    } catch {
      return [];
    }
  },
  async sendMessage(body, signal?: AbortSignal) {
    // Fetch current history length so we know when a new agent reply appears
    let prevLen = 0;
    try {
      const before = await FastApiProvider.listMessages(body.chatId, signal);
      prevLen = before.length;
    } catch {
      prevLen = 0;
    }

    try {
      await fetch(`/api/workflow/${encodeURIComponent(body.chatId)}/prompt`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: body.text }),
        signal,
      });
    } catch {
      return;
    }

    // Poll for a new agent message for up to ~15s
    const start = Date.now();
    while (!signal?.aborted && Date.now() - start < 15000) {
      await new Promise((r) => setTimeout(r, 1000));
      try {
        const msgs = await FastApiProvider.listMessages(body.chatId, signal);
        if (msgs.slice(prevLen).some((m) => m.role === "agent")) return;
      } catch (e: unknown) {
        const name = (e as { name?: string } | null)?.name;
        if (name === "AbortError") return;
      }
    }
  },
  async deleteChat(chatId, _signal?: AbortSignal) {
    try {
  await fetch(`/api/workflow/${encodeURIComponent(chatId)}/end`, { method: "POST" });
    } catch {
    }
    const idx = fastApiChats.findIndex((c) => c.id === chatId);
    if (idx >= 0) fastApiChats.splice(idx, 1);
  },
  async listArtifacts(_params, _signal?: AbortSignal) {
    return [];
  },
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

function normalizeArtifact(x: unknown): Artifact | null {
  if (!isRecord(x)) return null;
  const id = (x as Dict)["id"] ?? (x as Dict)["artifact_id"] ?? (x as Dict)["uuid"] ?? (x as Dict)["_id"];
  const title = (x as Dict)["title"] ?? (x as Dict)["name"] ?? (id ? `Artifact ${id}` : undefined);
  const typeRaw = (x as Dict)["type"] ?? (x as Dict)["kind"];
  const type = (typeof typeRaw === "string" ? typeRaw : "file") as ArtifactType;
  const uri = (x as Dict)["uri"] ?? (x as Dict)["url"] ?? (x as Dict)["path"];
  const pinned = Boolean((x as Dict)["pinned"] ?? (x as Dict)["is_pinned"]);
  const json = (x as Dict)["json"] ?? (x as Dict)["spec"];
  const chatId = (x as Dict)["chatId"] ?? (x as Dict)["chat_id"];
  if (!id || !title) return null;
  return {
    id: String(id),
    title: String(title),
    type,
    uri: typeof uri === "string" ? uri : undefined,
    pinned,
    json,
    chatId: chatId ? String(chatId) : undefined,
  };
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
