export interface MockChat {
  id: string;
  title: string;
  userId: string;
  createdAt: Date;
  visibility: 'public' | 'private';
}

const mockChats: MockChat[] = [
  {
    id: 'chat-1',
    userId: 'guest-user-123',
    title: 'Getting Started with Discovery',
    createdAt: new Date(),
    visibility: 'private',
  },
  {
    id: 'chat-2',
    userId: 'guest-user-123',
    title: 'Project Planning Discussion',
    createdAt: new Date(Date.now() - 86400000), // Yesterday
    visibility: 'private',
  },
  {
    id: 'chat-3',
    userId: 'guest-user-123',
    title: 'Technical Architecture Review',
    createdAt: new Date(Date.now() - 172800000), // 2 days ago
    visibility: 'private',
  },
  {
    id: 'chat-4',
    userId: 'guest-user-123',
    title: 'UI/UX Design Feedback',
    createdAt: new Date(Date.now() - 259200000), // 3 days ago
    visibility: 'private',
  },
  {
    id: 'chat-5',
    userId: 'guest-user-123',
    title: 'Database Schema Discussion',
    createdAt: new Date(Date.now() - 345600000), // 4 days ago
    visibility: 'private',
  },
];

export const mockDb = {
  getChatHistory: async () => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300));
    return { chats: mockChats, hasMore: false };
  },

  createChat: async (chatData: Omit<MockChat, 'createdAt'>) => {
    await new Promise(resolve => setTimeout(resolve, 200));
    const newChat: MockChat = {
      ...chatData,
      createdAt: new Date(),
    };
    mockChats.unshift(newChat); // Add to beginning of array
    return newChat;
  },

  deleteChat: async (chatId: string) => {
    await new Promise(resolve => setTimeout(resolve, 200));
    // Remove from mock data
    const index = mockChats.findIndex(chat => chat.id === chatId);
    if (index > -1) {
      mockChats.splice(index, 1);
    }
    return { success: true };
  },

  updateChatVisibility: async (chatId: string, visibility: 'public' | 'private') => {
    await new Promise(resolve => setTimeout(resolve, 200));
    // Update in mock data
    const chat = mockChats.find(c => c.id === chatId);
    if (chat) {
      chat.visibility = visibility;
    }
    return { success: true };
  },
};
