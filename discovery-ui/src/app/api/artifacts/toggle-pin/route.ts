import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  const url = new URL(req.url);
  const dest = `${base}${url.pathname.replace(/^\/api/, "")}${url.search}`;
  const body = await req.json().catch(() => ({}));
  const res = await fetch(dest, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
  const data = await res.json().catch(() => ({}));
  return NextResponse.json(data, { status: res.status });
}
