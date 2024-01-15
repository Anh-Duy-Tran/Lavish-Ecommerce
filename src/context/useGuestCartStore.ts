import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { CartItem } from "@prisma/client";

type BearStore = {
  cart: CartItem[];
  setGuestCart: (cart: CartItem[]) => void;
  updateGuestCart: (id: string, cartItem: CartItem) => void;
  addToGuestCart: (cartItem: CartItem) => void;
};

export const useGuestCartStore = create<BearStore>()(
  persist(
    (set, get) => ({
      cart: [],
      setGuestCart: (cart: CartItem[]) => set({ cart }),
      updateGuestCart: (id: string, cartItem: CartItem) =>
        set(({ cart }) => ({
          cart: cart.map((oldCartItem) =>
            oldCartItem.id === id ? cartItem : oldCartItem,
          ),
        })),
      addToGuestCart: (cartItem: CartItem) =>
        set({ cart: [...get().cart, cartItem] }),
    }),
    {
      name: "guest-cart",
      storage: createJSONStorage(() => localStorage),
    },
  ),
);
