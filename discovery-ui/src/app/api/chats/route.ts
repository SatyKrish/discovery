import { NextResponse } from "next/server";
import { getChats } from "@/server/store";

export async function GET() {
  return NextResponse.json(getChats(), { status: 200 });
}
