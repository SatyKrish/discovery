import { NextResponse } from "next/server";

export async function POST(req: Request, ctx: { params: Promise<{ id: string }> }) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const { id } = await ctx.params;
  const body = await req.json().catch(() => ({}));
  const dest = `${base}/chat/confirm`;
  const res = await fetch(dest, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      workflow_id: id,
      tool_call_id: body.tool_call_id,
      approved: body.approved,
      args: body.custom_args
    })
  });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
