'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Bot, Plus, Search, Filter } from 'lucide-react';

import { ThreadHistorySidebar } from '@/components/ThreadHistorySidebar';
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
import Link from 'next/link';

interface AppSidebarProps {
  currentThreadId?: string | null;
  onThreadSelect?: (threadId: string) => void;
  onNewThread?: () => void;
}

type DateFilter = 'all' | 'today' | 'week' | 'month';

export function AppSidebar({ currentThreadId = null, onThreadSelect, onNewThread }: AppSidebarProps) {
  const router = useRouter();
  const { setOpenMobile, toggleSidebar } = useSidebar();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [dateFilter, setDateFilter] = useState<DateFilter>('all');

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

            {/* Thread History */}
            <div className="px-2">
              <ThreadHistorySidebar
                open={sidebarOpen}
                setOpen={setSidebarOpen}
                currentThreadId={currentThreadId}
                onThreadSelect={handleThreadSelect}
                searchQuery={searchQuery}
                dateFilter={dateFilter}
              />
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
