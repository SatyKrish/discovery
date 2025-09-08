"use client";

import React, { useState, useCallback, Suspense } from "react";
import { useQueryState } from "nuqs";
import { ChatInterface } from "@/components/ChatInterface";
import { DiscoverySidebar } from "@/components/app-sidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import type { SubAgent, TodoItem } from "@/lib/types";

function HomePageContent() {
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

  const handleThreadSelect = useCallback((selectedThreadId: string) => {
    setThreadId(selectedThreadId);
    setSelectedSubAgent(null);
  }, [setThreadId]);

  const handleThreadCreated = useCallback((newThreadId: string) => {
    console.log('Thread created in parent:', newThreadId);
    // The sidebar will handle refreshing its own thread list
  }, []);

  return (
    <div className="flex h-screen w-full">
      <SidebarProvider>
        <DiscoverySidebar
          currentThreadId={threadId}
          onThreadSelect={handleThreadSelect}
          onNewThread={handleNewThread}
          onThreadCreated={handleThreadCreated}
        />
        <SidebarInset>
          <ChatInterface
            threadId={threadId}
            selectedSubAgent={selectedSubAgent}
            setThreadId={setThreadId}
            onSelectSubAgent={setSelectedSubAgent}
            onTodosUpdate={setTodos}
            onFilesUpdate={setFiles}
            onNewThread={handleNewThread}
            onThreadCreated={handleThreadCreated}
            isLoadingThreadState={isLoadingThreadState}
          />
        </SidebarInset>
      </SidebarProvider>
    </div>
  );
}

export default function HomePage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HomePageContent />
    </Suspense>
  );
}
