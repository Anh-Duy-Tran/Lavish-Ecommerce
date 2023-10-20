import { create } from "zustand";

interface UIStoreType {
  currentCategoryIndex: number;
  setCurrentCategoryIndex: (i: number) => void;
}

export const useUIStore = create<UIStoreType>()((set) => ({
  currentCategoryIndex: 0,
  setCurrentCategoryIndex: (i) => set(() => ({ currentCategoryIndex: i })),
}));
