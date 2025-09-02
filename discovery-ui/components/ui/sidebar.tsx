'use client';

import { createContext, useContext } from 'react';

const SidebarContext = createContext<{ open: boolean }>({ open: true });

export function useSidebar() {
  return useContext(SidebarContext);
}
