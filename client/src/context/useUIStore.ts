import { create } from "zustand";

interface UIStoreType {
  currentCategoryIndex: number;
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  closeSidebar: () => void;
  setCurrentCategoryIndex: (i: number) => void;
}

export const useUIStore = create<UIStoreType>()((set) => ({
  currentCategoryIndex: 0,
  isSidebarOpen: false,
  closeSidebar: () => set(() => ({ isSidebarOpen: false })),
  toggleSidebar: () =>
    set(({ isSidebarOpen }) => ({ isSidebarOpen: !isSidebarOpen })),
  setCurrentCategoryIndex: (i) => set(() => ({ currentCategoryIndex: i })),
}));
