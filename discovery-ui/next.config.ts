import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    // Ensure Next.js uses the UI folder as the workspace root during tests/build
    root: __dirname,
  },
};

export default nextConfig;
