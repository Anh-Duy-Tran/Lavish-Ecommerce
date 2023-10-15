import { create } from "zustand";

interface UIStoreType {
  bears: number;
  increase: (by: number) => void;
}

export const useUIStore = create<UIStoreType>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
}));
