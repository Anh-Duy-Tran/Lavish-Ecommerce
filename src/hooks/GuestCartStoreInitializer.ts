"use client";

import { useCartStore } from "@/context/useCartStore";
import { useGuestCartStore } from "@/context/useGuestCartStore";
import { useSession } from "next-auth/react";
import { useEffect } from "react";

function GuestCartStoreInitializer() {
  const { data: session } = useSession();
  const { cart } = useGuestCartStore();
  const { setInitialCart } = useCartStore();

  useEffect(() => {
    if (session === undefined || session) {
      return;
    }
    setInitialCart(cart);
  }, [session, cart, setInitialCart]);

  return null;
}

export default GuestCartStoreInitializer;
