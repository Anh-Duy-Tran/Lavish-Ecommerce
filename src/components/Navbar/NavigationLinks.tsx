"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { User } from "next-auth";

interface NavigationLinksProps {
  user?: User;
}

export function NavigationLinks({ user }: NavigationLinksProps) {
  const pathname = usePathname() || "";

  return (
    <div id="navigation-links" className="flex gap-7 select-none">
      {!pathname.includes("/login") ? (
        user ? (
          <Link href="/login">
            <p>{user.firstName.toUpperCase()}</p>
          </Link>
        ) : (
          <Link href="/login">
            <p>LOGIN</p>
          </Link>
        )
      ) : null}
      {!pathname.includes("/help") ? (
        <Link href="/help">
          <p>HELP</p>
        </Link>
      ) : null}
      <Link href="/cart">
        <p>CART</p>
      </Link>
    </div>
  );
}
