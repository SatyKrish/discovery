export interface Attachment {
  url: string;
  name: string;
  contentType: string;
}

import type { UIMessage } from 'ai';

export interface ChatMessage extends UIMessage {
  attachments?: Attachment[];
  createdAt?: Date;
}

export interface CustomUIDataTypes {
  'data-id': string;
  'data-title': string;
  'data-kind': string;
  'data-clear': boolean;
  'data-finish': boolean;
  [key: string]: any; // Add index signature for extensibility
}
