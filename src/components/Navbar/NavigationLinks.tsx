"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSession } from "next-auth/react";

interface NavigationLinksProps {
  name?: string | null;
}

export function NavigationLinks({ name }: NavigationLinksProps) {
  const [username, setUsername] = useState(name);
  const pathname = usePathname() || "";
  const { data: session } = useSession();

  useEffect(() => {
    // session is not yet loaded
    if (session === undefined) {
      return;
    }

    if (session) {
      setUsername(session.user?.name);
    } else {
      setUsername(undefined);
    }
  }, [session]);

  return (
    <div id="navigation-links" className="flex gap-7 select-none">
      {!pathname.includes("/login") ? (
        username ? (
          <Link href="/user/profile">
            <p>{username.toUpperCase()}</p>
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
