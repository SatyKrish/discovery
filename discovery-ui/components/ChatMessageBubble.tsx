import type { ChatMessage } from '@/lib/types';
import { MemoizedMarkdown } from './MemoizedMarkdown';
import { cn } from '@/lib/utils';

export function ChatMessageBubble(props: { message: ChatMessage; aiEmoji?: string }) {
  return (
    <div
      className={cn(
        `rounded-[24px] max-w-[100%] mb-8 flex`,
        props.message.role === 'user' ? 'bg-secondary text-secondary-foreground px-4 py-2' : null,
        props.message.role === 'user' ? 'ml-auto' : 'mr-auto',
      )}
    >
      <div className="chat-message-bubble whitespace-pre-wrap flex flex-col prose max-w-none overflow-x-auto">
        <MemoizedMarkdown
          content={props.message.parts?.find(part => part.type === 'text')?.text || 'Message content'}
          id={props.message.id}
        />
      </div>
    </div>
  );
}
