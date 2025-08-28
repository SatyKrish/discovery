import { NextRequest, NextResponse } from "next/server";

export async function DELETE(_req: NextRequest, ctx: { params: Promise<{ id: string }> }) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const { id } = await ctx.params;
  const dest = `${base}/chats/${encodeURIComponent(id)}`;
  const res = await fetch(dest, { method: "DELETE" });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
