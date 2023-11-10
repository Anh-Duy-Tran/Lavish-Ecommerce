"use client";

import { useCartStore } from "@/context/useCartStore";
import { signOut } from "next-auth/react";
import { useRouter } from "next/navigation";

import React from "react";

export function Signout() {
  const router = useRouter();
  const { clearCart } = useCartStore();

  return (
    <div
      onClick={async () => {
        await signOut({ redirect: false });
        clearCart();
        router.push("/");
      }}
    >
      <h3 className="underline text-black/50 dark:text-white/50 w-fit cursor-pointer">
        Sign out
      </h3>
    </div>
  );
}
