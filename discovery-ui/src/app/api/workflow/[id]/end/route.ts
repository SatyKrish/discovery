import { NextResponse } from "next/server";

export async function POST(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const { id } = await ctx.params;
  const dest = `${base}/workflow/${encodeURIComponent(id)}/end`;
  const res = await fetch(dest, { method: "POST" });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
