import { FetchCategoriesQuery } from "@/gql/graphql";
import { create } from "zustand";

type CategoryItemsType = FetchCategoriesQuery['categories']!['categoriesCollection']!['items'];

export interface CategoryStoreType {
  categories: CategoryType;
  // categoryHighlights: Record<string, TypeCategoryHighlightFields>;
  setCategories: (categories: CategoryType[]) => void;
}

export const useCategoryStore = create<CategoryStoreType>()((set) => ({
  categories: [],
  categoryHighlights: {},
  setCategories: (categories) => set(() => ({ categories })),
}));
