"use client";
import React, { useEffect, useMemo, useState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Send, Paperclip, Search, MoreVertical, Pin as PinIcon, Menu, Sun, Moon, FileDown, Pencil, Image as ImageIcon } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/***********************************
 * Types
 ***********************************/
export type Role = "user" | "agent" | "tool";
export type Artifact = { id: string; type: "chart.vegaLite" | "table.json" | "file"; title: string; uri?: string; json?: unknown; pinned?: boolean };
export type Message = { id: string; role: Role; text: string; createdAt: string; artifacts?: Artifact[] };
export type Chat = { id: string; title: string; lastActivity?: string };

/***********************************
 * Provider contract
 ***********************************/
export interface DiscoveryAgentDataProvider {
  listChats(signal?: AbortSignal): Promise<Chat[]>;
  listMessages(chatId: string, signal?: AbortSignal): Promise<Message[]>;
  sendMessage(params: { chatId: string; text: string }, signal?: AbortSignal): Promise<void>;
  togglePin?(params: { chatId: string; artifactId: string }, signal?: AbortSignal): Promise<void>;
}

export const NoopProvider: DiscoveryAgentDataProvider = {
  async listChats() { return []; },
  async listMessages() { return []; },
  async sendMessage() { return; },
};

/***********************************
 * Sidebar (Chat search + new chat)
 ***********************************/
function Sidebar({
  chats,
  selectedId,
  onSelect,
  onNew,
  collapsed,
  setCollapsed,
  isLoading,
}: {
  chats: Chat[];
  selectedId?: string;
  onSelect: (id: string) => void;
  onNew: () => void;
  collapsed: boolean;
  setCollapsed: (b: boolean) => void;
  isLoading?: boolean;
}) {
  const searchInputRef = React.useRef<HTMLInputElement>(null);
  const focusSearch = () => {
    if (collapsed) {
      setCollapsed(false);
      setTimeout(() => searchInputRef.current?.focus(), 0);
    } else {
      searchInputRef.current?.focus();
    }
  };
  return (
    <div className={cn("h-full w-full flex flex-col border-r bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60")}> 
      <div className="px-3 py-2 flex items-center gap-2 h-14 border-b">
        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setCollapsed(!collapsed)} aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}>
          <Menu className="h-4 w-4" />
        </Button>
        {!collapsed && <div className="font-semibold truncate">Chats</div>}
      </div>

      <div className={cn("p-3", collapsed && "p-2")}> 
        {collapsed ? (
          <div className="flex flex-col items-center gap-3">
            <Tooltip>
              <TooltipTrigger asChild>
                <Button size="icon" variant="secondary" className="h-9 w-9 rounded-full" onClick={onNew} aria-label="New chat" title="New chat">
                  <Pencil className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">New chat</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button size="icon" variant="secondary" className="h-9 w-9 rounded-full" onClick={focusSearch} aria-label="Search chats" title="Search chats">
                  <Search className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">Search chats</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button size="icon" variant="secondary" className="h-9 w-9 rounded-full" onClick={() => { /* TODO: open library */ }} aria-label="Library" title="Library">
                  <ImageIcon className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">Library</TooltipContent>
            </Tooltip>
          </div>
        ) : (
          <div className="space-y-2">
            <Button variant="ghost" className="w-full justify-start gap-2" onClick={onNew}>
              <Pencil className="h-4 w-4" /> New chat
            </Button>
            <Button variant="ghost" className="w-full justify-start gap-2" onClick={focusSearch}>
              <Search className="h-4 w-4" /> Search chats
            </Button>
            <Button variant="ghost" className="w-full justify-start gap-2" onClick={() => { /* TODO: open library */ }}>
              <ImageIcon className="h-4 w-4" /> Library
            </Button>
          </div>
        )}
      </div>

      {!collapsed && (
        <div className="px-3 pb-2">
          <div className="relative">
            <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input ref={searchInputRef} placeholder="Search chats" className="pl-7 h-8" />
          </div>
        </div>
      )}

      <ScrollArea className="flex-1">
        <div className={cn("px-2 pb-2 space-y-1")}> 
          {isLoading && Array.from({ length: 6 }).map((_, i) => (<div key={i} className="h-9 rounded-md bg-muted animate-pulse"/>))}
          {/* no empty-state message for chats list */}
          {!isLoading && chats.map((c) => (
            <button key={c.id} onClick={() => onSelect(c.id)} className={cn("w-full rounded-lg border px-3 py-2 text-left hover:bg-muted/50 transition", selectedId === c.id ? "border-primary/40 bg-muted" : "border-border/60 bg-background")}>
              <div className="truncate text-sm text-foreground">{c.title}</div>
              {c.lastActivity && <div className="text-[10px] text-muted-foreground mt-1">{c.lastActivity}</div>}
            </button>
          ))}
        </div>
      </ScrollArea>

      <div className="border-t p-3 flex items-center justify-end">
        <ThemeToggleInline />
      </div>
    </div>
  );
}

