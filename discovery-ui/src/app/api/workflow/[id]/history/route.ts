import { NextResponse } from "next/server";

export async function GET(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const { id } = await ctx.params;
  const dest = `${base}/sessions/${encodeURIComponent(id)}/history`;
  const res = await fetch(dest, { method: "GET" });
  const data = await res.json().catch(() => ([]));

  // Transform backend response to match frontend expectations
  const messages = Array.isArray(data) ? data.map((msg: any) => ({
    role: msg.role === 'user' ? 'user' : 'agent',
    content: msg.content || '',
    timestamp: msg.ts || new Date().toISOString()
  })) : [];

  return NextResponse.json({ history: messages }, { status: res.status });
}
