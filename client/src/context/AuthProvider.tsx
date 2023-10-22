"use client";

import { ReactNode } from "react";
import { SessionProvider } from "next-auth/react";

import React from "react";
interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  return <SessionProvider>{children}</SessionProvider>;
}
