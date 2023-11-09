"use client";

import { signOut } from "next-auth/react";

import React from "react";

export function Signout() {
  return (
    <div
      onClick={async () => {
        await signOut({ redirect: false });
      }}
    >
      <h3 className="underline text-black/50 w-fit cursor-pointer">Sign out</h3>
    </div>
  );
}
