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
export type Message = {
  id: string;
  role: Role;
  text: string;
  createdAt: string;
  state?: "sent" | "read";
  artifacts?: Artifact[];
};
export type Chat = { id: string; title: string; lastActivity?: string };

export interface DiscoveryAgentDataProvider {
  listChats(signal?: AbortSignal): Promise<Chat[]>;
  listMessages(chatId: string, signal?: AbortSignal): Promise<Message[]>;
  sendMessage(params: { chatId: string; text: string; attachments?: { id: string; title: string; uri: string; mime?: string; size?: number }[] }, signal?: AbortSignal): Promise<SendMessageResult>;
  confirmToolCall?(params: { chatId: string; toolCallId: string; approved: boolean; customArgs?: Record<string, any> }, signal?: AbortSignal): Promise<void>;
  togglePin?(params: { chatId: string; artifactId: string }, signal?: AbortSignal): Promise<void>;
  createChat?(params: { title?: string }, signal?: AbortSignal): Promise<Chat | null>;
  deleteChat?(chatId: string, signal?: AbortSignal): Promise<void>;
  uploadFiles?(files: File[], signal?: AbortSignal): Promise<Array<{ id: string; title: string; uri: string; mime?: string; size?: number }>>;
  listArtifacts?(params?: { filter?: "pinned" | "recent"; type?: ArtifactType }, signal?: AbortSignal): Promise<Artifact[]>;
}

export type SendMessageResult = {
  message?: Message;
  requiresApproval?: boolean;
  toolCall?: {
    id: string;
    name: string;
    args: Record<string, any>;
  };
};

export const HttpProvider: DiscoveryAgentDataProvider = {
  async listChats(signal) {
    try {
      const base = process.env.DISCOVERY_AGENT_URL || 'http://localhost:8080';
      const res = await fetch(`${base}/sessions`, { signal, cache: "no-store" });
      if (!res.ok) return [];
      const data: unknown = await res.json().catch(() => [] as unknown);
      // Transform discovery-agent sessions to chat format
      const sessions = Array.isArray(data) ? data : [];
      return sessions.map((session: any) => ({
        id: session.workflow_id || session.id,
        title: session.goal || `Session ${session.workflow_id || session.id}`,
        lastActivity: session.last_activity || new Date().toISOString()
      }));
    } catch (e: unknown) {
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return [];
      return [];
    }
  },

  async listMessages(chatId, signal) {
    try {
      const base = process.env.DISCOVERY_AGENT_URL || 'http://localhost:8080';
      const res = await fetch(`${base}/sessions/${chatId}/history`, { signal, cache: "no-store" });
      if (!res.ok) return [];
      const data: unknown = await res.json().catch(() => [] as unknown);
      const messages = Array.isArray(data) ? data : [];
      return messages.map((msg: any) => ({
        id: msg.id || Date.now().toString(),
        role: msg.role === 'user' ? 'user' : 'agent',
        text: msg.content || msg.text || '',
        createdAt: msg.timestamp || new Date().toISOString()
      }));
    } catch (e: unknown) {
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return [];
      return [];
    }
  },

  async sendMessage(params, signal) {
    try {
      const base = process.env.DISCOVERY_AGENT_URL || 'http://localhost:8080';
      const response = await fetch(`${base}/chat/send-sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: params.text,
          workflow_id: params.chatId,
          goal: "Have a helpful conversation"
        }),
        signal
      });

      const data = await response.json();

      if (data.pending_tool) {
        return {
          requiresApproval: true,
          toolCall: {
            id: data.pending_tool.id,
            name: data.pending_tool.name,
            args: data.pending_tool.args
          }
        };
      }

      return {
        message: {
          id: Date.now().toString(),
          role: 'agent',
          text: data.assistant?.content || '',
          createdAt: new Date().toISOString()
        }
      };
    } catch (e: unknown) {
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return {};
      throw e;
    }
  },

  async confirmToolCall(params, signal) {
    try {
      const base = process.env.DISCOVERY_AGENT_URL || 'http://localhost:8080';
      await fetch(`${base}/chat/confirm`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workflow_id: params.chatId,
          tool_call_id: params.toolCallId,
          approved: params.approved,
          custom_args: params.customArgs
        }),
        signal
      });
    } catch (e: unknown) {
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return;
      throw e;
    }
  },

  async createChat(params, signal) {
    try {
      const base = process.env.DISCOVERY_AGENT_URL || 'http://localhost:8080';
      const response = await fetch(`${base}/chat/send-sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: params?.title || "Hello",
          goal: "Have a helpful conversation"
        }),
        signal
      });

      if (!response.ok) return null;

      const data = await response.json();
      return {
        id: data.workflow_id,
        title: params?.title || `Chat ${data.workflow_id}`,
        lastActivity: new Date().toISOString()
      };
    } catch (e: unknown) {
      const name = (e as { name?: string } | null)?.name;
      if (name === "AbortError") return null;
      return null;
    }
  },

  async deleteChat(chatId, signal) {
    try {
      const base = process.env.DISCOVERY_AGENT_URL || 'http://localhost:8080';
      await fetch(`${base}/chat/end`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workflow_id: chatId }),
        signal
      });
    } catch {
      // ignore abort/network errors
      return;
    }
  },

  // Placeholder implementations for remaining methods
  async uploadFiles(files, signal) {
    // TODO: Implement file upload for discovery-agent
    return [];
  },

  async togglePin(params, signal) {
    // TODO: Implement artifact pinning
    return;
  },

  async listArtifacts(params, signal) {
    // TODO: Implement artifact listing
    return [];
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
  async sendMessage(body, signal?: AbortSignal): Promise<SendMessageResult> {
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
      return {};
    }

    // Poll for a new agent message for up to ~15s
    const start = Date.now();
    while (!signal?.aborted && Date.now() - start < 15000) {
      await new Promise((r) => setTimeout(r, 1000));
      try {
        const msgs = await FastApiProvider.listMessages(body.chatId, signal);
        if (msgs.slice(prevLen).some((m) => m.role === "agent")) return {};
      } catch (e: unknown) {
        const name = (e as { name?: string } | null)?.name;
        if (name === "AbortError") return {};
      }
    }
    return {};
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
  const stateRaw = (x as Dict)["state"] ?? (x as Dict)["status"];
  const state = stateRaw === "read" || stateRaw === "sent" ? (stateRaw as "read" | "sent") : undefined;
  if (!text) return null;
  return { id: String(id), role, text: String(text), createdAt: String(createdAt), state, artifacts };
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
