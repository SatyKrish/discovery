import { Client } from "@langchain/langgraph-sdk";
import { getAgent } from "./config";

export function createClient(accessToken?: string) {
  const agent = getAgent();
  const clientConfig: any = {
    apiUrl: agent?.apiUrl || "http://127.0.0.1:2024",
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
