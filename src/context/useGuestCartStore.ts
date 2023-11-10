import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { CartItem } from "@prisma/client";

type BearStore = {
  cart: CartItem[];
  setCart: (cart: CartItem[]) => void;
};

export const useGuestCartStore = create<BearStore>()(
  persist(
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    (set, get) => ({
      cart: [],
      setCart: (cart: CartItem[]) => set({ cart }),
    }),
    {
      name: "guest-cart",
      storage: createJSONStorage(() => sessionStorage),
    }
  )
);
