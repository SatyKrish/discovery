import NextAuth from "next-auth";
import AzureADProvider from "next-auth/providers/azure-ad";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const handler =
  process.env.NODE_ENV === "production"
    ? NextAuth({
        providers: [
          AzureADProvider({
            clientId: process.env.AZURE_AD_CLIENT_ID!,
            clientSecret: process.env.AZURE_AD_CLIENT_SECRET!,
            tenantId: process.env.AZURE_AD_TENANT_ID,
          }),
        ],
      })
    : (_req: NextRequest) => NextResponse.json({}, { status: 404 });

export { handler as GET, handler as POST };