function ThemeToggleInline() {
  const [dark, setDark] = useState(false);
  useEffect(() => { const saved = typeof window !== "undefined" ? localStorage.getItem("theme") : null; if (saved === "dark" || saved === "light") setDark(saved === "dark"); }, []);
  useEffect(() => { if (typeof document !== "undefined") { document.documentElement.classList.toggle("dark", dark); document.documentElement.setAttribute("data-theme", dark ? "dark" : "light"); try { localStorage.setItem("theme", dark ? "dark" : "light"); } catch {} } }, [dark]);
  return (
    <TooltipProvider>
  <Tooltip>
        <TooltipTrigger asChild>
          <Button variant="outline" size="icon" onClick={() => setDark(!dark)} aria-label={dark ? "Switch to light" : "Switch to dark"}>
            {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
        </TooltipTrigger>
        <TooltipContent side="top" className="pointer-events-none select-none">
          {dark ? "Light mode" : "Dark mode"}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}

/***********************************
 * Artifact preview (minimal)
 ***********************************/
function ArtifactPreview({ artifact }: { artifact: Artifact }) {
  return (
    <Card className="rounded-2xl shadow-sm border-border/60">
      <CardHeader className="p-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-semibold truncate text-foreground">{artifact.title}</CardTitle>
          <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground"><MoreVertical className="h-4 w-4" /></Button>
        </div>
        <div className="text-xs text-muted-foreground">
          <div className="flex items-center gap-2">
            <Badge variant="secondary" className="bg-muted text-foreground">{artifact.type}</Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-4 pt-0">
        {artifact.type === "table.json" ? (
          <TableArtifact artifact={artifact} />
        ) : (
          <div className="h-24 flex items-center justify-center bg-muted/30 rounded-md text-sm text-foreground">
            <FileDown className="h-4 w-4 mr-2" /> {artifact.title}
          </div>
        )}
      </CardContent>
      <CardFooter className="p-4 pt-0 flex gap-2">
        <Button size="sm" variant="outline">Expand</Button>
        <Button size="sm" variant="ghost" className="text-muted-foreground"><PinIcon className="h-4 w-4 mr-1" /> {artifact.pinned ? "Unpin" : "Pin"}</Button>
      </CardFooter>
    </Card>
  );
}

function TableArtifact({ artifact }: { artifact: Artifact }) {
  const [cols, setCols] = useState<string[]>([]);
  const [rows, setRows] = useState<Record<string, unknown>[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      if (artifact.type !== "table.json") return;
      setLoading(true);
      setError(null);
      try {
        let input: unknown = artifact.json;
        if (!input && artifact.uri) {
          const res = await fetch(artifact.uri, { cache: "no-store" });
          if (!res.ok) throw new Error(`Failed to fetch table: ${res.status}`);
          input = await res.json();
        }
        const norm = normalizeTable(input);
        if (!cancelled) {
          setCols(norm.columns);
          setRows(norm.data);
        }
      } catch (e) {
        if (!cancelled) setError("Failed to load table data");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; };
  }, [artifact]);

  if (loading) return <div className="h-24 rounded-md bg-muted animate-pulse" />;
  if (error) return <div className="text-sm text-red-500">{error}</div>;
  if (!cols.length || !rows.length) return <div className="text-sm text-muted-foreground">No rows</div>;

  return (
    <div className="w-full overflow-x-auto">
      <Table className="min-w-[480px]">
        <TableHeader>
          <TableRow>
            {cols.map((c) => (
              <TableHead key={c} className="whitespace-nowrap">{c}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((r, i) => (
            <TableRow key={i}>
              {cols.map((c) => (
                <TableCell key={c} className="align-top">
                  {formatCell((r as Record<string, unknown>)[c])}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

function normalizeTable(input: unknown): { columns: string[]; data: Record<string, unknown>[] } {
  if (!input) return { columns: [], data: [] };
  // Case 1: array of objects
  if (Array.isArray(input)) {
    const rows = input.filter((x) => x && typeof x === "object") as Record<string, unknown>[];
    const columns = Array.from(new Set(rows.flatMap((r) => Object.keys(r))));
    return { columns, data: rows };
  }
  // Case 2: object with data array
  if (typeof input === "object") {
    const o = input as Record<string, unknown>;
    if (Array.isArray(o.data)) return normalizeTable(o.data);
    // Case 3: columns + rows (2D array)
    if (Array.isArray(o.columns) && Array.isArray(o.rows)) {
      const cols = (o.columns as unknown[]).map(String);
      const data = (o.rows as unknown[]).map((row) => {
        const arr = Array.isArray(row) ? row : [];
        const obj: Record<string, unknown> = {};
        cols.forEach((c, i) => { obj[c] = arr[i]; });
        return obj;
      });
      return { columns: cols, data };
    }
    // Fallback: single object -> single row
    return { columns: Object.keys(o), data: [o] };
  }
  // Primitive fallback
  return { columns: ["value"], data: [{ value: input }] };
}

function formatCell(v: unknown) {
  if (v == null) return <span className="text-muted-foreground">—</span>;
  if (typeof v === "object") {
    try { return <span className="text-xs text-muted-foreground break-words">{JSON.stringify(v)}</span>; } catch { /* noop */ }
  }
  return String(v);
}

/***********************************
 * Message Bubble
 ***********************************/
function MessageBubble({ m }: { m: Message }) {
  const isUser = m.role === "user";
  return (
    <div className={cn("flex gap-3", isUser ? "justify-end" : "justify-start")}> 
      {!isUser && (
        <Avatar className="h-8 w-8 mt-1"><AvatarFallback>A</AvatarFallback></Avatar>
      )}
      <div className="max-w-[720px] w-full">
        <div className={cn("rounded-2xl p-4 border", isUser ? "bg-primary text-primary-foreground" : "bg-card text-card-foreground border-border/60")}> 
          <div className="prose dark:prose-invert max-w-none text-[15px] leading-7">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.text}</ReactMarkdown>
          </div>
        </div>
        {m.artifacts?.length ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3 mt-3">
            {m.artifacts.map((a) => (
              <ArtifactPreview key={a.id} artifact={a} />
            ))}
          </div>
        ) : null}
        <div className="text-[11px] text-muted-foreground mt-2">{m.createdAt}</div>
      </div>
      {isUser && (
        <Avatar className="h-8 w-8 mt-1"><AvatarFallback>U</AvatarFallback></Avatar>
      )}
    </div>
  );
}

/***********************************
 * Composer
 ***********************************/
function Composer({ value, onChange, onSend }: { value: string; onChange: (v: string) => void; onSend: () => void }) {
  return (
    <div className="sticky bottom-0 bg-gradient-to-t from-background via-background/95 to-background/0">
      <div className="mx-auto max-w-[920px] px-4 pb-4">
        <div className="rounded-2xl border bg-background shadow-sm">
          <Textarea
            placeholder="Message Discovery Agent…"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={(e) => {
              if ((e.metaKey || e.ctrlKey) && e.key === "Enter") onSend();
            }}
            className="min-h-[72px] resize-none border-0 focus-visible:ring-0"
          />
          <div className="flex items-center justify-between px-2 pb-2">
            <div className="flex items-center gap-2">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon"><Paperclip className="h-4 w-4" /></Button>
                </TooltipTrigger>
                <TooltipContent side="top" className="pointer-events-none select-none">Attach file</TooltipContent>
              </Tooltip>
              <Checkbox id="pin-next" />
              <label htmlFor="pin-next" className="text-xs text-muted-foreground">Pin next artifact</label>
            </div>
            <div className="flex items-center gap-2">
              <Button size="sm" onClick={onSend}><Send className="h-4 w-4 mr-1" /> Send</Button>
            </div>
          </div>
        </div>
        <div className="text-[11px] text-muted-foreground mt-2 text-center">AI may produce inaccurate information. Verify critical outputs.</div>
      </div>
    </div>
  );
}

/***********************************
 * Root UI (Grid with collapsible left + inline right)
 ***********************************/
export default function DiscoveryChat({ provider = NoopProvider }: { provider?: DiscoveryAgentDataProvider }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [composer, setComposer] = useState("");

  const [chats, setChats] = useState<Chat[]>([]);
  const [selectedChatId, setSelectedChatId] = useState<string | undefined>();
  const [loadingChats, setLoadingChats] = useState(false);
  const [artifactsOpen, setArtifactsOpen] = useState(false);
  const [collapsed, setCollapsed] = useState(false);

  // load chats
  React.useEffect(() => {
    const ac = new AbortController();
    setLoadingChats(true);
    provider.listChats(ac.signal).then((list) => {
      setChats(list);
    }).finally(() => setLoadingChats(false));
    return () => ac.abort();
  }, [provider]);

  // choose initial chat when chats load
  React.useEffect(() => {
    if (!selectedChatId && chats[0]?.id) setSelectedChatId(chats[0].id);
  }, [chats, selectedChatId]);

  // load messages when a chat is selected
  React.useEffect(() => {
    if (!selectedChatId) return;
    const ac = new AbortController();
    provider.listMessages(selectedChatId, ac.signal).then((list) => setMessages(list));
    return () => ac.abort();
  }, [selectedChatId, provider]);

  const onSend = () => {
    if (!composer.trim()) return;
    const now = new Date().toLocaleTimeString();
    const newMsg: Message = { id: String(Date.now()), role: "user", text: composer, createdAt: now };
    setMessages((prev) => [...prev, newMsg]);
    setComposer("");
    const ac = new AbortController();
    provider
      .sendMessage({ chatId: selectedChatId || "demo", text: newMsg.text }, ac.signal)
      .then(() => {
        if (!selectedChatId) return;
        return provider.listMessages(selectedChatId).then((list) => setMessages(list));
      })
      .catch(() => { /* ignore demo errors */ });
  };

  const selectedChat = useMemo(() => chats.find((c) => c.id === selectedChatId), [chats, selectedChatId]);
  const allArtifacts = useMemo(() => messages.flatMap(m => m.artifacts ?? []), [messages]);

  return (
    <TooltipProvider>
      <div
        className="h-screen w-full grid bg-background text-foreground"
        style={{
          gridTemplateColumns: `${collapsed ? "64px" : "260px"} 1fr ${artifactsOpen ? "420px" : "0px"}`,
        }}
      >
        {/* LEFT COLUMN: sidebar */}
        <div className="min-w-0">
          <Sidebar
            chats={chats}
            selectedId={selectedChatId}
            onSelect={setSelectedChatId}
            onNew={() => setSelectedChatId(undefined)}
            collapsed={collapsed}
            setCollapsed={setCollapsed}
            isLoading={loadingChats}
          />
        </div>

        {/* CENTER COLUMN */}
        <div className="min-w-0 flex flex-col">
          {/* Header */}
          <div className="h-14 border-b flex items-center justify-between px-4 bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-10">
            <div className="flex items-center gap-2 min-w-0">
              <div className="text-base font-semibold truncate max-w-[60vw]">{selectedChat?.title ?? "New Chat"}</div>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setArtifactsOpen(!artifactsOpen)}
                className="relative"
              >
                Artifacts
                {allArtifacts.length > 0 && (
                  <span className="ml-2 inline-flex h-5 min-w-[20px] items-center justify-center rounded-full bg-primary text-primary-foreground px-1 text-[10px] font-medium">
                    {allArtifacts.length}
                  </span>
                )}
              </Button>
              <Avatar><AvatarFallback>U</AvatarFallback></Avatar>
            </div>
          </div>

          {/* Thread */}
          <ScrollArea className="flex-1 p-4">
            <div className="mx-auto w-full max-w-[920px] space-y-6">
              {messages.map((m) => (
                <MessageBubble key={m.id} m={m} />
              ))}
            </div>
          </ScrollArea>

          {/* Composer */}
          <Composer value={composer} onChange={setComposer} onSend={onSend} />
        </div>

        {/* RIGHT COLUMN: artifacts inline */}
        <div className="border-l overflow-hidden transition-[width] duration-200 ease-out">
          <div className="h-14 border-b flex items-center px-4 font-semibold">Artifacts</div>
          <ScrollArea className="h-[calc(100vh-3.5rem)] p-3">
            <div className="grid grid-cols-1 gap-3">
              {allArtifacts.length ? (
                allArtifacts.map((a) => <ArtifactPreview key={a.id} artifact={a} />)
              ) : (
                <div className="text-sm text-muted-foreground p-6 text-center">No artifacts yet</div>
              )}
            </div>
          </ScrollArea>
        </div>
      </div>
    </TooltipProvider>
  );
}
