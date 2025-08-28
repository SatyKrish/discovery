import { NextResponse } from "next/server";

export async function GET(req: Request) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });

  const url = new URL(req.url);
  // Forward to backend without the /api prefix: /api/chats -> {base}/chats
  const dest = `${base}${url.pathname.replace(/^\/api/, "")}${url.search}`;
  const res = await fetch(dest, { method: "GET" });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
