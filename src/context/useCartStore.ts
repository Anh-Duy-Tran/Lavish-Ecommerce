import { create } from "zustand";
import { CartItem } from "@prisma/client";

interface CartStoreType {
  cart: CartItem[];
  setInitialCart: (cart: CartItem[]) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartStoreType>()((set) => ({
  cart: [],
  setInitialCart: (cart: CartItem[]) => set({ cart }),
  clearCart: () => set({ cart: [] }),
}));
