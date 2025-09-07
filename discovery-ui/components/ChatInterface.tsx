"use client";

import React, {
  useState,
  useRef,
  useCallback,
  useMemo,
  useEffect,
  FormEvent,
} from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot, LoaderCircle, SquarePen, History, X } from "lucide-react";
import { ChatMessage } from "./ChatMessage";
import { ThreadHistorySidebar } from "./ThreadHistorySidebar";
import type { SubAgent, TodoItem, ToolCall } from "@/lib/types";
import { useChat } from "@/hooks/useChat";
import { Message } from "@langchain/langgraph-sdk";
import { extractStringFromMessageContent } from "@/lib/utils";

interface ChatInterfaceProps {
  threadId: string | null;
  selectedSubAgent: SubAgent | null;
  setThreadId: (
    value: string | ((old: string | null) => string | null) | null,
  ) => void;
  onSelectSubAgent: (subAgent: SubAgent) => void;
  onTodosUpdate: (todos: TodoItem[]) => void;
  onFilesUpdate: (files: Record<string, string>) => void;
  onNewThread: () => void;
  isLoadingThreadState: boolean;
}

export const ChatInterface = React.memo<ChatInterfaceProps>(
  ({
    threadId,
    selectedSubAgent,
    setThreadId,
    onSelectSubAgent,
    onTodosUpdate,
    onFilesUpdate,
    onNewThread,
    isLoadingThreadState,
  }) => {
    const [input, setInput] = useState("");
    const [isThreadHistoryOpen, setIsThreadHistoryOpen] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const { messages, isLoading, sendMessage, stopStream } = useChat(
      threadId,
      setThreadId,
      onTodosUpdate,
      onFilesUpdate,
    );

    useEffect(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSubmit = useCallback(
      (e: FormEvent) => {
        e.preventDefault();
        const messageText = input.trim();
        if (!messageText || isLoading) return;
        sendMessage(messageText);
        setInput("");
      },
      [input, isLoading, sendMessage],
    );

    const handleNewThread = useCallback(() => {
      // Cancel any ongoing thread when creating new thread
      if (isLoading) {
        stopStream();
      }
      setIsThreadHistoryOpen(false);
      onNewThread();
    }, [isLoading, stopStream, onNewThread]);

    const handleThreadSelect = useCallback(
      (id: string) => {
        setThreadId(id);
        setIsThreadHistoryOpen(false);
      },
      [setThreadId],
    );

    const toggleThreadHistory = useCallback(() => {
      setIsThreadHistoryOpen((prev) => !prev);
    }, []);

    const hasMessages = messages.length > 0;

    const processedMessages = useMemo(() => {
      /*
    1. Loop through all messages
    2. For each AI message, add the AI message, and any tool calls to the messageMap
    3. For each tool message, find the corresponding tool call in the messageMap and update the status and output
    */
      const messageMap = new Map<string, any>();
      messages.forEach((message: Message) => {
        if (message.type === "ai") {
          const toolCallsInMessage: any[] = [];
          if (
            message.additional_kwargs?.tool_calls &&
            Array.isArray(message.additional_kwargs.tool_calls)
          ) {
            toolCallsInMessage.push(...message.additional_kwargs.tool_calls);
          } else if (message.tool_calls && Array.isArray(message.tool_calls)) {
            toolCallsInMessage.push(
              ...message.tool_calls.filter(
                (toolCall: any) => toolCall.name !== "",
              ),
            );
          } else if (Array.isArray(message.content)) {
            const toolUseBlocks = message.content.filter(
              (block: any) => block.type === "tool_use",
            );
            toolCallsInMessage.push(...toolUseBlocks);
          }
          const toolCallsWithStatus = toolCallsInMessage.map(
            (toolCall: any) => {
              const name =
                toolCall.function?.name ||
                toolCall.name ||
                toolCall.type ||
                "unknown";
              const args =
                toolCall.function?.arguments ||
                toolCall.args ||
                toolCall.input ||
                {};
              return {
                id: toolCall.id || `tool-${Math.random()}`,
                name,
                args,
                status: "pending" as const,
              } as ToolCall;
            },
          );
          messageMap.set(message.id!, {
            message,
            toolCalls: toolCallsWithStatus,
          });
        } else if (message.type === "tool") {
          const toolCallId = message.tool_call_id;
          if (!toolCallId) {
            return;
          }
          for (const [, data] of messageMap.entries()) {
            const toolCallIndex = data.toolCalls.findIndex(
              (tc: any) => tc.id === toolCallId,
            );
            if (toolCallIndex === -1) {
              continue;
            }
            data.toolCalls[toolCallIndex] = {
              ...data.toolCalls[toolCallIndex],
              status: "completed" as const,
              // TODO: Make this nicer
              result: extractStringFromMessageContent(message),
            };
            break;
          }
        } else if (message.type === "human") {
          messageMap.set(message.id!, {
            message,
            toolCalls: [],
          });
        }
      });
      const processedArray = Array.from(messageMap.values());
      return processedArray.map((data, index) => {
        const prevMessage =
          index > 0 ? processedArray[index - 1].message : null;
        return {
          ...data,
          showAvatar: data.message.type !== prevMessage?.type,
        };
      });
    }, [messages]);

    return (
      <div className="flex flex-col h-screen w-full bg-background">
        <div className="flex justify-between items-center px-6 py-4 border-b border-border bg-background flex-shrink-0">
          <div className="flex items-center gap-3">
            <Bot className="w-6 h-6 text-primary" />
            <h1 className="text-xl font-semibold text-foreground">Discovery Agent</h1>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleNewThread}
              disabled={!hasMessages}
            >
              <SquarePen size={20} />
            </Button>
            <Button variant="ghost" size="icon" onClick={toggleThreadHistory}>
              <History size={20} />
            </Button>
          </div>
        </div>
        <div className="flex flex-1 min-h-0 relative">
          <ThreadHistorySidebar
            open={isThreadHistoryOpen}
            setOpen={setIsThreadHistoryOpen}
            currentThreadId={threadId}
            onThreadSelect={handleThreadSelect}
          />
          <div className="flex flex-col flex-1 min-h-0">
            {!hasMessages && !isLoading && !isLoadingThreadState && (
              <div className="flex flex-col items-center justify-center h-full px-8 text-center">
                <Bot size={48} className="text-muted-foreground mb-6" />
                <h2 className="text-2xl font-semibold text-foreground mb-2">Start a conversation</h2>
                <p className="text-muted-foreground">Ask me anything and I'll help you discover insights.</p>
              </div>
            )}
            {isLoadingThreadState && (
              <div className="flex items-center justify-center h-full">
                <LoaderCircle className="animate-spin w-8 h-8 text-primary" />
              </div>
            )}
            <div className="flex-1 overflow-y-auto px-6 py-4">
              {processedMessages.map((data) => (
                <ChatMessage
                  key={data.message.id}
                  message={data.message}
                  toolCalls={data.toolCalls}
                  showAvatar={data.showAvatar}
                  onSelectSubAgent={onSelectSubAgent}
                  selectedSubAgent={selectedSubAgent}
                />
              ))}
              {isLoading && (
                <div className="flex items-center gap-3 px-4 py-3 text-muted-foreground">
                  <LoaderCircle className="animate-spin w-5 h-5" />
                  <span>Working...</span>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
        </div>
        <form onSubmit={handleSubmit} className="flex gap-3 px-6 py-4 border-t border-border bg-background flex-shrink-0">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1"
          />
          {isLoading ? (
            <Button
              type="button"
              onClick={stopStream}
              variant="destructive"
            >
              Stop
            </Button>
          ) : (
            <Button
              type="submit"
              disabled={!input.trim()}
            >
              <Send size={16} />
            </Button>
          )}
        </form>
      </div>
    );
  },
);

ChatInterface.displayName = "ChatInterface";
