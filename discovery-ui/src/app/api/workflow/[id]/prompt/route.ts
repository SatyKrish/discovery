import { NextResponse } from "next/server";

export async function POST(req: Request, ctx: { params: Promise<{ id: string }> }) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const { id } = await ctx.params;
  const body = await req.json().catch(() => ({}));
  const dest = `${base}/chat/send-sync`;
  const res = await fetch(dest, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      text: body.prompt,
      workflow_id: id,
      goal: "Have a helpful conversation"
    })
  });
  const data = await res.json().catch(() => ({}));

  // Transform backend response to match frontend expectations
  const response: any = {};

  // Handle assistant message
  if (data.assistant) {
    response.assistant = {
      id: `assistant-${Date.now()}`,
      role: 'agent',
      text: data.assistant.content || '',
      createdAt: data.assistant.ts ? new Date(data.assistant.ts * 1000).toLocaleString() : new Date().toLocaleString()
    };
  }

  // Handle pending tool call
  if (data.pending_tool) {
    response.pending_tool = {
      id: data.pending_tool.id,
      name: data.pending_tool.name,
      args: data.pending_tool.args
    };
  }

  return NextResponse.json(response, { status: res.status });
}
