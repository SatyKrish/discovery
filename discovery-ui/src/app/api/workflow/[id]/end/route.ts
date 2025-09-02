import { NextResponse } from "next/server";

export async function POST(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const { id } = await ctx.params;
  const dest = `${base}/chat/end`;
  const res = await fetch(dest, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ workflow_id: id })
  });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
