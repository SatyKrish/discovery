import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const base = process.env.BACKEND_BASE_URL;
  if (!base) return NextResponse.json({ error: "BACKEND_BASE_URL not set" }, { status: 500 });
  try {
    const form = await req.formData();
    const dest = `${base}/uploads`;
    const res = await fetch(dest, { method: "POST", body: form as unknown as BodyInit });
    const data = await res.json().catch(() => ({} as unknown));
    return NextResponse.json(data, { status: res.status });
  } catch (e: unknown) {
    const message = (e as { message?: string } | null)?.message || "Upload failed";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
