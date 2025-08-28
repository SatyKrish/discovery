import { NextResponse } from "next/server";

export async function GET(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const { id } = await ctx.params;
  const dest = `${base}/workflow/${encodeURIComponent(id)}/history`;
  const res = await fetch(dest, { method: "GET" });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
