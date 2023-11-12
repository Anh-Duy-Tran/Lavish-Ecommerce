"use client";

import React from "react";
import { Button } from "../Button";
import { useCartStore } from "@/context/useCartStore";
import { changeCartItemQuantity } from "@/actions/changeCartItemQuantity";
import { useUIStore } from "@/context/useUIStore";
import { useSession } from "next-auth/react";
import { CartItem } from "@prisma/client";
import { useGuestCartStore } from "@/context/useGuestCartStore";
interface CartItemQuantityProps {
  id: string;
}

export function CartItemQuantity({ id }: CartItemQuantityProps) {
  const { data: session } = useSession();
  const { cart, updateCart } = useCartStore();
  const { updateGuestCart } = useGuestCartStore();
  const { setLoadingModalContent } = useUIStore();

  const cartItem = cart.find((cartItem) => cartItem.id === id) as CartItem;

  const changeCartItemQuantityWithSession = async (
    id: string,
    delta: number,
  ): Promise<CartItem> => {
    if (session) {
      return changeCartItemQuantity(id, delta);
    } else {
      updateGuestCart(id, {
        ...cartItem,
        quantity: cartItem?.quantity + delta,
      });
    }
    return cartItem;
  };

  const handleChangeQuantity = async (delta: number) => {
    const updatedCartItem = await setLoadingModalContent(
      changeCartItemQuantityWithSession(id, delta),
      (res) => {
        if (res) {
          return null;
        }
        return { title: "error", message: "error" };
      },
    );
    updateCart(id, updatedCartItem);
  };

  return (
    <div className="flex items-center gap-3 mt-1">
      <Button
        variant="outlined"
        size="compact"
        onClick={() => handleChangeQuantity(-1)}
      >
        -
      </Button>
      <h3>{cartItem?.quantity || 0}</h3>
      <Button
        variant="outlined"
        size="compact"
        onClick={() => handleChangeQuantity(1)}
      >
        +
      </Button>
    </div>
  );
}
