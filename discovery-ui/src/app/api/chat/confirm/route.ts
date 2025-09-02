import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const base = process.env.BACKEND_BASE_URL || 'http://localhost:8080';
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });

  try {
    const body = await req.json().catch(() => ({}));
    const dest = `${base}/chat/confirm`;
    const res = await fetch(dest, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body)
    });

    const data = await res.json().catch(() => ({}));
    return NextResponse.json(data, { status: res.status });
  } catch (error) {
    console.error('Chat confirm error:', error);
    return NextResponse.json({ error: "Failed to confirm tool" }, { status: 500 });
  }
}
