"use client";

import React, { useState, useMemo, useCallback } from "react";
import {
  ChevronDown,
  ChevronRight,
  Terminal,
  CheckCircle,
  AlertCircle,
  Loader,
} from "lucide-react";
import type { ToolCall } from "@/types/types";

interface ToolCallBoxProps {
  toolCall: ToolCall;
}

export const ToolCallBox = React.memo<ToolCallBoxProps>(({ toolCall }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const { name, args, result, status } = useMemo(() => {
    const toolName = toolCall.name || "Unknown Tool";
    const toolArgs = toolCall.args || "{}";
    let parsedArgs = {};
    try {
      parsedArgs =
        typeof toolArgs === "string" ? JSON.parse(toolArgs) : toolArgs;
    } catch {
      parsedArgs = { raw: toolArgs };
    }
    const toolResult = toolCall.result || null;
    const toolStatus = toolCall.status || "completed";

    return {
      name: toolName,
      args: parsedArgs,
      result: toolResult,
      status: toolStatus,
    };
  }, [toolCall]);

  const statusIcon = useMemo(() => {
    switch (status) {
      case "completed":
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case "error":
        return <AlertCircle className="w-4 h-4 text-red-600" />;
      case "pending":
        return <Loader className="w-4 h-4 animate-spin text-blue-600" />;
      default:
        return <Terminal className="w-4 h-4 text-gray-600" />;
    }
  }, [status]);

  const toggleExpanded = useCallback(() => {
    setIsExpanded((prev) => !prev);
  }, []);

  const hasContent = result || Object.keys(args).length > 0;

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden w-fit max-w-full">
      <button
        onClick={toggleExpanded}
        className="w-full px-4 py-3 flex items-center justify-between gap-3 text-left hover:bg-muted/50 focus:outline-none focus:ring-2 focus:ring-ring transition-colors"
        disabled={!hasContent}
      >
        <div className="flex items-center gap-3 flex-1 min-w-0">
          {hasContent && isExpanded ? (
            <ChevronDown className="w-4 h-4 text-muted-foreground flex-shrink-0" />
          ) : (
            <ChevronRight className="w-4 h-4 text-muted-foreground flex-shrink-0" />
          )}
          {statusIcon}
          <span className="font-medium text-sm text-foreground truncate">{name}</span>
        </div>
      </button>

      {isExpanded && hasContent && (
        <div className="px-4 pb-4 border-t border-border">
          {Object.keys(args).length > 0 && (
            <div className="mt-4">
              <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                Arguments
              </h4>
              <pre className="bg-muted p-3 rounded-md text-xs font-mono overflow-x-auto max-w-full whitespace-pre-wrap break-all">
                {JSON.stringify(args, null, 2)}
              </pre>
            </div>
          )}
          {result && (
            <div className="mt-4">
              <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                Result
              </h4>
              <pre className="bg-muted p-3 rounded-md text-xs font-mono overflow-x-auto max-w-full whitespace-pre-wrap break-all">
                {typeof result === "string"
                  ? result
                  : JSON.stringify(result, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
});

ToolCallBox.displayName = "ToolCallBox";
