'use client';

import { isToday, isYesterday, subMonths, subWeeks } from 'date-fns';
import { useParams, useRouter } from 'next/navigation';
import type { User } from 'next-auth';
import { useState, useMemo } from 'react';
import { toast } from 'sonner';
import { motion } from 'framer-motion';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  useSidebar,
} from '@/components/ui/sidebar';
import type { Chat } from '@/lib/db/schema';
import { fetcher } from '@/lib/utils';
import { ChatItem } from './sidebar-history-item';
import useSWR from 'swr';
import { LoaderIcon, SearchIcon, PlusIcon } from './icons';
import { mockDb } from '@/lib/mock-db';
import { Input } from './ui/input';
import { Button } from './ui/button';
type GroupedChats = {
  today: Chat[];
  yesterday: Chat[];
  lastWeek: Chat[];
  lastMonth: Chat[];
  older: Chat[];
};

export interface ChatHistory {
  chats: Array<Chat>;
  hasMore: boolean;
}

const groupChatsByDate = (chats: Chat[]): GroupedChats => {
  const now = new Date();
  const oneWeekAgo = subWeeks(now, 1);
  const oneMonthAgo = subMonths(now, 1);

  return chats.reduce(
    (groups, chat) => {
      const chatDate = new Date(chat.createdAt);

      if (isToday(chatDate)) {
        groups.today.push(chat);
      } else if (isYesterday(chatDate)) {
        groups.yesterday.push(chat);
      } else if (chatDate > oneWeekAgo) {
        groups.lastWeek.push(chat);
      } else if (chatDate > oneMonthAgo) {
        groups.lastMonth.push(chat);
      } else {
        groups.older.push(chat);
      }

      return groups;
    },
    {
      today: [],
      yesterday: [],
      lastWeek: [],
      lastMonth: [],
      older: [],
    } as GroupedChats,
  );
};

