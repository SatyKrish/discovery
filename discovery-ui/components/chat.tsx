'use client';

import { DefaultChatTransport } from 'ai';
import { useChat } from '@ai-sdk/react';
import { useEffect, useRef, useState } from 'react';
import { ChatHeader } from '@/components/chat-header';
import type { Vote } from '@/lib/db/schema';
import { fetchWithErrorHandlers, generateUUID } from '@/lib/utils';
import { Artifact } from './artifact';
import { MultimodalInput } from './multimodal-input';
import { Messages } from './messages';
import type { VisibilityType } from './visibility-selector';
import { useArtifactSelector } from '@/hooks/use-artifact';
import { toast } from './toast';
import type { Session } from 'next-auth';
import { useSearchParams } from 'next/navigation';
import { useAutoResume } from '@/hooks/use-auto-resume';
import { ChatSDKError } from '@/lib/errors';
import type { Attachment, ChatMessage } from '@/lib/types';
import { useDataStream } from './data-stream-provider';

export function Chat({
  id,
  initialMessages,
  initialChatModel,
  initialVisibilityType,
  isReadonly,
  session,
  autoResume,
}: {
  id: string;
  initialMessages: ChatMessage[];
  initialChatModel: string;
  initialVisibilityType: VisibilityType;
  isReadonly: boolean;
  session: Session;
  autoResume: boolean;
}) {
  // Keep visibility simple since DB is removed
  const visibilityType = initialVisibilityType;

  const { setDataStream } = useDataStream();

  const [input, setInput] = useState<string>('');

  const {
    messages,
    setMessages,
    sendMessage,
    status,
    stop,
    regenerate,
    resumeStream,
  } = useChat<ChatMessage>({
    id,
    messages: initialMessages,
    experimental_throttle: 100,
    generateId: generateUUID,
    transport: new DefaultChatTransport({
      api: '/api/chat',
      fetch: async (input, init) => {
        try {
          const response = await fetch(input as RequestInfo, init as RequestInit);
          return response;
        } catch (error) {
          throw error;
        }
      },
      prepareSendMessagesRequest({ messages, id, body }) {

        // Convert AI SDK message format to backend expected format
        const formattedMessages = messages.map(msg => ({
          id: msg.id,
          role: msg.role,
          parts: msg.parts || [{ type: 'text', text: (msg as any).content || '' }],
          createdAt: (msg as any).createdAt || new Date().toISOString(),
        }));

        return {
          body: {
            id,
            messages: formattedMessages,
            selectedChatModel: initialChatModel,
            selectedVisibilityType: visibilityType,
            ...body,
          },
        };
      },
    }),
    onData: (dataPart) => {
      // pipe data UI parts to the artifact side panel
      setDataStream((ds) => (ds ? [...ds, dataPart] : [dataPart]));
    },
    onFinish: () => {
      // sidebar history mutation intentionally removed in this mock build
    },
    onError: (error) => {
      if (error instanceof ChatSDKError) {
        toast({
          type: 'error',
          description: error.message,
        });
      }
    },
  });

  const searchParams = useSearchParams();
  const query = searchParams.get('query');

  const [hasAppendedQuery, setHasAppendedQuery] = useState(false);

  useEffect(() => {
    if (query && !hasAppendedQuery) {
      sendMessage({
        role: 'user',
        parts: [{ type: 'text', text: query }],
      });
      setHasAppendedQuery(true);
      window.history.replaceState({}, '', `/chat/${id}`);
    }
  }, [query, hasAppendedQuery, id, sendMessage]);

  // Clear any cached data for new chats
  useEffect(() => {
    if (messages.length === 0 && !hasAppendedQuery) {
      // Clear any existing chat data for this session
      localStorage.removeItem(`chat-${id}`);
      sessionStorage.removeItem(`chat-${id}`);
    }
  }, [id, messages.length, hasAppendedQuery]);

  // Mock votes since DB is removed
  const votes: Array<Vote> | undefined = undefined;

  const [attachments, setAttachments] = useState<Array<Attachment>>([]);
  const isArtifactVisible = useArtifactSelector((state) => state.isVisible);

  useAutoResume({
    autoResume,
    initialMessages,
    resumeStream,
    setMessages,
  });

  // --- auto-scroll refs and state
  const listRef = useRef<HTMLDivElement | null>(null);
  const endRef = useRef<HTMLDivElement | null>(null);
  const [isAtBottom, setIsAtBottom] = useState(true);

  // Track if user is at bottom of chat
  useEffect(() => {
    const el = listRef.current;
    if (!el) return;

    const onScroll = () => {
      const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 8;
      setIsAtBottom(atBottom);
    };

    el.addEventListener('scroll', onScroll);
    return () => el.removeEventListener('scroll', onScroll);
  }, []);

  // Auto-scroll when messages update or streaming status changes
  useEffect(() => {
    if (isAtBottom) {
      endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [messages, status, isAtBottom]);

  return (
    <div className="flex h-dvh bg-background">
      {/* Main Content Area */}
      <div className="flex flex-col flex-1 min-w-0 min-h-0">
        {/* Header */}
        <div className="w-full">
          <ChatHeader
            chatId={id}
            selectedVisibilityType={initialVisibilityType}
            isReadonly={isReadonly}
            session={session}
            selectedModelId={initialChatModel}
          />
        </div>

        {/* Messages */}
        <div
          ref={listRef}
          className="flex-1 min-h-0 overflow-y-auto scroll-smooth overscroll-contain"
        >
          <Messages
            chatId={id}
            status={status}
            votes={votes}
            messages={messages}
            setMessages={setMessages}
            regenerate={regenerate}
            isReadonly={isReadonly}
            isArtifactVisible={isArtifactVisible}
          />
          {/* anchor at the very bottom to scrollIntoView */}
          <div ref={endRef} />
        </div>

        {/* Input */}
        <div className="flex-shrink-0">
          <div className="mx-auto w-full max-w-4xl px-4 py-4 md:px-6 md:py-6">
            {!isReadonly && (
              <MultimodalInput
                chatId={id}
                input={input}
                setInput={setInput}
                status={status}
                stop={stop}
                attachments={attachments}
                setAttachments={setAttachments}
                messages={messages}
                setMessages={setMessages}
                sendMessage={sendMessage}
                selectedVisibilityType={visibilityType}
                selectedModelId={initialChatModel}
              />
            )}
          </div>
        </div>
      </div>

      {/* Artifact Panel */}
      <Artifact
        chatId={id}
        input={input}
        setInput={setInput}
        status={status}
        stop={stop}
        attachments={attachments}
        setAttachments={setAttachments}
        sendMessage={sendMessage}
        messages={messages}
        setMessages={setMessages}
        regenerate={regenerate}
        votes={votes}
        isReadonly={isReadonly}
        selectedVisibilityType={visibilityType}
        selectedModelId={initialChatModel}
      />
    </div>
  );
}
