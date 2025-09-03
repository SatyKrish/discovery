'use client';

import type { UIMessage } from 'ai';
import {
  useRef,
  useEffect,
  useState,
  useCallback,
  type Dispatch,
  type SetStateAction,
  type ChangeEvent,
  memo,
} from 'react';
import { toast } from 'sonner';
import { useLocalStorage, useWindowSize } from 'usehooks-ts';

import { ArrowUpIcon, PaperclipIcon, StopIcon } from './icons';
import { Button } from './ui/button';
import {
  PromptInput,
  PromptInputTextarea,
  PromptInputToolbar,
  PromptInputTools,
  PromptInputSubmit,
} from './elements/prompt-input';
import equal from 'fast-deep-equal';
import type { UseChatHelpers } from '@ai-sdk/react';
import { AnimatePresence, motion } from 'framer-motion';
import { ArrowDown } from 'lucide-react';

import type { VisibilityType } from './visibility-selector';
import type { Attachment, ChatMessage } from '@/lib/types';
import { startTransition } from 'react';
import { SuggestedActions } from './suggested-actions';

function PureMultimodalInput({
  chatId,
  input,
  setInput,
  status,
  stop,
  attachments,
  setAttachments,
  messages,
  setMessages,
  sendMessage,
  className,
  selectedVisibilityType,
  selectedModelId,
  isAtBottom,
  onScrollToBottom,
}: {
  chatId: string;
  input: string;
  setInput: Dispatch<SetStateAction<string>>;
  status: UseChatHelpers<ChatMessage>['status'];
  stop: () => void;
  attachments: Array<Attachment>;
  setAttachments: Dispatch<SetStateAction<Array<Attachment>>>;
  messages: Array<UIMessage>;
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  className?: string;
  selectedVisibilityType: VisibilityType;
  selectedModelId: string;
  isAtBottom: boolean;
  onScrollToBottom: () => void;
}) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { width } = useWindowSize();

  useEffect(() => {
    if (textareaRef.current) {
      adjustHeight();
    }
  }, []);

  const adjustHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = '72px';
    }
  };

  const resetHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = '72px';
    }
  };

  const [localStorageInput, setLocalStorageInput] = useLocalStorage(
    'input',
    '',
  );

  useEffect(() => {
    if (textareaRef.current) {
      const domValue = textareaRef.current.value;
      // Prefer DOM value over localStorage to handle hydration
      const finalValue = domValue || localStorageInput || '';
      setInput(finalValue);
      adjustHeight();
    }
    // Only run once after hydration
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setLocalStorageInput(input);
  }, [input, setLocalStorageInput]);

  const handleInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    console.log('handleInput called with value:', event.target.value);
    setInput(event.target.value);
  };

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploadQueue, setUploadQueue] = useState<Array<string>>([]);

  const submitForm = useCallback(async () => {
    console.log('🚀 submitForm called with input:', input);
    console.log('🚀 sendMessage function exists:', typeof sendMessage);

    if (!input.trim() && attachments.length === 0) {
      console.log('⚠️ No input or attachments, skipping send');
      return;
    }

    window.history.replaceState({}, '', `/chat/${chatId}`);

    const messageParts = [
      ...attachments.map((attachment) => ({
        type: 'file' as const,
        url: attachment.url,
        name: attachment.name,
        mediaType: attachment.contentType,
      })),
      ...(input.trim() ? [{
        type: 'text' as const,
        text: input,
      }] : []),
    ];

    console.log('🚀 Sending message with parts:', messageParts);

    try {
      await sendMessage({
        role: 'user',
        parts: messageParts,
      });
      console.log('✅ sendMessage called successfully');

      // Clear form after successful send
      setAttachments([]);
      setLocalStorageInput('');
      resetHeight();
      setInput('');

      if (width && width > 768) {
        textareaRef.current?.focus();
      }
    } catch (error) {
      console.error('❌ Error calling sendMessage:', error);
      toast.error('Failed to send message. Please try again.');
    }
  }, [
    input,
    setInput,
    attachments,
    sendMessage,
    setAttachments,
    setLocalStorageInput,
    width,
    chatId,
  ]);

  const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/files/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        const { url, pathname, contentType } = data;

        return {
          url,
          name: pathname,
          contentType: contentType,
        };
      }
      const { error } = await response.json();
      toast.error(error);
    } catch (error) {
      toast.error('Failed to upload file, please try again!');
    }
  };

  const handleFileChange = useCallback(
    async (event: ChangeEvent<HTMLInputElement>) => {
      const files = Array.from(event.target.files || []);

      setUploadQueue(files.map((file) => file.name));

      try {
        const uploadPromises = files.map((file) => uploadFile(file));
        const uploadedAttachments = await Promise.all(uploadPromises);
        const successfullyUploadedAttachments = uploadedAttachments.filter(
          (attachment) => attachment !== undefined,
        );

        setAttachments((currentAttachments) => [
          ...currentAttachments,
          ...successfullyUploadedAttachments,
        ]);
      } catch (error) {
        console.error('Error uploading files!', error);
      } finally {
        setUploadQueue([]);
      }
    },
    [setAttachments],
  );



  return (
    <div className="flex relative flex-col gap-4 w-full">
      <AnimatePresence>
        {!isAtBottom && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            className="absolute bottom-28 left-1/2 z-50 -translate-x-1/2"
          >
            <Button
              data-testid="scroll-to-bottom-button"
              className="rounded-full"
              size="icon"
              variant="outline"
              onClick={(event) => {
                event.preventDefault();
                onScrollToBottom();
              }}
            >
              <ArrowDown />
            </Button>
          </motion.div>
        )}
      </AnimatePresence>

      {messages.length === 0 &&
        attachments.length === 0 &&
        uploadQueue.length === 0 && (
          <SuggestedActions onActionClick={(action) => setInput(action)} />
        )}

      <input
        type="file"
        className="fixed -top-4 -left-4 size-0.5 opacity-0 pointer-events-none"
        ref={fileInputRef}
        multiple
        onChange={handleFileChange}
        tabIndex={-1}
      />

      <form
        className="bg-muted/50 rounded-3xl border shadow-none transition-all duration-200 hover:ring-1 hover:ring-primary/30 focus-within:ring-1 focus-within:ring-primary/50 flex flex-col"
        onSubmit={(event) => {
          console.log('📝 Form onSubmit called');
          console.log('📝 Event type:', event.type);
          console.log('📝 Status:', status);
          event.preventDefault();
          if (status !== 'ready') {
            console.log('⚠️ Status is not ready, showing error');
            toast.error('Please wait for the model to finish its response!');
          } else {
            console.log('✅ Calling submitForm');
            submitForm();
          }
        }}
      >
        {(attachments.length > 0 || uploadQueue.length > 0) && (
          <div
            data-testid="attachments-preview"
            className="flex overflow-x-scroll flex-row gap-2 items-end px-3 py-2"
          >
            {attachments.map((attachment) => (
              <div key={attachment.url} className="text-sm">
                {attachment.name}
              </div>
            ))}

            {uploadQueue.map((filename) => (
              <div key={filename} className="text-sm text-muted-foreground">
                Uploading {filename}...
              </div>
            ))}
          </div>
        )}

        <PromptInputTextarea
          data-testid="multimodal-input"
          ref={textareaRef}
          placeholder="Send a message..."
          value={input}
          onChange={handleInput}
          className="text-base resize-none py-4 px-4 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none] bg-transparent !border-0 !border-none outline-none ring-0 focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:outline-none"
          rows={1}
          autoFocus
        />
        <PromptInputToolbar className="px-4 py-2 !border-t-0 !border-top-0 shadow-none dark:!border-transparent dark:border-0">
          <PromptInputTools className="gap-2">
            <AttachmentsButton fileInputRef={fileInputRef} status={status} />
          </PromptInputTools>
          {status === 'submitted' ? (
            <StopButton stop={stop} setMessages={setMessages} />
          ) : (
            <PromptInputSubmit
              data-testid="send-button"
              disabled={!input.trim() || uploadQueue.length > 0}
              className="p-3 text-primary-foreground bg-primary rounded-full hover:bg-primary/90"
            >
              <ArrowUpIcon size={20} />
            </PromptInputSubmit>
          )}
        </PromptInputToolbar>
      </form>
    </div>
  );
}

