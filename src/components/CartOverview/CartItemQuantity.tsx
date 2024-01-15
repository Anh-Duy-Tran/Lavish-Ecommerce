"use client";

import React from "react";
import { Button } from "../Button";
import { useCartStore } from "@/context/useCartStore";
import { changeCartItemQuantity } from "@/actions/cartActions/changeCartItemQuantity";
import { useUIStore } from "@/context/useUIStore";
import { useSession } from "next-auth/react";
import { CartItem } from "@prisma/client";
import { useGuestCartStore } from "@/context/useGuestCartStore";
import { removeCartItem } from "@/actions/cartActions/removeCartItem";
interface CartItemQuantityProps {
  id: string;
}

export function CartItemQuantity({ id }: CartItemQuantityProps) {
  const { data: session } = useSession();
  const { cart, updateCart, removeClientCartItem } = useCartStore();
  const { updateGuestCart, removeGuestCart } = useGuestCartStore();
  const { setLoadingModalContent } = useUIStore();

  const cartItem = cart.find((cartItem) => cartItem.id === id) as CartItem;

  const changeCartItemQuantityWithSession = async (
    id: string,
    delta: number,
  ): Promise<CartItem> => {
    if (session) {
      return changeCartItemQuantity(id, delta);
    }
    const updatedCartItem = {
      ...cartItem,
      quantity: cartItem?.quantity + delta,
    };
    updateGuestCart(id, updatedCartItem);
    return updatedCartItem;
  };

  const removeCartItemWithSession = async (): Promise<CartItem> => {
    if (session) {
      return removeCartItem(id);
    } else {
      removeGuestCart(id);
    }
    return cartItem;
  };

  const handleRemoveCartItem = async () => {
    await setLoadingModalContent(removeCartItemWithSession(), (res) => {
      if (res) {
        return null;
      }
      return { title: "error", message: "error" };
    });
    removeClientCartItem(id);
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
    <>
      <div className="flex items-center gap-3 mt-1">
        <Button
          variant="outlined"
          size="compact"
          onClick={() =>
            cartItem.quantity === 1
              ? handleRemoveCartItem()
              : handleChangeQuantity(-1)
          }
          className="w-8 h-8"
        >
          -
        </Button>
        <h3>{cartItem.quantity || 0}</h3>
        <Button
          variant="outlined"
          size="compact"
          onClick={() => handleChangeQuantity(1)}
          className="w-8 h-8"
        >
          +
        </Button>
      </div>
      <div className="absolute top-2 right-2">
        <button onClick={handleRemoveCartItem}>{removeCartItemIcon}</button>
      </div>
    </>
  );
}

const removeCartItemIcon = (
  <svg
    width="20"
    height="20"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    fill="inherit"
    stroke="inherit"
    className="icon"
  >
    <path d="M12 12.707l6.846 6.846.708-.707L12.707 12l6.847-6.846-.707-.708L12 11.293 5.154 4.446l-.707.708L11.293 12l-6.846 6.846.707.707L12 12.707z"></path>
  </svg>
);
