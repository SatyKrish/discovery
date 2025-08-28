import { NextResponse } from "next/server";

export async function GET(req: Request) {
  // No direct backend list endpoint; return empty list by default.
  return NextResponse.json({ chats: [] }, { status: 200 });
}

export async function POST(req: Request) {
  // Adapt to workflow start and normalize to a chat shape
  const origin = new URL(req.url).origin;
  const body = await req.json().catch(() => ({} as any));
  const question = typeof body?.title === "string" && body.title.trim() ? body.title : undefined;
  const res = await fetch(`${origin}/api/workflow/start`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ question }),
  });
  const data = await res.json().catch(() => ({} as any));
  const id = typeof data?.workflow_id === "string" ? data.workflow_id : undefined;
  if (!id) return NextResponse.json({ error: "Failed to create chat" }, { status: 500 });
  return NextResponse.json({ id, title: question || `Chat ${id}` }, { status: 200 });
}
