import { Chat } from '@/components/chat';
import { DEFAULT_CHAT_MODEL } from '@/lib/ai/models';
import { generateUUID } from '@/lib/utils';
import { DataStreamHandler } from '@/components/data-stream-handler';
import { DataStreamProvider } from '@/components/data-stream-provider';

export default function Page() {
  const id = generateUUID();

  // Mock session for now - will be replaced with Discovery Agent auth
  const mockSession = {
    user: {
      id: 'guest',
      email: 'guest@example.com',
      name: 'Guest User',
    },
    expires: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
  };

  return (
    <DataStreamProvider>
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
      <DataStreamHandler />
    </DataStreamProvider>
  );
}
