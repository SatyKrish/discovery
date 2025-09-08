import { useCallback, useMemo } from "react";
import { useStream } from "@langchain/langgraph-sdk/react";
import { type Message } from "@langchain/langgraph-sdk";
import { getAgent } from "@/lib/config";
import { v4 as uuidv4 } from "uuid";
import type { TodoItem, AgentState } from "@/lib/types";
import { createClient } from "@/lib/client";


export function useChat(
  threadId: string | null,
  setThreadId: (
    value: string | ((old: string | null) => string | null) | null,
  ) => void,
  onTodosUpdate: (todos: TodoItem[]) => void,
  onFilesUpdate: (files: Record<string, string>) => void,
  onThreadCreated?: (threadId: string) => void,
) {
  const agent = useMemo(() => getAgent(), []);

  const agentId = useMemo(() => {
    if (!agent?.agentId) {
      throw new Error(`No agent ID configured in environment`);
    }
    return agent.agentId;
  }, [agent]);

  const handleUpdateEvent = useCallback(
    (data: { [node: string]: Partial<AgentState> }) => {
      Object.entries(data).forEach(([_, nodeData]) => {
        if (nodeData?.todos) {
          onTodosUpdate(nodeData.todos);
        }
        if (nodeData?.files) {
          onFilesUpdate(nodeData.files);
        }
      });
    },
    [onTodosUpdate, onFilesUpdate],
  );

  const handleThreadId = useCallback((newThreadId: string | null) => {
    // Call the original setThreadId
    setThreadId(newThreadId);
    // If a new thread was created (threadId was null and now has a value), notify
    if (onThreadCreated && threadId === null && newThreadId !== null) {
      onThreadCreated(newThreadId);
    }
  }, [setThreadId, threadId, onThreadCreated]);

  const stream = useStream<AgentState & Record<string, unknown>>({
    assistantId: agentId,
    client: createClient(),
    reconnectOnMount: true,
    threadId: threadId ?? null,
    onUpdateEvent: handleUpdateEvent,
    onThreadId: handleThreadId,
    defaultHeaders: {
      "x-auth-scheme": "langsmith",
    },
  });

  const sendMessage = useCallback(
    (message: string) => {
      const humanMessage: Message = {
        id: uuidv4(),
        type: "human",
        content: message,
        role: "user",
      } as Message;
      stream.submit(
        { messages: [humanMessage] },
        {
          optimisticValues(prev) {
            const prevMessages = prev.messages ?? [];
            const newMessages = [...prevMessages, humanMessage];
            return { ...prev, messages: newMessages };
          },
          config: {
            recursion_limit: 100,
          },
        },
      );
    },
    [stream],
  );

  const stopStream = useCallback(() => {
    stream.stop();
  }, [stream]);

  return {
    messages: stream.messages,
    isLoading: stream.isLoading,
    sendMessage,
    stopStream,
  };
}
