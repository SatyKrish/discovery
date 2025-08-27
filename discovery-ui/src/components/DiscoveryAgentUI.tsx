'use client';
import React, { useEffect, useMemo, useRef, useState, useCallback } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Checkbox } from "@/components/ui/checkbox";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Highlight, themes } from "prism-react-renderer";
import {
  Send,
  Paperclip,
  MoreVertical,
  BarChart3,
  Table2,
  FileDown,
  ChevronRight,
  Search,
  Pin as PinIcon,
  ExternalLink,
  Plus,
  Sun,
  Moon,
  AlertTriangle,
  Menu,
  Copy as CopyIcon,
  Check as CheckIcon,
  RotateCw,
  Square,
} from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
} from "recharts";

/***********************************
 * HEADLESS TYPES & CONTRACTS
 ***********************************/
export type Role = "user" | "agent" | "tool";

export type Artifact = {
  id: string;
  type: "chart.vegaLite" | "table.json" | "file";
  title: string;
  uri?: string;
  json?: unknown;
  meta?: Record<string, unknown>;
  pinned?: boolean;
};

export type Message = {
  id: string;
  role: Role;
  text: string;
  artifacts?: Artifact[];
  createdAt: string;
};

export type Chat = {
  id: string;
  title: string;
  tags?: string[];
  lastActivity?: string;
};

export interface DiscoveryAgentDataProvider {
  listChats(signal?: AbortSignal): Promise<Chat[]>;
  listMessages(chatId: string, signal?: AbortSignal): Promise<Message[]>;
  sendMessage(params: { chatId: string; text: string; pinNext?: boolean }, signal?: AbortSignal): Promise<void>;
  togglePin(params: { chatId: string; artifactId: string }, signal?: AbortSignal): Promise<void>;
}

/***********************************
 * PROVIDER GUARD & SAFE DEFAULTS
 ***********************************/
export const NoopProvider: DiscoveryAgentDataProvider = {
  async listChats() { if (typeof window !== "undefined") console.warn("[DiscoveryAgentUI] No provider supplied: listChats() returning []"); return []; },
  async listMessages() { if (typeof window !== "undefined") console.warn("[DiscoveryAgentUI] No provider supplied: listMessages() returning []"); return []; },
  async sendMessage() { if (typeof window !== "undefined") console.warn("[DiscoveryAgentUI] No provider supplied: sendMessage() ignored"); await new Promise((r)=>setTimeout(r,800)); },
  async togglePin() { if (typeof window !== "undefined") console.warn("[DiscoveryAgentUI] No provider supplied: togglePin() ignored"); },
};

function isValidProvider(p: unknown): p is DiscoveryAgentDataProvider {
  return (
    !!p &&
    ["listChats", "listMessages", "sendMessage", "togglePin"].every(
      (m) => typeof (p as Record<string, unknown>)[m] === "function"
    )
  );
}

/***********************************
 * THEME-AWARE PRIMITIVES
 ***********************************/
function ThemedLineChart({ data, height = "100%" }: { data: unknown[]; height?: number | string }) {
  const axisStroke = "hsl(var(--muted-foreground))";
  const gridStroke = "hsl(var(--border))";
  const lineStroke = "hsl(var(--foreground))";
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 10, right: 16, bottom: 10, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
        <XAxis dataKey="name" stroke={axisStroke} tick={{ fill: axisStroke }} />
        <YAxis stroke={axisStroke} tick={{ fill: axisStroke }} />
        <RechartsTooltip
          contentStyle={{ background: "hsl(var(--popover))", color: "hsl(var(--popover-foreground))", border: "1px solid hsl(var(--border))", borderRadius: 12 }}
          labelStyle={{ color: "hsl(var(--popover-foreground))" }}
          itemStyle={{ color: "hsl(var(--popover-foreground))" }}
        />
        <Line type="monotone" dataKey="value" stroke={lineStroke} strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}

/***********************************
 * PRESENTATIONAL COMPONENTS
 ***********************************/
function EmptyState({ title, subtitle, action }: { title: string; subtitle?: string; action?: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 gap-2 text-muted-foreground">
      <div className="text-lg font-medium text-foreground/90">{title}</div>
      {subtitle && <div className="text-sm">{subtitle}</div>}
      {action}
    </div>
  );
}

