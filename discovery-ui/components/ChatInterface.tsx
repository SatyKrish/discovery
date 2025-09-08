"use client";

import React, {
  useState,
  useRef,
  useCallback,
  useMemo,
  useEffect,
  FormEvent,
} from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { SidebarTrigger, useSidebar } from "@/components/ui/sidebar";
import { Send, Bot, LoaderCircle, SquarePen, Sun, Moon, Monitor } from "lucide-react";
import { ChatMessage } from "./ChatMessage";
import { SuggestedActions } from "./SuggestedActions";
import type { SubAgent, TodoItem, ToolCall } from "@/lib/types";
import { useChat } from "@/hooks/useChat";
import { useTheme } from "@/components/theme-provider";
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
  onThreadCreated?: (threadId: string) => void;
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
    onThreadCreated,
    isLoadingThreadState,
  }) => {
    const [input, setInput] = useState("");
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const { state: sidebarState, setOpenMobile } = useSidebar();
    const { theme, setTheme } = useTheme();

    const { messages, isLoading, sendMessage, stopStream } = useChat(
      threadId,
      setThreadId,
      onTodosUpdate,
      onFilesUpdate,
      onThreadCreated,
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
      onNewThread();
    }, [isLoading, stopStream, onNewThread]);

    const handleThemeToggle = useCallback(() => {
      if (theme === 'light') {
        setTheme('dark');
      } else if (theme === 'dark') {
        setTheme('system');
      } else {
        setTheme('light');
      }
    }, [theme, setTheme]);

    const handleSuggestedAction = useCallback((prompt: string) => {
      setInput(prompt);
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
      <div className="flex flex-col h-full w-full bg-background">
        {/* Header */}
        <div className="relative flex items-center px-4 md:px-6 py-4 bg-background flex-shrink-0">
          {/* Left side content - branding when sidebar collapsed */}
          <div className="flex items-center gap-3">
            {sidebarState === 'collapsed' && (
              <Link
                href="/"
                onClick={() => {
                  setOpenMobile(false);
                }}
                className="flex flex-row gap-3 items-center"
              >
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10">
                  <Bot className="w-5 h-5 text-primary" />
                </div>
                <span className="text-lg font-semibold px-2 hover:bg-muted rounded-md cursor-pointer text-foreground">
                  Discovery
                </span>
              </Link>
            )}
            {sidebarState === 'collapsed' && (
              <SidebarTrigger className="h-8 w-8" />
            )}
          </div>

          {/* Action buttons in top right corner */}
          <div className="absolute right-4 md:right-6 flex items-center gap-1">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleThemeToggle}
              className="h-9 w-9"
              title={`Current theme: ${theme}. Click to cycle themes.`}
            >
              {theme === 'light' && <Sun size={18} />}
              {theme === 'dark' && <Moon size={18} />}
              {theme === 'system' && <Monitor size={18} />}
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleNewThread}
              disabled={!hasMessages}
              className="h-9 w-9"
            >
              <SquarePen size={18} />
            </Button>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex flex-1 min-h-0">
          <div className="flex flex-col flex-1 min-h-0">
            {!hasMessages && !isLoading && !isLoadingThreadState && (
              <div className="flex flex-col items-center justify-center h-full px-4 md:px-8 text-center space-y-8">
                <div>
                  <h2 className="text-xl md:text-2xl font-semibold text-foreground mb-2">Start a conversation</h2>
                  <p className="text-sm md:text-base text-muted-foreground">Ask me anything and I'll help you discover insights.</p>
                </div>

                <div className="w-full max-w-4xl">
                  <h3 className="text-lg font-medium mb-6 text-foreground">Try these suggestions:</h3>
                  <SuggestedActions onActionClick={handleSuggestedAction} />
                </div>
              </div>
            )}
            {isLoadingThreadState && (
              <div className="flex items-center justify-center h-full">
                <LoaderCircle className="animate-spin w-8 h-8 text-primary" />
              </div>
            )}
            <div className="flex-1 overflow-y-auto px-4 md:px-6 py-4">
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

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="flex gap-2 md:gap-3 px-4 md:px-6 py-4 border-t border-border bg-background flex-shrink-0">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1 text-sm md:text-base"
            data-testid="multimodal-input"
          />
          {isLoading ? (
            <Button
              type="button"
              onClick={stopStream}
              variant="destructive"
              size="sm"
              className="px-3 md:px-4"
              data-testid="stop-button"
            >
              <span className="hidden sm:inline">Stop</span>
              <SquarePen size={16} className="sm:hidden" />
            </Button>
          ) : (
            <Button
              type="submit"
              disabled={!input.trim()}
              size="sm"
              className="px-3 md:px-4"
              data-testid="send-button"
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
