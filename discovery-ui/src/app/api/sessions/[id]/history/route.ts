import { NextResponse } from "next/server";

export async function GET(
  req: Request,
  { params }: { params: { id: string } }
) {
  const base = process.env.DISCOVERY_AGENT_URL;
  if (!base) return NextResponse.json({ error: "DISCOVERY_AGENT_URL not set" }, { status: 500 });

  try {
    const dest = `${base}/sessions/${params.id}/history`;
    const res = await fetch(dest, { cache: "no-store" });

    const data = await res.json().catch(() => []);
    return NextResponse.json(data, { status: res.status });
  } catch (error) {
    console.error('Session history error:', error);
    return NextResponse.json({ error: "Failed to get session history" }, { status: 500 });
  }
}
