'use client';

import { memo } from 'react';
import type { Vote } from '@/lib/db/schema';
import equal from 'fast-deep-equal';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { ChatMessage } from '@/lib/types';

interface MessagesProps {
  chatId: string;
  status: UseChatHelpers<ChatMessage>['status'];
  votes: Array<Vote> | undefined;
  messages: ChatMessage[];
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
    <div className="flex-1 overflow-y-auto">
      <div className="flex flex-col min-w-0 gap-6 pt-4 pb-32 px-4 max-w-4xl mx-auto">
        <div className="flex flex-col gap-6">
          {messages.length === 0 && (
            <div className="max-w-3xl mx-auto md:mt-20 px-8 size-full flex flex-col justify-center">
              <div className="text-2xl font-semibold">Hello there!</div>
              <div className="text-2xl text-zinc-500">How can I help you today?</div>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={message.id} className="flex gap-3">
              <div className="flex-1">
                <div className={`flex gap-2 max-w-[70%] ${message.role === 'user' ? 'justify-end ml-auto' : 'justify-start'}`}>
                  <div className={`rounded-lg p-3 ${message.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white border'}`}>
                    <p className="text-sm">
                      {message.parts?.find(part => part.type === 'text')?.text || 'Message content'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {status === 'submitted' && messages.length > 0 && messages[messages.length - 1].role === 'user' && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                <div className="w-4 h-4 bg-white rounded-full animate-pulse"></div>
              </div>
              <div className="bg-white border rounded-lg p-3">
                <div className="flex items-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                  <span className="text-sm text-gray-500">Thinking...</span>
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
