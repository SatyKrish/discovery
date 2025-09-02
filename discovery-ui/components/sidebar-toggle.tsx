'use client';

import { MenuIcon } from '@/components/icons';
import { Button } from '@/components/ui/button';
import { useSidebar } from '@/components/ui/sidebar';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

interface SidebarToggleProps {
  position?: 'header' | 'sidebar';
}

export function SidebarToggle({ position = 'header' }: SidebarToggleProps) {
  const { toggleSidebar, state } = useSidebar();

  // When position is 'sidebar', only show when sidebar is expanded
  if (position === 'sidebar' && state === 'collapsed') {
    return null;
  }

  // When position is 'header', only show when sidebar is collapsed
  if (position === 'header' && state === 'expanded') {
    return null;
  }

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button
          variant="outline"
          size="icon"
          onClick={toggleSidebar}
          className="md:px-2 md:h-fit"
        >
          <MenuIcon className="h-4 w-4" />
        </Button>
      </TooltipTrigger>
      <TooltipContent side="right">Toggle Sidebar</TooltipContent>
    </Tooltip>
  );
}
