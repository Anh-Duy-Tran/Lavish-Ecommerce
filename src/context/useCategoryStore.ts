import { FetchCategoriesQuery } from "@/gql/graphql";
import { create } from "zustand";

type CategoriesCollectionType = NonNullable<
  FetchCategoriesQuery["categories"]
>["categoriesCollection"];
type CategoriesType = NonNullable<CategoriesCollectionType>["items"];

export interface CategoryStoreType {
  categories: CategoriesType;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  categoryHighlights: Record<string, any>;
  setCategories: (categories: CategoriesType) => void;
}

export const useCategoryStore = create<CategoryStoreType>()((set) => ({
  categories: [],
  categoryHighlights: {},
  setCategories: (categories) => set(() => ({ categories })),
}));
