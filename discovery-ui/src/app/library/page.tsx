"use client";
import React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { buttonVariants, Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { Artifact } from "@/lib/provider";
import type { ArtifactType } from "@/lib/provider";
import { HttpProvider } from "@/lib/provider";
import { Image as ImageIcon, Pin, Copy, ExternalLink } from "lucide-react";

type Filter = {
  view: "pinned" | "recent";
  type: "all" | "file" | "table.json" | "chart.vegaLite" | "chart.recharts";
};

export default function LibraryPage() {
  const router = useRouter();
  const [filter, setFilter] = React.useState<Filter>({ view: "pinned", type: "all" });
  const [loading, setLoading] = React.useState(false);
  const [items, setItems] = React.useState<Artifact[]>([]);
  const [error, setError] = React.useState<string | null>(null);

  const load = React.useCallback(async (signal?: AbortSignal) => {
    setLoading(true);
    setError(null);
    try {
      const typeParam: ArtifactType | undefined = filter.type === "all" ? undefined : (filter.type as ArtifactType);
      const params: Parameters<NonNullable<typeof HttpProvider.listArtifacts>>[0] = {
        filter: filter.view,
        type: typeParam,
      };
      const list = (await HttpProvider.listArtifacts?.(params, signal)) ?? [];
      setItems(list);
    } catch (e: unknown) {
      const message = (e as { message?: string } | null)?.message || "Failed to load";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  React.useEffect(() => {
    const ac = new AbortController();
    load(ac.signal);
    return () => ac.abort();
  }, [load]);

  const onUnpin = async (a: Artifact) => {
    try {
      await HttpProvider.togglePin?.({ chatId: a.chatId ?? "", artifactId: a.id });
      setItems((prev) => prev.map((x) => (x.id === a.id ? { ...x, pinned: !x.pinned } : x)));
    } catch { /* ignore */ }
  };

  const onCopy = async (text: string) => {
    try { await navigator.clipboard.writeText(text); } catch { /* ignore */ }
  };

  const filtered = React.useMemo(() => {
    return items.filter((i) => filter.type === "all" ? true : i.type === filter.type);
  }, [items, filter]);

  return (
    <main className="min-h-dvh p-6">
      <div className="mx-auto max-w-6xl">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-semibold flex items-center gap-2">
            <ImageIcon className="h-6 w-6" /> Library
          </h1>
          <Link href="/" className={cn(buttonVariants({ variant: "outline" }))}>Back to chat</Link>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-2 mb-4">
          <div className="inline-flex items-center gap-1 rounded-lg border p-1 bg-background">
            {(["pinned", "recent"] as const).map((v) => (
              <button
                key={v}
                onClick={() => setFilter((f) => ({ ...f, view: v }))}
                className={cn(
                  "px-3 py-1.5 text-sm rounded-md",
                  filter.view === v ? "bg-primary text-primary-foreground" : "hover:bg-muted"
                )}
                aria-pressed={filter.view === v}
              >
                {v[0].toUpperCase() + v.slice(1)}
              </button>
            ))}
          </div>
          <div className="inline-flex items-center gap-1 rounded-lg border p-1 bg-background">
            {(["all", "file", "table.json", "chart.vegaLite", "chart.recharts"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setFilter((f) => ({ ...f, type: t }))}
                className={cn(
                  "px-3 py-1.5 text-sm rounded-md",
                  filter.type === t ? "bg-secondary" : "hover:bg-muted"
                )}
                aria-pressed={filter.type === t}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-44 rounded-xl border bg-muted animate-pulse" />
            ))}
          </div>
        ) : error ? (
          <div className="rounded-xl border p-6 text-sm text-red-500">{error}</div>
        ) : filtered.length === 0 ? (
          <div className="rounded-xl border p-10 text-center text-sm text-muted-foreground">
            No {filter.view} items{filter.type !== "all" ? ` for type ${filter.type}` : ""}.
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map((a) => (
              <Card key={a.id} className="rounded-2xl border-border/60">
                <CardHeader className="p-4 pb-2">
                  <CardTitle className="text-sm font-semibold truncate">{a.title}</CardTitle>
                  <div className="text-xs text-muted-foreground flex items-center gap-2">
                    <Badge variant="secondary" className="bg-muted text-foreground">{a.type}</Badge>
                    {a.pinned ? <Badge className="gap-1" variant="secondary"><Pin className="h-3 w-3" /> pinned</Badge> : null}
                  </div>
                </CardHeader>
                <CardContent className="p-4 pt-0">
                  {a.uri ? (
                    <div className="text-xs text-muted-foreground truncate">{a.uri}</div>
                  ) : (
                    <div className="text-xs text-muted-foreground">No URI</div>
                  )}
                </CardContent>
                <CardFooter className="p-4 pt-0 flex gap-2">
                  <Button size="sm" variant="outline" onClick={() => router.push(`/?chatId=${encodeURIComponent(a.chatId ?? "")}`)}>
                    <ExternalLink className="h-4 w-4 mr-1" /> Open in chat
                  </Button>
                  <Button size="sm" variant="ghost" onClick={() => onUnpin(a)}>
                    <Pin className={cn("h-4 w-4 mr-1", a.pinned && "text-primary")} /> {a.pinned ? "Unpin" : "Pin"}
                  </Button>
                  {a.uri && (
                    <Button size="sm" variant="ghost" onClick={() => onCopy(a.uri!)}>
                      <Copy className="h-4 w-4 mr-1" /> Copy link
                    </Button>
                  )}
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
