import { Client } from "@langchain/langgraph-sdk";
import { getDeployment } from "./environment/deployments";

export function createClient(accessToken?: string) {
  const deployment = getDeployment();
  const clientConfig: any = {
    apiUrl: deployment?.deploymentUrl || "http://127.0.0.1:2024",
  };

  // Only add auth if accessToken is provided and not empty
  if (accessToken && accessToken.trim() !== "") {
    clientConfig.apiKey = accessToken;
    clientConfig.defaultHeaders = {
      "x-auth-scheme": "langsmith",
    };
  }

  return new Client(clientConfig);
}