function InlineWarning({ message }: { message: string }) {
  return (
    <div className="mx-4 my-2 flex items-center gap-2 rounded-md border border-yellow-500/40 bg-yellow-500/10 p-2 text-yellow-600 dark:text-yellow-400">
      <AlertTriangle className="h-4 w-4" />
      <span className="text-xs">{message}</span>
    </div>
  );
}

function LoadingRows({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-2">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="h-9 w-full rounded-md bg-muted animate-pulse" />
      ))}
    </div>
  );
}

/***********************
 * Markdown Renderer
 ***********************/
function CodeBlock({ code, language }: { code: string; language?: string }) {
  const [copied, setCopied] = useState(false);
  const onCopy = async () => {
    try { await navigator.clipboard.writeText(code); setCopied(true); setTimeout(()=>setCopied(false), 1200);} catch {}
  };
  return (
    <div className="relative group border rounded-xl overflow-hidden">
      <div className="absolute right-2 top-2 z-10">
        <Button size="icon" variant="secondary" className="h-7 w-7" onClick={onCopy} aria-label="Copy code">
          {copied ? <CheckIcon className="h-4 w-4"/> : <CopyIcon className="h-4 w-4"/>}
        </Button>
      </div>
      <Highlight theme={themes.oneDark} code={code} language={language ?? "tsx"}>
        {({ className, style, tokens, getLineProps, getTokenProps }) => (
          <pre className={cn(className, "p-4 overflow-auto text-sm leading-6 bg-muted/60") } style={style}>
            {tokens.map((line, i) => (
              <div key={i} {...getLineProps({ line })}>
                {line.map((token, key) => (
                  <span key={key} {...getTokenProps({ token })} />
                ))}
              </div>
            ))}
          </pre>
        )}
      </Highlight>
    </div>
  );
}

function MarkdownMessage({ children }: { children: string }) {
  return (
    <div className="prose prose-zinc dark:prose-invert max-w-none prose-code:before:content-none prose-code:after:content-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{
          code({ inline, className, children: c }: { inline?: boolean; className?: string; children?: React.ReactNode }) {
            const match = /language-(\w+)/.exec(className || "");
            const code = String(c).replace(/\n$/, "");
            if (inline) {
              return <code className="px-1.5 py-0.5 rounded-md bg-muted text-foreground text-[13px]">{code}</code>;
            }
            return <CodeBlock code={code} language={match?.[1]} />;
          },
          table({ children }) {
            return <div className="w-full overflow-x-auto"><table className="w-full text-sm border-collapse">{children}</table></div>;
          },
          th({ children }) { return <th className="border-b text-left px-2 py-1">{children}</th>; },
          td({ children }) { return <td className="border-b px-2 py-1 align-top">{children}</td>; },
          a({ href, children }) {
            return <a href={href} target="_blank" rel="noreferrer" className="underline underline-offset-2">{children}</a>;
          },
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}

/***********************
 * Sidebar (ChatGPT-like)
 ***********************/
function Sidebar({
  chats,
  selectedId,
  onSelect,
  onNewChat,
  collapsed,
  setCollapsed,
  isLoading,
}: {
  chats: Chat[];
  selectedId?: string;
  onSelect: (id: string) => void;
  onNewChat: () => void;
  collapsed: boolean;
  setCollapsed: (b: boolean) => void;
  isLoading?: boolean;
}) {
  return (
    <div className={cn("h-full flex flex-col border-r bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60", collapsed ? "w-[64px]" : "w-[260px]")}> 
      <div className="px-3 py-2 flex items-center gap-2 h-14 border-b">
        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setCollapsed(!collapsed)} aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}>
          <Menu className="h-4 w-4" />
        </Button>
        {!collapsed && <div className="font-semibold truncate">Discovery Agent</div>}
      </div>

      <div className={cn("p-3", collapsed && "p-2")}> 
        {collapsed ? (
          <Tooltip>
            <TooltipTrigger asChild>
              <Button size="icon" className="w-full" onClick={onNewChat} aria-label="New chat"><Plus className="h-4 w-4" /></Button>
            </TooltipTrigger>
            <TooltipContent>New chat</TooltipContent>
          </Tooltip>
        ) : (
          <Button className="w-full justify-center" onClick={onNewChat}><Plus className="h-4 w-4 mr-2" /> New chat</Button>
        )}
      </div>

      {!collapsed && (
        <div className="px-3 pb-2">
          <div className="relative">
            <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input placeholder="Search chats" className="pl-7 h-8" />
          </div>
        </div>
      )}

      <ScrollArea className="flex-1">
        <div className={cn("px-2 pb-2 space-y-1")}> 
          {isLoading && <LoadingRows rows={6} />}
          {!isLoading && chats.length === 0 && (
            <EmptyState title={collapsed ? "" : "No chats yet"} subtitle={collapsed ? "" : "Start a new chat to see it here."} />
          )}
          {!isLoading && chats.map((c) => (
            <button key={c.id} onClick={() => onSelect(c.id)} className={cn("w-full rounded-lg border px-3 py-2 text-left hover:bg-muted/50 transition", selectedId === c.id ? "border-primary/40 bg-muted" : "border-border/60 bg-background")} title={collapsed ? c.title : undefined}>
              <div className={cn("flex items-center gap-2", collapsed && "justify-center")}> 
                <div className={cn("truncate text-sm text-foreground", collapsed && "text-center")}>{collapsed ? c.title.charAt(0).toUpperCase() : c.title}</div>
              </div>
              {!collapsed && c.lastActivity && <div className="text-[10px] text-muted-foreground mt-1">{c.lastActivity}</div>}
            </button>
          ))}
        </div>
      </ScrollArea>

      <div className="border-t p-3 flex items-center justify-between">
        {!collapsed && <span className="text-xs text-muted-foreground">v1 • Chat</span>}
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
        <TooltipContent>{dark ? "Light mode" : "Dark mode"}</TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}

