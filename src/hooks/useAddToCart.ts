"use client";

import { addToUserCart } from "@/actions/addToUserCart";
import { useCartStore } from "@/context/useCartStore";
import { useGuestCartStore } from "@/context/useGuestCartStore";
import { CartItem } from "@prisma/client";
import { useSession } from "next-auth/react";

export function useAddToCart() {
  const { data: session } = useSession();
  const { addToGuestCart } = useGuestCartStore();
  const { addToClientCart } = useCartStore();

  const addToCart = async (cartItem: Omit<CartItem, "id">) => {
    if (session) {
      const addedCartItem = await addToUserCart(cartItem);
      if (addedCartItem) {
        addToClientCart(addedCartItem);
      } else {
        //some error
      }
    } else {
      return addToGuestCart({ ...cartItem, id: "" });
    }
  };

  return { addToCart };
}
