export interface ChatModel {
  id: string;
  name: string;
  description: string;
}

export const chatModels: ChatModel[] = [
  {
    id: 'gpt-4',
    name: 'GPT-4',
    description: 'Most capable model for complex tasks',
  },
  {
    id: 'gpt-3.5-turbo',
    name: 'GPT-3.5 Turbo',
    description: 'Fast and efficient for most tasks',
  },
];

export const DEFAULT_CHAT_MODEL = 'gpt-4';