/***********************
 * Artifacts & Messages
 ***********************/
function ArtifactPreview({ artifact, onExpand, onPin }: { artifact: Artifact; onExpand: (a: Artifact) => void; onPin: (id: string) => void }) {
  const renderThumb = () => {
    if (artifact.type === "chart.vegaLite") {
      const seriesData = (artifact.json as { series?: unknown[] } | undefined)?.series;
      if (!seriesData || seriesData.length === 0) return <EmptyState title="No chart data" subtitle="Agent will render series once available." />;
      return <div className="h-32"><ThemedLineChart data={seriesData} height="100%" /></div>;
    }
    if (artifact.type === "table.json") {
      const rows = Array.isArray(artifact.json)
        ? (artifact.json.slice(0, 3) as Array<Record<string, unknown>>)
        : [];
      if (rows.length === 0) return <EmptyState title="No rows" subtitle="Agent will attach table rows." />;
      return (
        <Table>
          <TableHeader>
            <TableRow>
              {Object.keys(rows[0] ?? {}).map((k) => (
                <TableHead key={k} className="text-xs text-muted-foreground text-right first:text-left">{k}</TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((r, i) => (
              <TableRow key={i}>
                {Object.values(r).map((v, j) => (
                  <TableCell key={j} className="text-xs text-foreground text-right first:text-left tabular-nums">{typeof v === "number" ? v.toLocaleString() : String(v)}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      );
    }
    return (
      <div className="h-24 flex items-center justify-center bg-muted/40 rounded-md text-sm text-foreground">
        <FileDown className="h-4 w-4 mr-2" /> {artifact.title}
      </div>
    );
  };

  return (
    <Card className="rounded-2xl shadow-sm border-border/60">
      <CardHeader className="p-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-semibold truncate text-foreground">{artifact.title}</CardTitle>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground"><MoreVertical className="h-4 w-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Artifact</DropdownMenuLabel>
              <DropdownMenuItem onClick={() => onPin(artifact.id)}><PinIcon className="h-4 w-4 mr-2" /> {artifact.pinned ? "Unpin" : "Pin"}</DropdownMenuItem>
              {artifact.uri && (
                <DropdownMenuItem>
                  <a className="flex items-center" href="#" onClick={(e) => e.preventDefault()}>
                    <ExternalLink className="h-4 w-4 mr-2" /> Open source
                  </a>
                </DropdownMenuItem>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <CardDescription className="text-xs">
          <div className="flex items-center gap-2">
            {artifact.type.startsWith("chart") && (<Badge variant="secondary" className="bg-muted text-foreground"><BarChart3 className="h-3 w-3 mr-1" /> Chart</Badge>)}
            {artifact.type === "table.json" && (<Badge variant="secondary" className="bg-muted text-foreground"><Table2 className="h-3 w-3 mr-1" /> Table</Badge>)}
            {artifact.type === "file" && (<Badge variant="secondary" className="bg-muted text-foreground"><FileDown className="h-3 w-3 mr-1" /> File</Badge>)}
          </div>
        </CardDescription>
      </CardHeader>
      <CardContent className="p-4 pt-0">{renderThumb()}</CardContent>
      <CardFooter className="p-4 pt-0 flex gap-2">
        <Button size="sm" variant="outline" onClick={() => onExpand(artifact)}>Expand</Button>
        <Button size="sm" variant="ghost" onClick={() => onPin(artifact.id)} className="text-muted-foreground"><PinIcon className="h-4 w-4 mr-1" /> {artifact.pinned ? "Unpin" : "Pin"}</Button>
      </CardFooter>
    </Card>
  );
}

function TypingDots() {
  return (
    <div className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-muted text-muted-foreground text-xs">
      <span className="animate-bounce [animation-delay:-0.2s]">•</span>
      <span className="animate-bounce">•</span>
      <span className="animate-bounce [animation-delay:0.2s]">•</span>
    </div>
  );
}

function MessageBubble({ m, onExpand, onPin, live }: { m: Message; onExpand: (a: Artifact) => void; onPin: (id: string) => void; live?: boolean }) {
  const isUser = m.role === "user";
  return (
    <div className={cn("flex gap-3", isUser ? "justify-end" : "justify-start")} aria-live={live ? "polite" : undefined}>
      {!isUser && (<Avatar className="h-8 w-8 mt-1"><AvatarFallback className="bg-muted text-foreground">A</AvatarFallback></Avatar>)}
      <div className="max-w-[760px] w-full">
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.18 }} className={cn("rounded-2xl p-4 border", isUser ? "bg-primary text-primary-foreground" : "bg-card text-card-foreground border-border/60")}> 
          <div className="text-[15px] leading-7 whitespace-pre-wrap">
            <MarkdownMessage>{m.text}</MarkdownMessage>
          </div>
        </motion.div>
        {/* artifacts grid left in for parity extension, not wired here */}
        <div className="text-[11px] text-muted-foreground mt-2">{m.createdAt}</div>
      </div>
      {isUser && (<Avatar className="h-8 w-8 mt-1"><AvatarFallback className="bg-muted text-foreground">U</AvatarFallback></Avatar>)}
    </div>
  );
}

/***********************************
 * ROOT APP (ChatGPT-like + Streaming)
 ***********************************/
export default function DiscoveryAgentUI({ provider, initialDark = true }: { provider?: DiscoveryAgentDataProvider; initialDark?: boolean }) {
  const safeProvider = useMemo(() => (isValidProvider(provider) ? (provider as DiscoveryAgentDataProvider) : NoopProvider), [provider]);
  const [dark, setDark] = useState(initialDark);
  useEffect(() => { try { const saved = typeof window !== "undefined" ? localStorage.getItem("theme") : null; if (saved === "dark" || saved === "light") setDark(saved === "dark"); } catch {} }, []);
  useEffect(() => { if (typeof document !== "undefined") { document.documentElement.classList.toggle("dark", dark); document.documentElement.setAttribute("data-theme", dark ? "dark" : "light"); try { localStorage.setItem("theme", dark ? "dark" : "light"); } catch {} } }, [dark]);

  const [collapsed, setCollapsed] = useState(false);
  const [chats, setChats] = useState<Chat[]>([]);
  const [selectedChatId, setSelectedChatId] = useState<string | undefined>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [composer, setComposer] = useState("");
  const [loadingChats, setLoadingChats] = useState(false);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [providerWarning, setProviderWarning] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [attachments, setAttachments] = useState<File[]>([]);
  const abortRef = useRef<AbortController | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => { if (safeProvider === NoopProvider) setProviderWarning("No DiscoveryAgentDataProvider was supplied. The UI will render but show no data. Pass a provider to <DiscoveryAgentUI provider={...} />."); else setProviderWarning(null); }, [safeProvider]);

  // load chats
  useEffect(() => {
    const ac = new AbortController();
    setLoadingChats(true);
    safeProvider
      .listChats(ac.signal)
      .then((list) => { setChats(list); if (!selectedChatId && list[0]?.id) setSelectedChatId(list[0].id); })
      .catch((err) => { console.error("[DiscoveryAgentUI] listChats failed:", err); setProviderWarning("Provider.listChats failed: " + (err?.message || String(err))); })
      .finally(() => setLoadingChats(false));
    return () => ac.abort();
  }, [safeProvider]);

  // load messages for selected chat
  useEffect(() => {
    if (!selectedChatId) return;
    const ac = new AbortController();
    setLoadingMessages(true);
    safeProvider
      .listMessages(selectedChatId, ac.signal)
      .then((list) => setMessages(list))
      .catch((err) => { console.error("[DiscoveryAgentUI] listMessages failed:", err); setProviderWarning("Provider.listMessages failed: " + (err?.message || String(err))); })
      .finally(() => setLoadingMessages(false));
    return () => ac.abort();
  }, [selectedChatId, safeProvider]);

  // auto-scroll on message changes
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isStreaming]);

  const latestAssistantIndex = useMemo(() => {
    for (let i = messages.length - 1; i >= 0; i--) { if (messages[i].role !== "user") return i; }
    return -1;
  }, [messages]);

  const handleStop = useCallback(() => {
    abortRef.current?.abort();
    setIsStreaming(false);
  }, []);

  const refreshMessages = useCallback((chatId: string) => {
    const ac = new AbortController();
    setLoadingMessages(true);
    safeProvider
      .listMessages(chatId, ac.signal)
      .then((list) => setMessages(list))
      .finally(() => setLoadingMessages(false));
  }, [safeProvider]);

  const onSend = useCallback(async (overrideText?: string) => {
    const text = (overrideText ?? composer).trim();
    if (!text || !selectedChatId) return;
    setComposer("");
    const ac = new AbortController();
    abortRef.current = ac;
    setIsStreaming(true);
    try {
      await safeProvider.sendMessage({ chatId: selectedChatId, text, pinNext: (document.getElementById("pin-next") as HTMLInputElement)?.checked }, ac.signal);
    } catch (err: unknown) {
      if (!(err instanceof Error) || err.name !== "AbortError") console.error("[DiscoveryAgentUI] sendMessage failed:", err);
      setProviderWarning("Provider.sendMessage failed: " + (err instanceof Error ? err.message : String(err)));
    } finally {
      setIsStreaming(false);
      refreshMessages(selectedChatId);
    }
  }, [composer, selectedChatId, safeProvider, refreshMessages]);

  const onRegenerate = useCallback(() => {
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === "user") { onSend(messages[i].text); return; }
    }
  }, [messages, onSend]);

  const onDropFiles = (e: React.DragEvent) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files || []);
    if (files.length) setAttachments((prev) => [...prev, ...files.slice(0, 5)]);
  };

  const onPaste = (e: React.ClipboardEvent<HTMLTextAreaElement>) => {
    const files: File[] = [];
    for (const item of Array.from(e.clipboardData.items)) {
      if (item.kind === "file") {
        const f = item.getAsFile();
        if (f) files.push(f);
      }
    }
    if (files.length) setAttachments((prev) => [...prev, ...files.slice(0, 5)]);
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") { e.preventDefault(); onSend(); }
  };

  const selectedChat = useMemo(() => chats.find((c) => c.id === selectedChatId), [chats, selectedChatId]);

  return (
    <TooltipProvider>
      <div className={cn("h-screen w-full grid", "bg-background text-foreground", "[--pattern-color:theme(colors.zinc.900/0.04)] dark:[--pattern-color:theme(colors.zinc.50/0.04)]", "bg-[radial-gradient(1000px_600px_at_50%_-20%,var(--pattern-color),transparent_60%)]")}> 
        {/* Left Sidebar (optional wiring; hide if you don't use chats) */}
        {/* <div className="fixed inset-y-0 left-0 z-30">
          <Sidebar chats={chats} selectedId={selectedChatId} onSelect={setSelectedChatId} onNewChat={()=>setSelectedChatId(undefined)} collapsed={false} setCollapsed={()=>{}} isLoading={loadingChats} />
        </div> */}

        {/* Main column */}
        <div className={cn("h-full w-full flex flex-col")}> 
          <div className="h-14 border-b flex items-center justify-between px-4 bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-20">
            <div className="flex items-center gap-2 min-w-0">
              <div className="text-base font-semibold truncate max-w-[60vw]">{selectedChat?.title ?? "New Chat"}</div>
              {selectedChat?.tags?.map((t) => (<Badge key={t} variant="outline" className="border-border/70">{t}</Badge>))}
            </div>
            <div className="flex items-center gap-2">
              {isStreaming ? (
                <Button size="sm" variant="outline" onClick={handleStop}><Square className="h-4 w-4 mr-1"/> Stop</Button>
              ) : (
                messages.length > 0 && <Button size="sm" variant="outline" onClick={onRegenerate}><RotateCw className="h-4 w-4 mr-1"/> Regenerate</Button>
              )}
              <Avatar><AvatarFallback className="bg-muted text-foreground">U</AvatarFallback></Avatar>
            </div>
          </div>

          {providerWarning && <InlineWarning message={providerWarning} />}

          {/* Thread */}
          <ScrollArea ref={scrollRef} className="h-[calc(100vh-11rem)] px-4">
            <div className="mx-auto w-full max-w-[920px] py-6 space-y-6">
              {loadingMessages && <LoadingRows rows={8} />}
              {!loadingMessages && messages.length === 0 && (<EmptyState title="Start the conversation." subtitle="Ask a question or paste some data." />)}
              {!loadingMessages && messages.map((m, idx) => (
                <MessageBubble key={m.id} m={m} onExpand={()=>{}} onPin={()=>{}} live={idx === latestAssistantIndex} />
              ))}
              {isStreaming && (
                <div className="flex items-center gap-2"><TypingDots /><span className="text-xs text-muted-foreground">Generating…</span></div>
              )}
            </div>
          </ScrollArea>

          {/* Composer */}
          <div className="sticky bottom-0 z-20 w-full bg-gradient-to-t from-background via-background/90 to-background/0">
            <div className="mx-auto max-w-[920px] px-4 pb-4 pt-2">
              <div className="rounded-2xl border bg-background shadow-sm" onDragOver={(e)=>e.preventDefault()} onDrop={onDropFiles}>
                <Textarea placeholder="Message Discovery Agent…" value={composer} onChange={(e) => setComposer(e.target.value)} onKeyDown={onKeyDown} onPaste={onPaste} className="min-h-[72px] max-h-[40vh] resize-y border-0 focus-visible:ring-0 placeholder:text-muted-foreground text-foreground" />
                {attachments.length > 0 && (
                  <div className="px-2 pb-2 flex flex-wrap gap-2">
                    {attachments.map((f, i) => (
                      <div key={i} className="text-[11px] px-2 py-1 rounded-full border bg-muted/50">{f.name}</div>
                    ))}
                  </div>
                )}
                <div className="flex items-center justify-between px-2 pb-2">
                  <div className="flex items-center gap-2">
                    <Tooltip><TooltipTrigger asChild><Button variant="ghost" size="icon" className="text-muted-foreground"><Paperclip className="h-4 w-4" /></Button></TooltipTrigger><TooltipContent>Attach file (drag & drop / paste)</TooltipContent></Tooltip>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground"><Checkbox id="pin-next" /><label htmlFor="pin-next">Pin next artifact</label></div>
                  </div>
                  <div className="flex items-center gap-2">
                    {isStreaming ? (
                      <Button size="sm" variant="outline" onClick={handleStop}><Square className="h-4 w-4 mr-1"/> Stop</Button>
                    ) : (
                      <Button size="sm" onClick={()=>onSend()} disabled={!composer.trim()}><Send className="h-4 w-4 mr-1" /> Send</Button>
                    )}
                  </div>
                </div>
              </div>
              <div className="text-[11px] text-muted-foreground mt-2 text-center">AI may produce inaccurate information. Verify critical outputs. • Press ⌘/Ctrl+Enter to send</div>
            </div>
          </div>
        </div>
      </div>
    </TooltipProvider>
  );
}
