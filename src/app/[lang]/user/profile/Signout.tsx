"use client";

import { signOut } from "next-auth/react";
import { useRouter } from "next/navigation";

import React from "react";

export function Signout() {
  const router = useRouter();

  return (
    <div
      onClick={async () => {
        await signOut({ redirect: false });
        router.push("/");
      }}
    >
      <h3 className="underline text-black/50 w-fit cursor-pointer">Sign out</h3>
    </div>
  );
}
