import { create } from "zustand";
import { CartItem } from "@prisma/client";

export interface CartStoreType {
  cart: CartItem[];
  setInitialCart: (cart: CartItem[]) => void;
  addToClientCart: (cartItem: CartItem) => void;
  updateCart: (id: string, cartItem: CartItem) => void;
  removeClientCartItem: (id: string) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartStoreType>()((set) => ({
  cart: [],
  setInitialCart: (cart: CartItem[]) => set({ cart }),
  addToClientCart: (cartItem: CartItem) =>
    set(({ cart }) => ({ cart: [...cart, cartItem] })),
  updateCart: (id: string, cartItem: CartItem) =>
    set(({ cart }) => ({
      cart: cart.map((oldCartItem) =>
        oldCartItem.id === id ? cartItem : oldCartItem,
      ),
    })),
  removeClientCartItem: (id: string) =>
    set(({ cart }) => ({
      cart: cart.filter((cartItem) => cartItem.id !== id),
    })),
  clearCart: () => set({ cart: [] }),
}));
