"use client";

import { CartItem } from "@prisma/client";
import { useSession } from "next-auth/react";

export function useAddToCart() {
  const { data: session } = useSession();

  const addToCart = (cartItem: CartItem) => {
    if (session) {
      console.log("Add to account");
    } else {
      console.log("Add to local storage");
    }
    console.log(cartItem);
  };

  return { addToCart };
}
