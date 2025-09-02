import { redirect } from 'next/navigation';

export default function Page() {
  // Generate new chat ID and redirect to it
  const newChatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  redirect(`/chat/${newChatId}`);
}
