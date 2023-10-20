import { create } from "zustand";

type Category = {
  name: string;
  highlightSrcs: string[];
};

interface CategoryStoreType {
  categories: Category[];
  setCategories: (categories: Category[]) => void;
}

export const useCategoryStore = create<CategoryStoreType>()((set) => ({
  categories: [],
  setCategories: (categories) => set(() => ({ categories })),
}));
