import { Client } from "@langchain/langgraph-sdk";
import { getDeployment } from "./environment/deployments";

export function createClient(accessToken: string) {
  const deployment = getDeployment();
  return new Client({
    apiUrl: deployment?.deploymentUrl || "http://127.0.0.1:2024",
    apiKey: accessToken,
    defaultHeaders: {
      "x-auth-scheme": "langsmith",
    },
  });
}
