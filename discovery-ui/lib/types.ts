export interface Attachment {
  url: string;
  name: string;
  contentType: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  parts: Array<{
    type: 'text' | 'file';
    text?: string;
    url?: string;
    name?: string;
    mediaType?: string;
  }>;
  attachments?: Attachment[];
  createdAt?: Date;
}

export interface CustomUIDataTypes {
  'data-id': string;
  'data-title': string;
  'data-kind': string;
  'data-clear': boolean;
  'data-finish': boolean;
}