export const MultimodalInput = memo(
  PureMultimodalInput,
  (prevProps, nextProps) => {
    if (prevProps.input !== nextProps.input) return false;
    if (prevProps.status !== nextProps.status) return false;
    if (!equal(prevProps.attachments, nextProps.attachments)) return false;
    if (prevProps.selectedVisibilityType !== nextProps.selectedVisibilityType)
      return false;
    if (prevProps.isAtBottom !== nextProps.isAtBottom) return false;

    return true;
  },
);

function PureAttachmentsButton({
  fileInputRef,
  status,
}: {
  fileInputRef: React.MutableRefObject<HTMLInputElement | null>;
  status: UseChatHelpers<ChatMessage>['status'];
}) {
  return (
    <Button
      data-testid="attachments-button"
      className="rounded-md rounded-bl-lg p-[7px] h-fit dark:border-zinc-700 hover:dark:bg-zinc-900 hover:bg-zinc-200"
      onClick={(event) => {
        event.preventDefault();
        fileInputRef.current?.click();
      }}
      disabled={status !== 'ready'}
      variant="ghost"
    >
      <PaperclipIcon size={14} />
    </Button>
  );
}

const AttachmentsButton = memo(PureAttachmentsButton);



function PureStopButton({
  stop,
  setMessages,
}: {
  stop: () => void;
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
}) {
  return (
    <Button
      data-testid="stop-button"
      className="rounded-full p-1.5 h-fit border dark:border-zinc-600"
      onClick={(event) => {
        event.preventDefault();
        stop();
        setMessages((messages) => messages);
      }}
    >
      <StopIcon size={14} />
    </Button>
  );
}

const StopButton = memo(PureStopButton);

function PureSendButton({
  submitForm,
  input,
  uploadQueue,
}: {
  submitForm: () => void;
  input: string;
  uploadQueue: Array<string>;
}) {
  return (
    <Button
      data-testid="send-button"
      className="rounded-full p-1.5 h-fit border dark:border-zinc-600"
      onClick={(event) => {
        event.preventDefault();
        submitForm();
      }}
      disabled={input.length === 0 || uploadQueue.length > 0}
    >
      <ArrowUpIcon size={14} />
    </Button>
  );
}

const SendButton = memo(PureSendButton, (prevProps, nextProps) => {
  if (prevProps.uploadQueue.length !== nextProps.uploadQueue.length)
    return false;
  if (prevProps.input !== nextProps.input) return false;
  return true;
});
