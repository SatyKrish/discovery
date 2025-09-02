import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const base = process.env.DISCOVERY_AGENT_URL;
  if (!base) return NextResponse.json({ error: "DISCOVERY_AGENT_URL not set" }, { status: 500 });

  try {
    const body = await req.json().catch(() => ({}));
    const dest = `${base}/chat/wait-sync`;
    const res = await fetch(dest, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body)
    });

    const data = await res.json().catch(() => ({}));
    return NextResponse.json(data, { status: res.status });
  } catch (error) {
    console.error('Chat wait-sync error:', error);
    return NextResponse.json({ error: "Failed to wait for response" }, { status: 500 });
  }
}
