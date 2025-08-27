import type { Chat, Message } from "@/lib/provider";

const store = {
  chats: [{ id: "demo", title: "Welcome", lastActivity: "just now" }] as Chat[],
  messages: new Map<string, Message[]>([
    ["demo", [
      { id: "m1", role: "agent", text: "Ask me anything.", createdAt: new Date().toISOString() }
    ]]
  ])
};

export function getChats() { return store.chats; }
export function getMessages(chatId: string) { return store.messages.get(chatId) ?? []; }
export function addMessage(chatId: string, msg: Message) {
  const list = store.messages.get(chatId) ?? [];
  list.push(msg);
  store.messages.set(chatId, list);
}
