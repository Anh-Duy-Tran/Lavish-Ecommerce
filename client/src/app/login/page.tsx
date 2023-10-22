import { LoginForm } from "@/components/LoginForm";
import React from "react";

interface pageProps {
  searchParams?: Record<"callbackUrl" | "error", string>;
}

export default function page({ searchParams }: pageProps) {
  return <LoginForm {...searchParams} />;
}
