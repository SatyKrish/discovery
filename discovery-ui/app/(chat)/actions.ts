'use server';

import { cookies } from 'next/headers';

export async function saveChatModelAsCookie(modelId: string) {
  const cookieStore = await cookies();
  cookieStore.set('chat-model', modelId);
}
