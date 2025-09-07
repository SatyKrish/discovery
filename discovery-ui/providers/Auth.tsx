"use client";

import { createContext, useContext, type ReactNode } from "react";

interface AuthContextType {
  user: any;
  session: {
    accessToken: string;
  } | null;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  session: null,
});

export const AuthProvider = ({ children }: { children: ReactNode }) => (
  <AuthContext.Provider value={{ user: null, session: { accessToken: "" } }}>
    {children}
  </AuthContext.Provider>
);

export const useAuthContext = () => useContext(AuthContext);
