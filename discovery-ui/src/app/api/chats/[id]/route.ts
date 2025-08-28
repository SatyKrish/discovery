import { NextRequest, NextResponse } from "next/server";

export async function DELETE(_req: NextRequest, ctx: { params: Promise<{ id: string }> }) {
  const { id } = await ctx.params;
  const dest = `/api/workflow/${encodeURIComponent(id)}/end`;
  const res = await fetch(dest, { method: "POST" });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
