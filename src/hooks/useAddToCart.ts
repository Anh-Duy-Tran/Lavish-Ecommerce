"use client";

import { addToUserCart } from "@/actions/addToUserCart";
import { useCartStore } from "@/context/useCartStore";
import { useGuestCartStore } from "@/context/useGuestCartStore";
import { CartItem } from "@prisma/client";
import { useSession } from "next-auth/react";
import { v4 } from "uuid";

export function useAddToCart() {
  const { data: session } = useSession();
  const { addToGuestCart } = useGuestCartStore();
  const { addToClientCart } = useCartStore();

  const addToCart = async (
    cartItem: Omit<CartItem, "id">,
  ): Promise<CartItem | Omit<CartItem, "id"> | undefined> => {
    if (session) {
      const addedCartItem = await addToUserCart(cartItem);
      if (addedCartItem) {
        addToClientCart(addedCartItem);
        return addedCartItem;
      } else {
        throw new Error("Failed to add to database error");
      }
    } else {
      addToGuestCart({ ...cartItem, id: v4() });
      return cartItem;
    }
  };

  return { addToCart };
}