export function SidebarHistory({ user }: { user: User | undefined }) {
  const { setOpenMobile } = useSidebar();
  const { id } = useParams();

  // Mock chat history instead of real database
  const { data: chatHistory, isLoading, mutate } = useSWR('mock-chat-history', mockDb.getChatHistory);

  const router = useRouter();
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Filter chats based on search query - must be called before any conditional returns
  const filteredChats = useMemo(() => {
    if (!chatHistory?.chats) {
      return [];
    }

    if (!searchQuery.trim()) {
      return chatHistory.chats;
    }

    return chatHistory.chats.filter((chat) =>
      chat.title.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [chatHistory?.chats, searchQuery]);

  const handleDelete = async () => {
    if (!deleteId) return;

    try {
      await mockDb.deleteChat(deleteId);
      // Refresh the chat history
      mutate();
      toast.success('Chat deleted successfully');
    } catch (error) {
      toast.error('Failed to delete chat');
    }

    setShowDeleteDialog(false);
    setDeleteId(null);

    if (deleteId === id) {
      router.push('/');
    }
  };

  if (!user) {
    return (
      <SidebarGroup>
        <SidebarGroupContent>
          <div className="flex flex-row gap-2 justify-center items-center px-2 w-full text-sm text-zinc-500">
            Login to save and revisit previous chats!
          </div>
        </SidebarGroupContent>
      </SidebarGroup>
    );
  }

  if (isLoading) {
    return (
      <SidebarGroup>
        <div className="px-2 py-1 text-xs text-sidebar-foreground/50">
          Today
        </div>
        <SidebarGroupContent>
          <div className="flex flex-col">
            {[44, 32, 28, 64, 52].map((item) => (
              <div
                key={item}
                className="flex gap-2 items-center px-2 h-8 rounded-md"
              >
                <div
                  className="h-4 rounded-md flex-1 max-w-[--skeleton-width] bg-sidebar-accent-foreground/10"
                  style={
                    {
                      '--skeleton-width': `${item}%`,
                    } as React.CSSProperties
                  }
                />
              </div>
            ))}
          </div>
        </SidebarGroupContent>
      </SidebarGroup>
    );
  }

  if (!chatHistory || !chatHistory.chats || chatHistory.chats.length === 0) {
    return (
      <SidebarGroup>
        <SidebarGroupContent>
          <div className="flex flex-row gap-2 justify-center items-center px-2 w-full text-sm text-zinc-500">
            Your conversations will appear here once you start chatting!
          </div>
        </SidebarGroupContent>
      </SidebarGroup>
    );
  }

  const groupedChats = groupChatsByDate(filteredChats);

  return (
    <>
      <SidebarGroup>
        <SidebarGroupContent>
          {/* New Chat Button */}
          <div className="px-2 py-2">
            <Button
              onClick={async () => {
                setOpenMobile(false);
                // Generate new chat ID and navigate to it
                const newChatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
                router.push(`/chat/${newChatId}`);
              }}
              className="w-full h-9 bg-primary text-primary-foreground hover:bg-primary/90"
              size="sm"
            >
              New Chat
            </Button>
          </div>

          {/* Search Input */}
          <div className="px-2 py-2">
            <div className="relative">
              <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search chats..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 h-8 bg-background border-sidebar-border focus-visible:ring-sidebar-ring"
              />
            </div>
          </div>

          <SidebarMenu>
            <div className="flex flex-col gap-6">
              {filteredChats.length === 0 && searchQuery.trim() ? (
                <div className="px-2 py-4 text-center text-sm text-muted-foreground">
                  No chats found matching "{searchQuery}"
                </div>
              ) : (
                <>
                  {groupedChats.today.length > 0 && (
                    <div>
                      <SidebarGroupLabel className="px-2 py-1 text-xs">
                        Today
                      </SidebarGroupLabel>
                      {groupedChats.today.map((chat) => (
                        <ChatItem
                          key={chat.id}
                          chat={chat}
                          isActive={chat.id === id}
                          onDelete={(chatId: string) => {
                            setDeleteId(chatId);
                            setShowDeleteDialog(true);
                          }}
                          setOpenMobile={setOpenMobile}
                        />
                      ))}
                    </div>
                  )}

                  {groupedChats.yesterday.length > 0 && (
                    <div>
                      <SidebarGroupLabel className="px-2 py-1 text-xs">
                        Yesterday
                      </SidebarGroupLabel>
                      {groupedChats.yesterday.map((chat) => (
                        <ChatItem
                          key={chat.id}
                          chat={chat}
                          isActive={chat.id === id}
                          onDelete={(chatId: string) => {
                            setDeleteId(chatId);
                            setShowDeleteDialog(true);
                          }}
                          setOpenMobile={setOpenMobile}
                        />
                      ))}
                    </div>
                  )}

                  {groupedChats.lastWeek.length > 0 && (
                    <div>
                      <SidebarGroupLabel className="px-2 py-1 text-xs">
                        Last 7 days
                      </SidebarGroupLabel>
                      {groupedChats.lastWeek.map((chat) => (
                        <ChatItem
                          key={chat.id}
                          chat={chat}
                          isActive={chat.id === id}
                          onDelete={(chatId: string) => {
                            setDeleteId(chatId);
                            setShowDeleteDialog(true);
                          }}
                          setOpenMobile={setOpenMobile}
                        />
                      ))}
                    </div>
                  )}

                  {groupedChats.lastMonth.length > 0 && (
                    <div>
                      <SidebarGroupLabel className="px-2 py-1 text-xs">
                        Last 30 days
                      </SidebarGroupLabel>
                      {groupedChats.lastMonth.map((chat) => (
                        <ChatItem
                          key={chat.id}
                          chat={chat}
                          isActive={chat.id === id}
                          onDelete={(chatId: string) => {
                            setDeleteId(chatId);
                            setShowDeleteDialog(true);
                          }}
                          setOpenMobile={setOpenMobile}
                        />
                      ))}
                    </div>
                  )}

                  {groupedChats.older.length > 0 && (
                    <div>
                      <SidebarGroupLabel className="px-2 py-1 text-xs">
                        Older than last month
                      </SidebarGroupLabel>
                      {groupedChats.older.map((chat) => (
                        <ChatItem
                          key={chat.id}
                          chat={chat}
                          isActive={chat.id === id}
                          onDelete={(chatId: string) => {
                            setDeleteId(chatId);
                            setShowDeleteDialog(true);
                          }}
                          setOpenMobile={setOpenMobile}
                        />
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>

      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete your
              chat and remove it from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete}>
              Continue
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
