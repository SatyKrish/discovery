"use client";

import React, { useEffect, useState, useCallback, useMemo } from "react";
import { MessageSquare, X } from "lucide-react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { createClient } from "@/lib/client";
import { useAuthContext } from "@/providers/Auth";
import { getDeployment } from "@/lib/environment/deployments";
import type { Thread } from "@/lib/types";
import { extractStringFromMessageContent } from "@/lib/utils";

interface ThreadHistorySidebarProps {
  open: boolean;
  setOpen: (open: boolean) => void;
  currentThreadId: string | null;
  onThreadSelect: (threadId: string) => void;
}

export const ThreadHistorySidebar = React.memo<ThreadHistorySidebarProps>(
  ({ open, setOpen, currentThreadId, onThreadSelect }) => {
    const [threads, setThreads] = useState<Thread[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const { session } = useAuthContext();
    const deployment = useMemo(() => getDeployment(), []);

    const fetchThreads = useCallback(async () => {
      if (!deployment?.deploymentUrl || !session?.accessToken) return;
      setIsLoading(true);
      try {
        const client = createClient(session.accessToken);
        const response = await client.threads.search({
          limit: 30,
          sortBy: "created_at",
          sortOrder: "desc",
        });
        const threadList: Thread[] = response.map((thread: any) => {
          let displayContent = `Thread ${thread.thread_id.slice(0, 8)}`;
          try {
            if (
              thread.values &&
              typeof thread.values === "object" &&
              "messages" in thread.values
            ) {
              const messages = (thread.values as any).messages;
              if (Array.isArray(messages) && messages.length > 0) {
                displayContent = extractStringFromMessageContent(messages[0]);
              }
            }
          } catch (error) {
            console.warn(
              `Failed to get first message for thread ${thread.thread_id}:`,
              error,
            );
          }
          return {
            id: thread.thread_id,
            title: displayContent,
            createdAt: new Date(thread.created_at),
            updatedAt: new Date(thread.updated_at || thread.created_at),
          } as Thread;
        });
        setThreads(
          threadList.sort(
            (a, b) => b.updatedAt.getTime() - a.updatedAt.getTime(),
          ),
        );
      } catch (error) {
        console.error("Failed to fetch threads:", error);
      } finally {
        setIsLoading(false);
      }
    }, [deployment?.deploymentUrl, session?.accessToken]);

    useEffect(() => {
      if (open) {
        fetchThreads();
      }
    }, [open, fetchThreads]);

    const groupedThreads = useMemo(() => {
      const groups: Record<string, Thread[]> = {
        today: [],
        yesterday: [],
        week: [],
        older: [],
      };
      const now = new Date();
      threads.forEach((thread) => {
        const diff = now.getTime() - thread.updatedAt.getTime();
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        if (days === 0) groups.today.push(thread);
        else if (days === 1) groups.yesterday.push(thread);
        else if (days < 7) groups.week.push(thread);
        else groups.older.push(thread);
      });
      return groups;
    }, [threads]);

    const sidebarContent = (
      <div className="flex flex-col h-full">
        <div className="flex items-center justify-between p-4 border-b border-border">
          <h3 className="text-lg font-semibold text-foreground">Thread History</h3>
          <button
            onClick={() => setOpen(false)}
            className="p-2 hover:bg-muted rounded-md transition-colors md:hidden"
          >
            <X size={20} />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto">
          {isLoading ? (
            <div className="flex items-center justify-center h-32">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : threads.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-32 text-center px-4">
              <MessageSquare size={32} className="text-muted-foreground mb-2" />
              <p className="text-sm text-muted-foreground">No threads yet</p>
            </div>
          ) : (
            <div className="p-2">
              {groupedThreads.today.length > 0 && (
                <div className="mb-6">
                  <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 px-2">
                    Today
                  </h4>
                  {groupedThreads.today.map((thread) => (
                    <ThreadItem
                      key={thread.id}
                      thread={thread}
                      isActive={thread.id === currentThreadId}
                      onClick={() => onThreadSelect(thread.id)}
                    />
                  ))}
                </div>
              )}
              {groupedThreads.yesterday.length > 0 && (
                <div className="mb-6">
                  <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 px-2">
                    Yesterday
                  </h4>
                  {groupedThreads.yesterday.map((thread) => (
                    <ThreadItem
                      key={thread.id}
                      thread={thread}
                      isActive={thread.id === currentThreadId}
                      onClick={() => onThreadSelect(thread.id)}
                    />
                  ))}
                </div>
              )}
              {groupedThreads.week.length > 0 && (
                <div className="mb-6">
                  <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 px-2">
                    This Week
                  </h4>
                  {groupedThreads.week.map((thread) => (
                    <ThreadItem
                      key={thread.id}
                      thread={thread}
                      isActive={thread.id === currentThreadId}
                      onClick={() => onThreadSelect(thread.id)}
                    />
                  ))}
                </div>
              )}
              {groupedThreads.older.length > 0 && (
                <div className="mb-6">
                  <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 px-2">
                    Older
                  </h4>
                  {groupedThreads.older.map((thread) => (
                    <ThreadItem
                      key={thread.id}
                      thread={thread}
                      isActive={thread.id === currentThreadId}
                      onClick={() => onThreadSelect(thread.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );

    return (
      <>
        {/* Mobile Sheet */}
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetContent side="right" className="w-80 p-0">
            <SheetHeader className="sr-only">
              <SheetTitle>Thread History</SheetTitle>
            </SheetHeader>
            {sidebarContent}
          </SheetContent>
        </Sheet>

        {/* Desktop Fixed Sidebar */}
        {open && (
          <div className="hidden md:flex fixed inset-y-0 right-0 w-80 bg-background border-l border-border shadow-xl z-50 flex-col">
            {sidebarContent}
          </div>
        )}
      </>
    );
  },
);

const ThreadItem = React.memo<{
  thread: Thread;
  isActive: boolean;
  onClick: () => void;
}>(({ thread, isActive, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-3 rounded-lg mb-1 transition-colors ${
        isActive
          ? 'bg-primary text-primary-foreground'
          : 'hover:bg-muted text-foreground'
      }`}
    >
      <div className="flex items-start gap-3">
        <MessageSquare size={16} className="mt-0.5 flex-shrink-0" />
        <div className="flex-1 min-w-0">
          <div className="text-sm font-medium truncate">{thread.title}</div>
          <div className="text-xs text-muted-foreground mt-1">
            {thread.updatedAt.toLocaleDateString()}
          </div>
        </div>
      </div>
    </button>
  );
});

ThreadItem.displayName = "ThreadItem";
ThreadHistorySidebar.displayName = "ThreadHistorySidebar";
