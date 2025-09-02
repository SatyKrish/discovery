'use client';

import { memo, useEffect, useState } from 'react';
import { Moon, Sun, Monitor } from 'lucide-react';
import { Button } from './ui/button';
import { useTheme } from './theme-provider';
import type { VisibilityType } from './visibility-selector';
import type { Session } from 'next-auth';
import { SidebarToggle } from './sidebar-toggle';
import { Logo } from './logo';

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
    <header className="sticky top-0 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-border py-3 px-3 md:px-4 z-10">
      <div className="flex items-center justify-between w-full max-w-none">
        {/* Left side - Toggle + Logo + Title */}
        <div className="flex items-center gap-2 min-w-0">
          <SidebarToggle position="header" />
          <Logo />
          <div className="min-w-0">
            <h1 className="text-lg font-semibold text-foreground truncate">Discovery</h1>
            <p className="text-xs text-muted-foreground hidden sm:block">AI-powered Deep Research Agent</p>
          </div>
        </div>

        {/* Right side - Controls */}
        <div className="flex items-center gap-2 shrink-0">
          <div className="hidden sm:flex items-center gap-2 text-sm text-muted-foreground">
            <span className="px-2 py-1 bg-muted rounded-md text-xs font-medium">
              {currentModel}
            </span>
            <span className="text-xs">
              ID: {chatId.slice(0, 8)}...
            </span>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            className="h-8 w-8 shrink-0"
            aria-label="Toggle theme"
          >
            {getThemeIcon()}
          </Button>
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
