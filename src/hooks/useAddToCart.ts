"use client";

import { addToUserCart } from "@/actions/addToUserCart";
import { useGuestCartStore } from "@/context/useGuestCartStore";
import { CartItem } from "@prisma/client";
import { useSession } from "next-auth/react";

export function useAddToCart() {
  const { data: session } = useSession();
  const { addToGuestCart } = useGuestCartStore();

  const addToCart = async (cartItem: CartItem) => {
    if (session) {
      return await addToUserCart(cartItem);
    } else {
      return addToGuestCart(cartItem);
    }
  };

  return { addToCart };
}
