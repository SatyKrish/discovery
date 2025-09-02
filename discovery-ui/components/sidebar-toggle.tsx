'use client';

import { SidebarLeftIcon } from '@/components/icons';
import { Button } from '@/components/ui/button';
import { useSidebar } from '@/components/ui/sidebar';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

export function SidebarToggle() {
  const { toggleSidebar } = useSidebar();

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button
          variant="outline"
          size="icon"
          onClick={toggleSidebar}
          className="md:px-2 md:h-fit"
        >
          <SidebarLeftIcon width={16} height={16} />
        </Button>
      </TooltipTrigger>
      <TooltipContent side="right">Toggle Sidebar</TooltipContent>
    </Tooltip>
  );
}
