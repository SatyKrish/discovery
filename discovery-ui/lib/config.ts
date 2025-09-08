export function getAgent() {
  return {
    name: "Discovery Agent",
    apiUrl: process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:2024",
    agentId: process.env.NEXT_PUBLIC_AGENT_ID || "discoveryagent",
  };
}
