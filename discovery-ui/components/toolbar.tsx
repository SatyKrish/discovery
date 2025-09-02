'use client';

import { memo } from 'react';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { ChatMessage } from '@/lib/types';
import type { ArtifactKind } from './artifact';

function PureToolbar({
  isToolbarVisible,
  setIsToolbarVisible,
  sendMessage,
  status,
  stop,
  setMessages,
  artifactKind,
}: {
  isToolbarVisible: boolean;
  setIsToolbarVisible: (visible: boolean) => void;
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  status: UseChatHelpers<ChatMessage>['status'];
  stop: () => void;
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  artifactKind: ArtifactKind;
}) {
  if (!isToolbarVisible) return null;

  return (
    <div className="flex items-center gap-2 p-2 border-t">
      <span className="text-sm text-gray-500">Toolbar for {artifactKind}</span>
    </div>
  );
}

export const Toolbar = memo(PureToolbar);
