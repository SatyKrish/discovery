'use client';

import { forwardRef } from 'react';
import { cn } from '@/lib/utils';

export interface PromptInputProps extends React.HTMLAttributes<HTMLDivElement> {}

const PromptInput = forwardRef<HTMLDivElement, PromptInputProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        className={cn('flex flex-col border rounded-lg', className)}
        ref={ref}
        {...props}
      >
        {children}
      </div>
    );
  }
);
PromptInput.displayName = 'PromptInput';

const PromptInputTextarea = forwardRef<HTMLTextAreaElement, React.TextareaHTMLAttributes<HTMLTextAreaElement>>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn('flex min-h-[60px] w-full resize-none border-0 bg-transparent px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50', className)}
        ref={ref}
        {...props}
      />
    );
  }
);
PromptInputTextarea.displayName = 'PromptInputTextarea';

const PromptInputToolbar = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        className={cn('flex items-center justify-between border-t px-3 py-2', className)}
        ref={ref}
        {...props}
      >
        {children}
      </div>
    );
  }
);
PromptInputToolbar.displayName = 'PromptInputToolbar';

const PromptInputTools = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        className={cn('flex items-center gap-2', className)}
        ref={ref}
        {...props}
      >
        {children}
      </div>
    );
  }
);
PromptInputTools.displayName = 'PromptInputTools';

const PromptInputSubmit = forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <button
        className={cn('inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 w-10', className)}
        ref={ref}
        {...props}
      >
        {children}
      </button>
    );
  }
);
PromptInputSubmit.displayName = 'PromptInputSubmit';

const PromptInputModelSelect = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        className={cn('', className)}
        ref={ref}
        {...props}
      >
        {children}
      </div>
    );
  }
);
PromptInputModelSelect.displayName = 'PromptInputModelSelect';

const PromptInputModelSelectTrigger = forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <button
        className={cn('inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2', className)}
        ref={ref}
        {...props}
      >
        {children}
      </button>
    );
  }
);
PromptInputModelSelectTrigger.displayName = 'PromptInputModelSelectTrigger';

const PromptInputModelSelectContent = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        className={cn('absolute top-full z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md', className)}
        ref={ref}
        {...props}
      >
        {children}
      </div>
    );
  }
);
PromptInputModelSelectContent.displayName = 'PromptInputModelSelectContent';

export {
  PromptInput,
  PromptInputTextarea,
  PromptInputToolbar,
  PromptInputTools,
  PromptInputSubmit,
  PromptInputModelSelect,
  PromptInputModelSelectTrigger,
  PromptInputModelSelectContent,
};
