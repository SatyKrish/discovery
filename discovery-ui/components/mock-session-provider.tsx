'use client';

import React, { createContext, useContext } from 'react';
import type { Session } from 'next-auth';

const mockSession: Session = {
  user: {
    id: 'guest-user-123',
    email: 'guest@discovery.ai',
    name: 'Discovery User',
    image: 'https://avatar.vercel.sh/discovery'
  },
  expires: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
};

const MockSessionContext = createContext<{
  data: Session | null;
  status: 'loading' | 'authenticated' | 'unauthenticated';
}>({
  data: mockSession,
  status: 'authenticated',
});

export function useSession() {
  return useContext(MockSessionContext);
}

export function MockSessionProvider({ children }: { children: React.ReactNode }) {
  return (
    <MockSessionContext.Provider value={{ data: mockSession, status: 'authenticated' }}>
      {children}
    </MockSessionContext.Provider>
  );
}
