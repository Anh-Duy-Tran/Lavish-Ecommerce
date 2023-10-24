import { create } from "zustand";

export type Category = {
  name: string;
  highlightSrcs: string[];
};

export interface CategoryStoreType {
  categories: Category[];
  setCategories: (categories: Category[]) => void;
}

export const useCategoryStore = create<CategoryStoreType>()((set) => ({
  categories: [],
  setCategories: (categories) => set(() => ({ categories })),
}));
