'use client';

import { memo } from 'react';
import type { VisibilityType } from './visibility-selector';
import type { Session } from 'next-auth';

function PureChatHeader({
  chatId,
  selectedVisibilityType,
  isReadonly,
  session,
}: {
  chatId: string;
  selectedVisibilityType: VisibilityType;
  isReadonly: boolean;
  session: Session;
}) {
  return (
    <header className="flex sticky top-0 bg-background py-1.5 items-center px-2 md:px-2 gap-2">
      <div className="flex items-center justify-between w-full">
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white text-xs font-bold">AI</span>
          </div>
          <h1 className="text-xl font-semibold">Discovery AI</h1>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <span>Workflow: {chatId.slice(0, 8)}...</span>
        </div>
      </div>
    </header>
  );
}

export const ChatHeader = memo(PureChatHeader, (prevProps, nextProps) => {
  return (
    prevProps.chatId === nextProps.chatId &&
    prevProps.selectedVisibilityType === nextProps.selectedVisibilityType &&
    prevProps.isReadonly === nextProps.isReadonly
  );
});
