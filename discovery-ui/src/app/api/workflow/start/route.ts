import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const body = await req.json().catch(() => ({}));
  const dest = `${base}/chat/send-sync`;
  const res = await fetch(dest, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      text: body.question || "Hello",
      goal: "Have a helpful conversation"
    })
  });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json({
    workflow_id: data.workflow_id
  }, { status: res.status });
}
