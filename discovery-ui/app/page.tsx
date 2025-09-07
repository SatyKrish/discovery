"use client";

import React, { useState, useCallback } from "react";
import { useQueryState } from "nuqs";
import { ChatInterface } from "@/components/ChatInterface";
import type { SubAgent, TodoItem } from "@/types/types";

export default function HomePage() {
  const [threadId, setThreadId] = useQueryState("threadId");
  const [selectedSubAgent, setSelectedSubAgent] = useState<SubAgent | null>(null);
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [files, setFiles] = useState<Record<string, string>>({});
  const [isLoadingThreadState, setIsLoadingThreadState] = useState(false);

  const handleNewThread = useCallback(() => {
    setThreadId(null);
    setSelectedSubAgent(null);
    setTodos([]);
    setFiles({});
  }, [setThreadId]);

  return (
    <ChatInterface
      threadId={threadId}
      selectedSubAgent={selectedSubAgent}
      setThreadId={setThreadId}
      onSelectSubAgent={setSelectedSubAgent}
      onTodosUpdate={setTodos}
      onFilesUpdate={setFiles}
      onNewThread={handleNewThread}
      isLoadingThreadState={isLoadingThreadState}
    />
  );
}
