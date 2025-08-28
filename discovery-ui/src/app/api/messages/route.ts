import { NextResponse } from "next/server";
import { addMessage, getMessages } from "@/server/store";
import type { Message } from "@/lib/provider";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const chatId = searchParams.get("chatId") || "demo";
  return NextResponse.json(getMessages(chatId), { status: 200 });
}

export async function POST(req: Request) {
  const { chatId = "demo", text = "" } = await req.json();
  const now = new Date().toISOString();
  const userMsg: Message = { id: `${Date.now()}`, role: "user", text, createdAt: now };
  addMessage(chatId, userMsg);

  const assistant: Message = { id: `${Date.now()+1}`, role: "agent", text: `You said: ${text}`, createdAt: new Date().toISOString() };
  addMessage(chatId, assistant);

  return NextResponse.json({ ok: true }, { status: 200 });
}
