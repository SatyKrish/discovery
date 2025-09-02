import { NextResponse } from "next/server";

export async function GET(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const { id } = await ctx.params;
  const dest = `${base}/sessions/${encodeURIComponent(id)}/history`;
  const res = await fetch(dest, { method: "GET" });
  const data = await res.json().catch(() => ([]));

  // Transform backend response to match frontend expectations
  const messages = Array.isArray(data) ? data.map((msg: any, index: number) => ({
    id: `msg-${index}-${Date.now()}`,
    role: msg.role === 'user' ? 'user' : 'agent',
    text: msg.content || '',
    createdAt: msg.ts ? new Date(msg.ts * 1000).toLocaleString() : new Date().toLocaleString(),
    state: msg.role === 'user' ? 'sent' : undefined
  })) : [];

  return NextResponse.json({ history: messages }, { status: res.status });
}
