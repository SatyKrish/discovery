'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState, useCallback, useMemo } from 'react';
import { Bot, Plus, Search, Filter, MessageSquare, X } from 'lucide-react';

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarGroup,
  SidebarGroupContent,
  useSidebar,
} from '@/components/ui/sidebar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { createClient } from '@/lib/client';
import { useAuthContext } from '@/providers/Auth';
import { getDeployment } from '@/lib/environment/deployments';
import type { Thread } from '@/lib/types';
import { extractStringFromMessageContent } from '@/lib/utils';
import Link from 'next/link';

interface DiscoverySidebarProps {
  currentThreadId?: string | null;
  onThreadSelect?: (threadId: string) => void;
  onNewThread?: () => void;
}

type DateFilter = 'all' | 'today' | 'week' | 'month';

export function DiscoverySidebar({ currentThreadId = null, onThreadSelect, onNewThread }: DiscoverySidebarProps) {
  const router = useRouter();
  const { setOpenMobile, toggleSidebar } = useSidebar();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [dateFilter, setDateFilter] = useState<DateFilter>('all');
  const [threads, setThreads] = useState<Thread[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const { session } = useAuthContext();
  const deployment = useMemo(() => getDeployment(), []);

  // Add keyboard shortcut support (Cmd/Ctrl + B to toggle sidebar)
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'b' && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        toggleSidebar();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [toggleSidebar]);

  // Fetch threads
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
    if (sidebarOpen) {
      fetchThreads();
    }
  }, [sidebarOpen, fetchThreads]);

  // Filter threads based on search and date
  const filteredThreads = useMemo(() => {
    let filtered = threads;

    // Text search
    if (searchQuery.trim()) {
      filtered = filtered.filter((thread) =>
        thread.title.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Date filter
    if (dateFilter !== 'all') {
      const now = new Date();
      const filterDate = new Date();

      switch (dateFilter) {
        case 'today':
          filterDate.setHours(0, 0, 0, 0);
          break;
        case 'week':
          filterDate.setDate(now.getDate() - 7);
          break;
        case 'month':
          filterDate.setMonth(now.getMonth() - 1);
          break;
      }

      filtered = filtered.filter((thread) => thread.updatedAt >= filterDate);
    }

    return filtered;
  }, [threads, searchQuery, dateFilter]);

  // Group threads by date
  const groupedThreads = useMemo(() => {
    const groups: Record<string, Thread[]> = {
      today: [],
      yesterday: [],
      week: [],
      older: [],
    };
    const now = new Date();
    filteredThreads.forEach((thread) => {
      const diff = now.getTime() - thread.updatedAt.getTime();
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      if (days === 0) groups.today.push(thread);
      else if (days === 1) groups.yesterday.push(thread);
      else if (days < 7) groups.week.push(thread);
      else groups.older.push(thread);
    });
    return groups;
  }, [filteredThreads]);

  const handleThreadSelect = (threadId: string) => {
    if (onThreadSelect) {
      onThreadSelect(threadId);
    }
    // Close mobile sidebar after selection
    setOpenMobile(false);
  };

  const handleNewThread = () => {
    if (onNewThread) {
      onNewThread();
    }
    // Close mobile sidebar after creating new thread
    setOpenMobile(false);
  };

  return (
    <Sidebar className="group-data-[side=left]:border-r-0">
      <SidebarHeader>
        <SidebarMenu>
          <div className="flex flex-row justify-between items-center">
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
              <span className="text-lg font-semibold px-2 hover:bg-muted rounded-md cursor-pointer">
                Discovery Agent
              </span>
            </Link>
          </div>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            {/* New Chat Button */}
            <div className="px-2 py-2">
              <Button
                onClick={handleNewThread}
                className="w-full h-9 bg-primary text-primary-foreground hover:bg-primary/90"
                size="sm"
              >
                <Plus className="w-4 h-4 mr-2" />
                New Chat
              </Button>
            </div>

            {/* Search and Filters */}
            <div className="px-2 py-2 space-y-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search threads..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9 h-8 bg-background border-sidebar-border focus-visible:ring-sidebar-ring"
                />
              </div>

              {/* Filter Dropdown */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm" className="w-full justify-between">
                    <div className="flex items-center gap-2">
                      <Filter className="h-4 w-4" />
                      Filters
                    </div>
                    {dateFilter !== 'all' && (
                      <div className="w-2 h-2 bg-primary rounded-full" />
                    )}
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="start" className="w-48">
                  <div className="p-2 space-y-2">
                    <div>
                      <label className="text-xs font-medium text-muted-foreground">Date</label>
                      <select
                        value={dateFilter}
                        onChange={(e) => setDateFilter(e.target.value as DateFilter)}
                        className="w-full mt-1 px-2 py-1 text-sm border rounded"
                      >
                        <option value="all">All time</option>
                        <option value="today">Today</option>
                        <option value="week">Last 7 days</option>
                        <option value="month">Last 30 days</option>
                      </select>
                    </div>
                  </div>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            {/* Thread List */}
            <div className="px-2">
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
                <div className="space-y-6">
                  {groupedThreads.today.length > 0 && (
                    <div>
                      <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 px-2">
                        Today
                      </h4>
                      {groupedThreads.today.map((thread) => (
                        <ThreadItem
                          key={thread.id}
                          thread={thread}
                          isActive={thread.id === currentThreadId}
                          onClick={() => handleThreadSelect(thread.id)}
                        />
                      ))}
                    </div>
                  )}
                  {groupedThreads.yesterday.length > 0 && (
                    <div>
                      <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 px-2">
                        Yesterday
                      </h4>
                      {groupedThreads.yesterday.map((thread) => (
                        <ThreadItem
                          key={thread.id}
                          thread={thread}
                          isActive={thread.id === currentThreadId}
                          onClick={() => handleThreadSelect(thread.id)}
                        />
                      ))}
                    </div>
                  )}
                  {groupedThreads.week.length > 0 && (
                    <div>
                      <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 px-2">
                        This Week
                      </h4>
                      {groupedThreads.week.map((thread) => (
                        <ThreadItem
                          key={thread.id}
                          thread={thread}
                          isActive={thread.id === currentThreadId}
                          onClick={() => handleThreadSelect(thread.id)}
                        />
                      ))}
                    </div>
                  )}
                  {groupedThreads.older.length > 0 && (
                    <div>
                      <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 px-2">
                        Older
                      </h4>
                      {groupedThreads.older.map((thread) => (
                        <ThreadItem
                          key={thread.id}
                          thread={thread}
                          isActive={thread.id === currentThreadId}
                          onClick={() => handleThreadSelect(thread.id)}
                        />
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <div className="p-2 text-xs text-muted-foreground text-center">
          LangGraph Integration
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}

// Thread Item Component
const ThreadItem = ({ thread, isActive, onClick }: {
  thread: Thread;
  isActive: boolean;
  onClick: () => void;
}) => {
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
};
