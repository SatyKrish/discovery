'use client';

import { memo, useEffect, useState } from 'react';
import { Moon, Sun, Monitor } from 'lucide-react';
import { Button } from './ui/button';
import { useTheme } from './theme-provider';
import type { VisibilityType } from './visibility-selector';
import type { Session } from 'next-auth';

function PureChatHeader({
  chatId,
  selectedVisibilityType,
  isReadonly,
  session,
  selectedModelId,
}: {
  chatId: string;
  selectedVisibilityType: VisibilityType;
  isReadonly: boolean;
  session: Session;
  selectedModelId: string;
}) {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const currentModel = selectedModelId === 'gpt-4' ? 'GPT-4' : 'GPT-3.5 Turbo';

  useEffect(() => {
    setMounted(true);
  }, []);

  const toggleTheme = () => {
    if (theme === 'light') {
      setTheme('dark');
    } else if (theme === 'dark') {
      setTheme('system');
    } else {
      setTheme('light');
    }
  };

  const getThemeIcon = () => {
    // Prevent hydration mismatch by showing system icon until mounted
    if (!mounted) return <Monitor className="h-4 w-4" />;

    if (theme === 'light') return <Sun className="h-4 w-4" />;
    if (theme === 'dark') return <Moon className="h-4 w-4" />;
    return <Monitor className="h-4 w-4" />;
  };

  return (
    <header className="flex sticky top-0 bg-background py-1.5 items-center px-2 md:px-2 gap-2">
      <div className="flex items-center justify-between w-full">
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white text-xs font-bold">AI</span>
          </div>
          <h1 className="text-xl font-semibold text-foreground">Discovery AI</h1>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleTheme}
            className="h-8 w-8 p-0"
          >
            {getThemeIcon()}
          </Button>
          <span className="px-2 py-1 bg-muted rounded-md text-xs">
            {currentModel}
          </span>
          <span>Workflow: {chatId.slice(0, 8)}...</span>
        </div>
      </div>
    </header>
  );
}

export const ChatHeader = memo(PureChatHeader, (prevProps, nextProps) => {
  return (
    prevProps.chatId === nextProps.chatId &&
    prevProps.selectedVisibilityType === nextProps.selectedVisibilityType &&
    prevProps.isReadonly === nextProps.isReadonly
  );
});
