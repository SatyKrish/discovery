export function getDeployment() {
  return {
    name: "Discovery Agent",
    deploymentUrl: process.env.NEXT_PUBLIC_DEPLOYMENT_URL || "http://127.0.0.1:2024",
    agentId: process.env.NEXT_PUBLIC_AGENT_ID || "discoveryagent",
  };
}
