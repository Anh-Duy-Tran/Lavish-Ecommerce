import { create } from "zustand";
import { CartItem } from "@prisma/client";

export interface CartStoreType {
  cart: CartItem[];
  setInitialCart: (cart: CartItem[]) => void;
  addToClientCart: (cartItem: CartItem) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartStoreType>()((set) => ({
  cart: [],
  setInitialCart: (cart: CartItem[]) => set({ cart }),
  addToClientCart: (cartItem: CartItem) =>
    set(({ cart }) => ({ cart: [...cart, cartItem] })),
  clearCart: () => set({ cart: [] }),
}));
