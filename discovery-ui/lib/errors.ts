export class ChatSDKError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ChatSDKError';
  }
}
