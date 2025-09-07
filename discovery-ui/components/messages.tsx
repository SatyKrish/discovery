'use client';

import { memo } from 'react';
import type { Vote } from '@/lib/db/schema';
import equal from 'fast-deep-equal';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { ChatMessage } from '@/lib/types';
import type { UIMessage } from 'ai';
import { ChatMessageBubble } from './ChatMessageBubble';

interface MessagesProps {
  chatId: string;
  status: UseChatHelpers<ChatMessage>['status'];
  votes: Array<Vote> | undefined;
  messages: Array<ChatMessage>;
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  regenerate: UseChatHelpers<ChatMessage>['regenerate'];
  isReadonly: boolean;
  isArtifactVisible: boolean;
}

function PureMessages({
  chatId,
  status,
  votes,
  messages,
  setMessages,
  regenerate,
  isReadonly,
  isArtifactVisible,
}: MessagesProps) {
  return (
    <div className="flex-1 bg-background">
      <div className="flex flex-col min-w-0 gap-6 pt-4 pb-32 px-4 max-w-4xl mx-auto">
        <div className="flex flex-col gap-6">
          {messages.length === 0 && (
            <div className="max-w-3xl mx-auto md:mt-20 px-8 size-full flex flex-col justify-center">
              <div className="text-2xl font-semibold text-foreground">Hello there!</div>
              <div className="text-2xl text-muted-foreground">How can I help you today?</div>
            </div>
          )}

          {messages.map((message, index) => (
            <ChatMessageBubble key={message.id} message={message} />
          ))}

          {status === 'submitted' && messages.length > 0 && messages[messages.length - 1].role === 'user' && (
            <div className="chat-message-bubble rounded-[24px] max-w-[100%] mb-8 flex mr-auto">
              <div className="whitespace-pre-wrap flex flex-col prose max-w-none overflow-x-auto">
                <div className="flex items-center gap-2 p-3">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
                  <span className="text-sm text-muted-foreground">Thinking...</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export const Messages = memo(PureMessages, (prevProps, nextProps) => {
  if (prevProps.isArtifactVisible && nextProps.isArtifactVisible) return true;

  if (prevProps.status !== nextProps.status) return false;
  if (prevProps.messages.length !== nextProps.messages.length) return false;
  if (!equal(prevProps.messages, nextProps.messages)) return false;
  if (!equal(prevProps.votes, nextProps.votes)) return false;

  return false;
});
