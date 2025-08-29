"use client";
import React, { useEffect, useMemo, useRef, useState } from "react";
import { cn } from "@/lib/utils";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { useVirtualizer, elementScroll } from "@tanstack/react-virtual";
import { getFallbackVirtualItems } from "@/lib/virtual";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import {
  Send,
  Paperclip,
  Search,
  MoreVertical,
  Pin as PinIcon,
  Menu,
  Sun,
  Moon,
  FileDown,
  Pencil,
  Image as ImageIcon,
  Trash2,
  Check,
  CheckCheck,
  Loader2,
} from "lucide-react";
import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Link from "next/link";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
  BarChart,
  Bar,
  AreaChart,
  Area,
} from "recharts";

/***********************************
 * Types
 ***********************************/
export type Role = "user" | "agent" | "tool";
export type Artifact = { id: string; type: "chart.vegaLite" | "chart.recharts" | "table.json" | "file"; title: string; uri?: string; json?: unknown; pinned?: boolean };
export type Message = {
  id: string;
  role: Role;
  text: string;
  createdAt: string;
  state?: "sent" | "read";
  artifacts?: Artifact[];
};
export type Chat = { id: string; title: string; lastActivity?: string };

/***********************************
 * Provider contract
 ***********************************/
export interface DiscoveryAgentDataProvider {
  listChats(signal?: AbortSignal): Promise<Chat[]>;
  listMessages(chatId: string, signal?: AbortSignal): Promise<Message[]>;
  sendMessage(params: { chatId: string; text: string; attachments?: { id: string; title: string; uri: string; mime?: string; size?: number }[] }, signal?: AbortSignal): Promise<void>;
  togglePin?(params: { chatId: string; artifactId: string }, signal?: AbortSignal): Promise<void>;
  createChat?(params: { title?: string }, signal?: AbortSignal): Promise<Chat | null>;
  deleteChat?(chatId: string, signal?: AbortSignal): Promise<void>;
  uploadFiles?(files: File[], signal?: AbortSignal): Promise<Array<{ id: string; title: string; uri: string; mime?: string; size?: number }>>;
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
  onDelete,
  collapsed,
  setCollapsed,
  isLoading,
}: {
  chats: Chat[];
  selectedId?: string;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete: (id: string) => void;
  collapsed: boolean;
  setCollapsed: (b: boolean) => void;
  isLoading?: boolean;
}) {
  const searchInputRef = React.useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState("");
  const focusSearch = () => {
    if (collapsed) {
      setCollapsed(false);
      setTimeout(() => searchInputRef.current?.focus(), 0);
    } else {
      searchInputRef.current?.focus();
    }
  };
  // external request to focus search (for Cmd+K)
  useEffect(() => {
    const handler = () => focusSearch();
    window.addEventListener("discovery:focus-chat-search", handler as EventListener);
    return () => window.removeEventListener("discovery:focus-chat-search", handler as EventListener);
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return chats;
    return chats.filter((c) => c.title.toLowerCase().includes(q));
  }, [chats, query]);
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
                <Link
                  href="/library"
                  aria-label="Library"
                  title="Library"
                  className={cn(
                    buttonVariants({ variant: "secondary", size: "icon" }),
                    "h-9 w-9 rounded-full inline-flex"
                  )}
                >
                  <ImageIcon className="h-4 w-4" />
                </Link>
              </TooltipTrigger>
              <TooltipContent side="right">Library</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button size="icon" variant="secondary" className="h-9 w-9 rounded-full" onClick={focusSearch} aria-label="Search chats" title="Search chats">
                  <Search className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">Search chats</TooltipContent>
            </Tooltip>
          </div>
        ) : (
          <div className="space-y-2">
            <Button variant="ghost" className="w-full justify-start gap-2" onClick={onNew}>
              <Pencil className="h-4 w-4" /> New chat
            </Button>
            <Link
              href="/library"
              className={cn(buttonVariants({ variant: "ghost" }), "w-full justify-start gap-2")}
            >
              <ImageIcon className="h-4 w-4" /> Library
            </Link>
          </div>
        )}
      </div>

      {!collapsed && (
        <div className="px-3 pb-2">
          <div className="relative">
            <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              ref={searchInputRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search chats"
              className="pl-7 h-8"
            />
          </div>
        </div>
      )}

      {collapsed ? (
        <div className="flex-1" />
      ) : (
        <ScrollArea className="flex-1">
          <div className={cn("px-2 pb-2 space-y-1")}> 
            {isLoading && Array.from({ length: 6 }).map((_, i) => (<div key={i} className="h-9 rounded-md bg-muted animate-pulse"/>))}
            {/* no empty-state message for chats list */}
            {!isLoading && filtered.map((c) => (
              <div key={c.id} className={cn("w-full rounded-lg border px-2 py-2 text-left hover:bg-muted/50 transition flex items-center gap-2", selectedId === c.id ? "border-primary/40 bg-muted" : "border-border/60 bg-background") }>
                <button onClick={() => onSelect(c.id)} className="flex-1 text-left min-w-0">
                  <div className="truncate text-sm text-foreground">{c.title}</div>
                  {c.lastActivity && <div className="text-[10px] text-muted-foreground mt-1">{c.lastActivity}</div>}
                </button>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-7 w-7 text-muted-foreground"
                      onClick={(e) => {
                        e.stopPropagation();
                        if (confirm(`Delete chat \"${c.title}\"?`)) onDelete(c.id);
                      }}
                      aria-label={`Delete chat ${c.title}`}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent side="left">Delete</TooltipContent>
                </Tooltip>
              </div>
            ))}
          </div>
        </ScrollArea>
      )}

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
          <Button
            variant="outline"
            size="icon"
            onClick={() => setDark(!dark)}
            aria-label={dark ? "Switch to light" : "Switch to dark"}
            className="transition-colors duration-300 motion-reduce:transition-none"
          >
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
function ArtifactPreview({ artifact, onTogglePin }: { artifact: Artifact; onTogglePin?: (artifactId: string) => void }) {
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
        ) : artifact.type === "chart.recharts" || artifact.type === "chart.vegaLite" ? (
          <ChartArtifact artifact={artifact} />
        ) : (
          <div className="flex items-center justify-between gap-3 bg-muted/30 rounded-md text-sm text-foreground p-3">
            <div className="truncate">
              <div className="font-medium truncate">{artifact.title}</div>
              {artifact.uri && <div className="text-xs text-muted-foreground truncate">{artifact.uri}</div>}
            </div>
            {artifact.uri ? (
              <a href={artifact.uri} target="_blank" rel="noreferrer" className={cn(buttonVariants({ variant: "outline", size: "sm" }))}>
                <FileDown className="h-4 w-4 mr-1" /> Download
              </a>
            ) : null}
          </div>
        )}
      </CardContent>
      <CardFooter className="p-4 pt-0 flex gap-2">
        <Button size="sm" variant="outline">Expand</Button>
        <Button size="sm" variant="ghost" className="text-muted-foreground" onClick={() => onTogglePin?.(artifact.id)}>
          <PinIcon className={cn("h-4 w-4 mr-1", artifact.pinned && "text-primary")}/> {artifact.pinned ? "Unpin" : "Pin"}
        </Button>
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
    const ac = new AbortController();
    async function load() {
      if (artifact.type !== "table.json") return;
      setLoading(true);
      setError(null);
      try {
        let input: unknown = artifact.json;
        if (!input && artifact.uri) {
          const res = await fetch(artifact.uri, { cache: "no-store", signal: ac.signal });
          if (!res.ok) throw new Error(`Failed to fetch table: ${res.status}`);
          input = await res.json();
        }
        const norm = normalizeTable(input);
        if (!cancelled) {
          setCols(norm.columns);
          setRows(norm.data);
        }
      } catch (e: unknown) {
        const name = (e as { name?: string } | null)?.name;
        if (name === "AbortError") return;
        if (!cancelled) setError("Failed to load table data");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; ac.abort(); };
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
 * Chart Artifact (Recharts minimal)
 ***********************************/
type ChartSpec = {
  kind?: "line" | "bar" | "area";
  data?: Array<Record<string, unknown>>;
  xKey?: string;
  yKey?: string;
  color?: string;
};

function normalizeChart(input: unknown): ChartSpec {
  if (!input || typeof input !== "object") return {};
  const o = input as Record<string, unknown>;
  const kind = (typeof o.kind === "string" ? o.kind : "line") as ChartSpec["kind"];
  const data = Array.isArray(o.data) ? (o.data as Array<Record<string, unknown>>) : [];
  const xKey = typeof o.xKey === "string" ? (o.xKey as string) : (data[0] ? Object.keys(data[0])[0] : undefined);
  const yKey = typeof o.yKey === "string" ? (o.yKey as string) : (data[0] ? Object.keys(data[0])[1] : undefined);
  const color = typeof o.color === "string" ? (o.color as string) : "hsl(var(--primary))";
  return { kind, data, xKey, yKey, color };
}

function ChartArtifact({ artifact }: { artifact: Artifact }) {
  const [spec, setSpec] = useState<ChartSpec>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const ac = new AbortController();
    async function load() {
      setLoading(true);
      setError(null);
      try {
        let input: unknown = artifact.json;
        if (!input && artifact.uri) {
          const res = await fetch(artifact.uri, { cache: "no-store", signal: ac.signal });
          if (!res.ok) throw new Error(`Failed to fetch chart: ${res.status}`);
          input = await res.json();
        }
        const s = normalizeChart(input);
        if (!cancelled) setSpec(s);
      } catch (e: unknown) {
        const name = (e as { name?: string } | null)?.name;
        if (name === "AbortError") return;
        if (!cancelled) setError("Failed to load chart data");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; ac.abort(); };
  }, [artifact]);

  if (loading) return <div className="h-40 rounded-md bg-muted animate-pulse" />;
  if (error) return <div className="text-sm text-red-500">{error}</div>;
  if (!spec.data?.length || !spec.xKey || !spec.yKey) return <div className="text-sm text-muted-foreground">No chart data</div>;

  const commonAxes = (
    <>
      <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
      <XAxis dataKey={spec.xKey} tickMargin={8} />
      <YAxis tickMargin={8} />
      <RechartsTooltip />
    </>
  );

  return (
    <div className="w-full h-[260px]">
      <ResponsiveContainer width="100%" height="100%">
        {spec.kind === "bar" ? (
          <BarChart data={spec.data}>
            {commonAxes}
            <Bar dataKey={spec.yKey} fill={spec.color} />
          </BarChart>
        ) : spec.kind === "area" ? (
          <AreaChart data={spec.data}>
            {commonAxes}
            <Area dataKey={spec.yKey} stroke={spec.color} fill={spec.color} />
          </AreaChart>
        ) : (
          <LineChart data={spec.data}>
            {commonAxes}
            <Line type="monotone" dataKey={spec.yKey} stroke={spec.color} strokeWidth={2} dot={false} />
          </LineChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}

/***********************************
 * Message Bubble
 ***********************************/
function MessageBubble({ m, onTogglePin }: { m: Message; onTogglePin?: (artifactId: string) => void }) {
  const isUser = m.role === "user";
  const status = m.state ?? "sent";
  return (
    <motion.div
      className={cn("flex gap-3", isUser ? "justify-end" : "justify-start")}
      data-testid="message-item"
      initial={isUser ? { opacity: 0, y: 8 } : undefined}
      animate={isUser ? { opacity: 1, y: 0 } : undefined}
      transition={{ duration: 0.2 }}
    >
      {!isUser && (
        <Avatar className="h-8 w-8 mt-1">
          <AvatarImage src="https://avatar.vercel.sh/agent" alt="Agent" />
          <AvatarFallback>AG</AvatarFallback>
        </Avatar>
      )}
      <div className={cn("max-w-[720px] w-full flex flex-col", isUser && "items-end")}>
        <div
          className={cn(
            "relative rounded-2xl p-4 border before:absolute before:content-[''] before:-bottom-1 before:h-3 before:w-3 before:bg-inherit before:rotate-45",
            isUser
              ? "bg-gradient-to-br from-[var(--message-user-from)] to-[var(--message-user-to)] text-primary-foreground before:right-3"
              : "bg-gradient-to-br from-[var(--message-agent-from)] to-[var(--message-agent-to)] text-card-foreground border-border/60 before:left-3",
          )}
        >
          <div className="prose dark:prose-invert max-w-none text-[15px] leading-7">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.text}</ReactMarkdown>
          </div>
        </div>
        {m.artifacts?.length ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3 mt-3">
            {m.artifacts.map((a) => (
              <ArtifactPreview key={a.id} artifact={a} onTogglePin={onTogglePin} />
            ))}
          </div>
        ) : null}
        <div
          className={cn(
            "text-[11px] text-muted-foreground mt-2 flex items-center gap-1",
            isUser && "justify-end",
          )}
        >
          {m.createdAt}
          {isUser && (
            status === "read" ? (
              <CheckCheck className="h-3 w-3 text-[var(--message-read)]" />
            ) : (
              <Check className="h-3 w-3 text-[var(--message-sent)]" />
            )
          )}
        </div>
      </div>
      {isUser && (
        <Avatar className="h-8 w-8 mt-1">
          <AvatarImage src="https://avatar.vercel.sh/user" alt="User" />
          <AvatarFallback>U</AvatarFallback>
        </Avatar>
      )}
    </motion.div>
  );
}

/***********************************
 * Typing indicator
 ***********************************/
function TypingIndicator({ active }: { active: boolean }) {
  const [visible, setVisible] = React.useState(active);
  useEffect(() => {
    if (active) setVisible(true);
    else {
      const t = setTimeout(() => setVisible(false), 200);
      return () => clearTimeout(t);
    }
  }, [active]);
  if (!visible) return null;
  return (
    <div
      className={cn(
        "mx-auto w-full max-w-[920px] pb-6 transition-opacity duration-200",
        active ? "opacity-100" : "opacity-0"
      )}
    >
      <div className="flex gap-3">
        <Avatar className="h-8 w-8 mt-1">
          <AvatarImage src="https://avatar.vercel.sh/agent" alt="Agent" />
          <AvatarFallback>AG</AvatarFallback>
        </Avatar>
        <div className="rounded-2xl p-4 border bg-gradient-to-br from-[var(--message-agent-from)] to-[var(--message-agent-to)] text-card-foreground border-border/60">
          <Loader2 className="h-4 w-4 animate-spin" />
        </div>
      </div>
    </div>
  );
}

/***********************************
 * Composer
 ***********************************/
function Composer({ value, onChange, onSend, textareaRef, onPickFiles, picked, onRemovePicked, uploading, onRetryUpload, uploadError }: {
  value: string;
  onChange: (v: string) => void;
  onSend: () => void;
  textareaRef?: React.RefObject<HTMLTextAreaElement | null>;
  onPickFiles: (files: FileList | null) => void;
  picked: Array<{ id: string; name: string; size: number }>;
  onRemovePicked: (id: string) => void;
  uploading?: boolean;
  onRetryUpload?: () => void;
  uploadError?: string | null;
}) {
  const inputRef = React.useRef<HTMLInputElement>(null);
  return (
    <div className="sticky bottom-0 bg-gradient-to-t from-background via-background/95 to-background/0">
      <div className="mx-auto max-w-[920px] px-4 pb-4">
        <div className="rounded-2xl border bg-background shadow-sm">
          <Textarea
            ref={textareaRef}
            placeholder="Message Discovery Agent…"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={(e) => {
              if ((e.metaKey || e.ctrlKey) && e.key === "Enter") onSend();
            }}
            className="min-h-[72px] resize-none border-0 focus-visible:ring-0"
          />
          <div className="px-3 pt-1 text-[11px] text-muted-foreground text-right">Shift+Enter for newline</div>
          {picked.length > 0 && (
            <div className="px-3 pb-2 flex flex-wrap gap-2">
              {picked.map((f) => (
                <div key={f.id} className="flex items-center gap-2 px-2 py-1 rounded-full bg-muted text-xs">
                  <span className="truncate max-w-[200px]">{f.name}</span>
                  <span className="text-muted-foreground">({Math.ceil(f.size/1024)} KB)</span>
                  <button aria-label={`Remove ${f.name}`} onClick={() => onRemovePicked(f.id)} className="text-muted-foreground hover:text-foreground">×</button>
                </div>
              ))}
              {uploading && <span className="text-xs text-muted-foreground">Uploading…</span>}
              {uploadError && (
                <div className="flex items-center gap-2 text-xs text-red-500">
                  <span>{uploadError}</span>
                  {onRetryUpload && <button onClick={onRetryUpload} className="underline">Retry</button>}
                </div>
              )}
            </div>
          )}
          <div className="flex items-center justify-between px-2 pb-2">
            <div className="flex items-center gap-2">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon" onClick={() => inputRef.current?.click()} aria-label="Attach file"><Paperclip className="h-4 w-4" /></Button>
                </TooltipTrigger>
                <TooltipContent side="top" className="pointer-events-none select-none">Attach file</TooltipContent>
              </Tooltip>
              <input
                ref={inputRef}
                type="file"
                multiple
                className="hidden"
                accept=".pdf,.doc,.docx,.rtf,.txt,.md,.csv,.xls,.xlsx,.json,.yaml,.yml,.xml,.zip,.ppt,.pptx,.js,.ts,.tsx,.jsx,.mjs,.cjs,.py,.java,.cs,.rb,.go,.rs,.c,.cpp,.h,.hpp,.sh,.bash,.zsh,.ps1,.toml,.ini,.cfg,.conf,.sql"
                onChange={(e) => onPickFiles(e.target.files)}
              />
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
  const composerRef = useRef<HTMLTextAreaElement>(null);
  const [picked, setPicked] = useState<Array<{ id: string; file: File }>>([]);
  const [uploaded, setUploaded] = useState<Array<{ id: string; title: string; uri: string; mime?: string; size?: number }>>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const [chats, setChats] = useState<Chat[]>([]);
  const [selectedChatId, setSelectedChatId] = useState<string | undefined>();
  const [loadingChats, setLoadingChats] = useState(false);
  const [artifactsOpen, setArtifactsOpen] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [agentTyping, setAgentTyping] = useState(false);

  // Virtualization state for the thread
  const threadScrollRef = useRef<HTMLDivElement | null>(null);
  const threadContainerRef = useRef<HTMLDivElement | null>(null);
  const [autoScroll, setAutoScroll] = useState(true);
  const rowVirtualizer = useVirtualizer({
    count: messages.length,
    getScrollElement: () => threadScrollRef.current,
    estimateSize: () => 140,
    overscan: 6,
    getItemKey: (index) => messages[index]?.id ?? index,
    scrollToFn: elementScroll,
  });

  // Keep autoscroll at bottom when new messages arrive unless user scrolled up
  useEffect(() => {
    if (!autoScroll) return;
    const lastIndex = messages.length - 1;
    if (lastIndex >= 0) {
      // Defer to next frame to ensure measurements
      requestAnimationFrame(() => rowVirtualizer.scrollToIndex(lastIndex, { align: "end" }));
    }
  }, [messages.length, autoScroll, rowVirtualizer]);

  useEffect(() => {
    if (agentTyping && autoScroll) {
      requestAnimationFrame(() => threadScrollRef.current?.scrollTo({ top: threadScrollRef.current.scrollHeight }));
    }
  }, [agentTyping, autoScroll]);

  // Track whether user is near bottom
  useEffect(() => {
    const el = threadScrollRef.current;
    if (!el) return;
    const onScroll = () => {
      const threshold = 24; // px from bottom to consider sticky
      const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight <= threshold;
      setAutoScroll(atBottom);
    };
    el.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    return () => el.removeEventListener("scroll", onScroll as EventListener);
  }, []);

  // restore last selected chat id from localStorage
  useEffect(() => {
    try {
      const last = localStorage.getItem("discovery:lastChatId");
      if (last) setSelectedChatId(last);
    } catch {}
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // pick chat from URL query if provided (e.g., /?chatId=123)
  useEffect(() => {
    try {
      const qs = new URLSearchParams(window.location.search);
      const cid = qs.get("chatId");
      if (cid) setSelectedChatId(cid);
    } catch {}
  }, []);

  useEffect(() => {
    if (selectedChatId) {
      try { localStorage.setItem("discovery:lastChatId", selectedChatId); } catch {}
    }
  }, [selectedChatId]);

  const handleNewChat = () => {
    const id = `local-${Date.now()}`;
    const now = new Date().toISOString();
    const newChat: Chat = { id, title: "New chat", lastActivity: now };
    setChats((prev) => [newChat, ...prev]);
    setSelectedChatId(id);
    // focus composer shortly after
    setTimeout(() => composerRef.current?.focus(), 0);
    // Try to persist to backend
    if (provider.createChat) {
      const ac = new AbortController();
      provider.createChat({ title: newChat.title }, ac.signal).then((serverChat: Chat | null) => {
        if (serverChat) {
          setChats((prev) => {
            // Replace the local temp chat with the server chat by id
            const replaced = prev.map((c) => (c.id === id ? serverChat : c));
            // If temp chat moved, ensure server chat is selected
            return replaced;
          });
          setSelectedChatId(serverChat.id);
        }
      }).catch(() => {/* ignore */});
    }
  };

  // listen for global events to start new chat or focus composer
  useEffect(() => {
    const onNew = () => handleNewChat();
    const onFocus = () => composerRef.current?.focus();
    window.addEventListener("discovery:new-chat", onNew as EventListener);
    window.addEventListener("discovery:focus-composer", onFocus as EventListener);
    return () => {
      window.removeEventListener("discovery:new-chat", onNew as EventListener);
      window.removeEventListener("discovery:focus-composer", onFocus as EventListener);
    };
  }, []);

  // load chats
  React.useEffect(() => {
    const ac = new AbortController();
    let mounted = true;
    setLoadingChats(true);
    provider.listChats(ac.signal)
      .then((list) => { if (mounted) setChats(list); })
  .catch((e: unknown) => { const name = (e as { name?: string } | null)?.name; if (name !== "AbortError") { /* ignore */ } })
      .finally(() => { if (mounted) setLoadingChats(false); });
    return () => { mounted = false; ac.abort(); };
  }, [provider]);

  // choose initial chat when chats load
  React.useEffect(() => {
    if (!selectedChatId && chats[0]?.id) setSelectedChatId(chats[0].id);
  }, [chats, selectedChatId]);

  // load messages when a chat is selected
  React.useEffect(() => {
    if (!selectedChatId) return;
    const ac = new AbortController();
    let mounted = true;
    provider.listMessages(selectedChatId, ac.signal)
      .then((list) => { if (mounted) setMessages(list); })
  .catch((e: unknown) => { const name = (e as { name?: string } | null)?.name; if (name !== "AbortError") { /* ignore */ } });
    return () => { mounted = false; ac.abort(); };
  }, [selectedChatId, provider]);

  const onSend = () => {
    if (!composer.trim()) return;
    const now = new Date().toLocaleTimeString();
    const newMsg: Message = {
      id: String(Date.now()),
      role: "user",
      text: composer,
      createdAt: now,
      artifacts: uploaded.map((u) => ({ id: u.id, type: "file", title: u.title, uri: u.uri }))
    };
    setMessages((prev) => [...prev, newMsg]);
    setComposer("");
    setPicked([]);
    setUploaded([]);
    setUploadError(null);
    setAgentTyping(true);
    const ac = new AbortController();
    provider
      .sendMessage({ chatId: selectedChatId || "demo", text: newMsg.text, attachments: uploaded }, ac.signal)
      .then(() => {
        if (!selectedChatId) return;
        return provider.listMessages(selectedChatId).then((list) => setMessages(list));
      })
      .catch(() => { /* ignore demo errors */ })
      .finally(() => setAgentTyping(false));
  // Ensure we stick to bottom on send
  setAutoScroll(true);
  };

  const handlePickFiles = (files: FileList | null) => {
    if (!files || files.length === 0) return;
    const arr = Array.from(files);
    // Block audio/video types for enterprise context
    const blocked = arr.filter((f) => (f.type?.startsWith("audio/") || f.type?.startsWith("video/")));
    const allowed = arr.filter((f) => !(f.type?.startsWith("audio/") || f.type?.startsWith("video/")));
    if (blocked.length) {
      setUploadError("Some files were blocked (audio/video not allowed).");
    }
    const next = allowed.map((f) => ({ id: `${f.name}-${f.size}-${Date.now()}-${Math.random().toString(36).slice(2)}`, file: f }));
    setPicked((prev) => [...prev, ...next]);
  };

  useEffect(() => {
    if (!picked.length || !provider.uploadFiles) return;
    let cancelled = false;
    const ac = new AbortController();
    (async () => {
      setUploading(true);
      setUploadError(null);
      try {
  const uploadFn = provider.uploadFiles;
  if (!uploadFn) return;
  const res = await uploadFn(picked.map((p) => p.file), ac.signal);
        if (!cancelled) setUploaded(res);
      } catch (e: unknown) {
        const name = (e as { name?: string } | null)?.name;
        if (!cancelled && name !== "AbortError") setUploadError("Failed to upload files");
      } finally {
        if (!cancelled) setUploading(false);
      }
    })();
    return () => { cancelled = true; ac.abort(); };
  }, [picked, provider]);

  const handleRemovePicked = (id: string) => {
    setPicked((prev) => prev.filter((p) => p.id !== id));
    // if removing, clear uploaded results so we don't send removed ones
    setUploaded([]);
  };

  // Keyboard shortcuts
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const isMeta = e.metaKey || (e.ctrlKey && navigator.platform.indexOf("Mac") === -1);
      // Cmd+N: new chat
      if (isMeta && !e.shiftKey && !e.altKey && e.key.toLowerCase() === "n") {
        e.preventDefault();
        handleNewChat();
        return;
      }
      // Cmd+K: focus chat search
      if (isMeta && !e.shiftKey && !e.altKey && e.key.toLowerCase() === "k") {
        e.preventDefault();
        try { window.dispatchEvent(new Event("discovery:focus-chat-search")); } catch {}
        return;
      }
      // Cmd+/ : toggle sidebar
      if (isMeta && !e.shiftKey && !e.altKey && e.key === "/") {
        e.preventDefault();
        setCollapsed((v) => !v);
        return;
      }
      // Cmd+Shift+A: toggle artifacts panel
      if (isMeta && e.shiftKey && !e.altKey && e.key.toLowerCase() === "a") {
        e.preventDefault();
        setArtifactsOpen((v) => !v);
        return;
      }
      // Esc: blur active element
      if (!isMeta && !e.shiftKey && !e.altKey && e.key === "Escape") {
        const el = document.activeElement as HTMLElement | null;
        if (el && typeof el.blur === "function") el.blur();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const selectedChat = useMemo(() => chats.find((c) => c.id === selectedChatId), [chats, selectedChatId]);
  const allArtifacts = useMemo(() => messages.flatMap(m => m.artifacts ?? []), [messages]);

  const handleTogglePin = (artifactId: string) => {
    // optimistic local toggle
    setMessages((prev) => prev.map((m) => ({
      ...m,
      artifacts: m.artifacts?.map((a) => a.id === artifactId ? { ...a, pinned: !a.pinned } : a)
    })));
    // best-effort server call
    if (provider.togglePin && selectedChatId) {
      const ac = new AbortController();
      provider.togglePin({ chatId: selectedChatId, artifactId }, ac.signal).catch(() => {/* ignore */});
    }
  };

  const handleDeleteChat = (id: string) => {
    setChats((prev) => prev.filter((c) => c.id !== id));
    if (selectedChatId === id) {
      // pick next available chat
      const next = chats.find((c) => c.id !== id)?.id;
      setSelectedChatId(next);
      if (!next) setMessages([]);
    }
    if (provider.deleteChat) {
      const ac = new AbortController();
      provider.deleteChat(id, ac.signal).catch(() => { /* ignore */ });
    }
  };

  return (
    <TooltipProvider>
      <div
        className="h-screen w-full grid bg-background text-foreground grid-cols-1 lg:[grid-template-columns:var(--sidebar)_1fr_var(--artifacts)]"
        style={{
          "--sidebar": collapsed ? "64px" : "260px",
          "--artifacts": artifactsOpen ? "420px" : "0px",
        } as React.CSSProperties}
      >
        {/* LEFT COLUMN: sidebar */}
        <div className="min-w-0 hidden lg:block">
          <Sidebar
            chats={chats}
            selectedId={selectedChatId}
            onSelect={setSelectedChatId}
            onNew={handleNewChat}
            onDelete={handleDeleteChat}
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
              <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
                <SheetTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="lg:hidden"
                    aria-label="Open sidebar"
                  >
                    <Menu className="h-4 w-4" />
                  </Button>
                </SheetTrigger>
                <SheetContent side="left" className="p-0 w-[260px] lg:hidden">
                  <Sidebar
                    chats={chats}
                    selectedId={selectedChatId}
                    onSelect={(id) => { setSelectedChatId(id); setSidebarOpen(false); }}
                    onNew={handleNewChat}
                    onDelete={handleDeleteChat}
                    collapsed={false}
                    setCollapsed={() => setSidebarOpen(false)}
                    isLoading={loadingChats}
                  />
                </SheetContent>
              </Sheet>
              {selectedChat?.title ? (
                <div className="text-base font-semibold truncate max-w-[60vw]">{selectedChat.title}</div>
              ) : null}
            </div>
            <div className="flex items-center gap-2">
              <Sheet open={artifactsOpen} onOpenChange={setArtifactsOpen}>
                <SheetTrigger asChild>
                  <Button
                    variant="outline"
                    size="sm"
                    className="relative"
                  >
                    Artifacts
                    {allArtifacts.length > 0 && (
                      <span className="ml-2 inline-flex h-5 min-w-[20px] items-center justify-center rounded-full bg-primary text-primary-foreground px-1 text-[10px] font-medium">
                        {allArtifacts.length}
                      </span>
                    )}
                  </Button>
                </SheetTrigger>
                <SheetContent side="right" className="p-0 w-[420px] lg:hidden">
                  <div className="h-14 border-b flex items-center px-4 font-semibold">Artifacts</div>
                  <ScrollArea className="h-[calc(100vh-3.5rem)] p-3">
                    <div className="grid grid-cols-1 gap-3">
                      {allArtifacts.length ? (
                        allArtifacts.map((a) => <ArtifactPreview key={a.id} artifact={a} onTogglePin={handleTogglePin} />)
                      ) : (
                        <div className="text-sm text-muted-foreground p-6 text-center">No artifacts yet</div>
                      )}
                    </div>
                  </ScrollArea>
                </SheetContent>
              </Sheet>
              <Avatar>
                <AvatarImage src="https://avatar.vercel.sh/user" alt="User" />
                <AvatarFallback>U</AvatarFallback>
              </Avatar>
            </div>
          </div>

          {/* Thread (virtualized) */}
          <ScrollArea className="flex-1 p-4" ref={threadScrollRef} data-testid="thread-scroll">
            {/* When virtualization is active */}
            {rowVirtualizer.getVirtualItems().length > 0 ? (
              <div ref={threadContainerRef} className="mx-auto w-full max-w-[920px]" style={{ height: rowVirtualizer.getTotalSize(), position: "relative" }}>
                {(function() {
                  // Cap extreme cases where the virtualizer may return an unexpectedly large set before measuring
                  const items = rowVirtualizer.getVirtualItems();
                  const bounded = items.length > 80 ? items.slice(0, 80) : items;
                  return bounded;
                })().map((item) => {
                  const m = messages[item.index];
                  if (!m) return null;
                  return (
                    <div
                      key={item.key}
                      data-index={item.index}
                      ref={rowVirtualizer.measureElement}
                      style={{ position: "absolute", top: 0, left: 0, width: "100%", transform: `translateY(${item.start}px)` }}
                    >
                      <div className="pb-6">
                        <MessageBubble m={m} onTogglePin={handleTogglePin} />
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              // Fallback: render last 20 messages without virtualization (e.g., tests)
              <div className="mx-auto w-full max-w-[920px] space-y-6">
                {getFallbackVirtualItems(messages.length, 20).map((fi) => {
                  const m = messages[fi.index];
                  return m ? <MessageBubble key={m.id} m={m} onTogglePin={handleTogglePin} /> : null;
                })}
              </div>
            )}
            <TypingIndicator active={agentTyping} />
          </ScrollArea>

          {/* Composer */}
          <Composer
            value={composer}
            onChange={setComposer}
            onSend={onSend}
            textareaRef={composerRef}
            onPickFiles={handlePickFiles}
            picked={picked.map((p) => ({ id: p.id, name: p.file.name, size: p.file.size }))}
            onRemovePicked={handleRemovePicked}
            uploading={uploading}
            onRetryUpload={() => setPicked((p) => [...p])}
            uploadError={uploadError}
          />
        </div>

        {/* RIGHT COLUMN: artifacts inline */}
        <div
          className="border-l overflow-hidden transition-[width] duration-200 ease-out hidden lg:block"
          style={{ width: artifactsOpen ? "420px" : "0px" }}
        >
          <div className="h-14 border-b flex items-center px-4 font-semibold">Artifacts</div>
          <ScrollArea className="h-[calc(100vh-3.5rem)] p-3">
            <div className="grid grid-cols-1 gap-3">
              {allArtifacts.length ? (
                allArtifacts.map((a) => <ArtifactPreview key={a.id} artifact={a} onTogglePin={handleTogglePin} />)
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
