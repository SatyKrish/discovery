'use client';

import { Chat } from '@/components/chat';
import { DEFAULT_CHAT_MODEL } from '@/lib/ai/models';
import { useEffect } from 'react';
import { useParams } from 'next/navigation';

export default function Page() {
  const { id } = useParams<{ id: string }>();

  // Mock session for now - will be replaced with Discovery Agent auth
  const mockSession = {
    user: {
      id: 'guest',
      email: 'guest@example.com',
      name: 'Guest User',
    },
    expires: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
  };

  // Clear any cached data when component mounts
  useEffect(() => {
    if (typeof window !== 'undefined' && id) {
      // Clear any existing chat data for this session
      localStorage.removeItem(`chat-${id}`);
      sessionStorage.removeItem(`chat-${id}`);
      // Also clear any AI SDK cached data
      localStorage.removeItem(`ai-chat-${id}`);
      sessionStorage.removeItem(`ai-chat-${id}`);
    }
  }, [id]);

  return (
    <Chat
      key={id}
      id={id}
      initialMessages={[]}
      initialChatModel={DEFAULT_CHAT_MODEL}
      initialVisibilityType="private"
      isReadonly={false}
      session={mockSession}
      autoResume={false}
    />
  );
}
