'use client';

import { useState, useEffect } from 'react';
import { Button } from './ui/button';

import { Pencil, Search, MessageSquare, Trash2, Menu, X } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface Chat {
  id: string;
  title: string;
  lastActivity?: string;
}

interface SidebarProps {
  chats: Chat[];
  selectedChatId?: string;
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void;
  onDeleteChat: (chatId: string) => void;
  isOpen: boolean;
  onToggle: () => void;
  isLoading?: boolean;
}

export function Sidebar({
  chats,
  selectedChatId,
  onSelectChat,
  onNewChat,
  onDeleteChat,
  isOpen,
  onToggle,
  isLoading = false,
}: SidebarProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const filteredChats = chats.filter(chat =>
    chat.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleNewChat = () => {
    onNewChat();
    if (window.innerWidth < 768) {
      onToggle(); // Close sidebar on mobile after creating new chat
    }
  };

  const handleSelectChat = (chatId: string) => {
    onSelectChat(chatId);
    if (window.innerWidth < 768) {
      onToggle(); // Close sidebar on mobile after selecting chat
    }
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar */}
      <div
        className={`
          fixed left-0 top-0 h-full bg-background border-r border-border z-50
          transition-transform duration-300 ease-in-out
          w-80
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
          md:relative md:translate-x-0 md:z-auto
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-bold">AI</span>
            </div>
            <h2 className="text-lg font-semibold text-foreground">Discovery AI</h2>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={onToggle}
            className="md:hidden"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>

        {/* Actions */}
        <div className="p-4 space-y-2">
          <Button
            onClick={handleNewChat}
            className="w-full justify-start gap-2"
            variant="outline"
          >
            <Pencil className="h-4 w-4" />
            New Chat
          </Button>

          <Link href="/library" className="block">
            <Button
              variant="ghost"
              className="w-full justify-start gap-2"
              onClick={() => window.innerWidth < 768 && onToggle()}
            >
              <MessageSquare className="h-4 w-4" />
              Library
            </Button>
          </Link>
        </div>

        {/* Search */}
        <div className="px-4 pb-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search chats..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 text-sm bg-muted border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
        </div>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto px-2">
          <div className="space-y-1 py-2">
            {isLoading ? (
              // Loading skeleton
              Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="h-12 bg-muted rounded-md animate-pulse mx-2" />
              ))
            ) : filteredChats.length === 0 ? (
              <div className="text-center text-muted-foreground py-8">
                {searchQuery ? 'No chats found' : 'No chats yet'}
              </div>
            ) : (
              filteredChats.map((chat) => (
                <div
                  key={chat.id}
                  className={`
                    group flex items-center gap-2 p-3 rounded-md cursor-pointer
                    hover:bg-muted transition-colors
                    ${selectedChatId === chat.id ? 'bg-muted border border-border' : ''}
                  `}
                  onClick={() => handleSelectChat(chat.id)}
                >
                  <MessageSquare className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-foreground truncate">
                      {chat.title}
                    </div>
                    {chat.lastActivity && (
                      <div className="text-xs text-muted-foreground">
                        {new Date(chat.lastActivity).toLocaleDateString()}
                      </div>
                    )}
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm(`Delete chat "${chat.title}"?`)) {
                        onDeleteChat(chat.id);
                      }
                    }}
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </>
  );
}
