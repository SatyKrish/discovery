import { NextResponse } from "next/server";

export async function GET(req: Request) {
  const url = new URL(req.url);
  const chatId = url.searchParams.get("chatId");
  if (!chatId) return NextResponse.json({ messages: [] }, { status: 200 });
  const res = await fetch(`${url.origin}/api/workflow/${encodeURIComponent(chatId)}/history`, { method: "GET" });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}

export async function POST(req: Request) {
  const url = new URL(req.url);
  const body = (await req.json().catch(() => ({}))) as { chatId?: unknown; text?: unknown };
  const chatId = typeof body.chatId === "string" ? body.chatId : url.searchParams.get("chatId");
  const text = typeof body.text === "string" ? body.text : undefined;
  if (!chatId || !text) return NextResponse.json({ error: "Invalid payload" }, { status: 400 });
  const res = await fetch(`${url.origin}/api/workflow/${encodeURIComponent(chatId)}/prompt`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ prompt: text }),
  });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
