import { create } from "zustand";
import { DeepNonNullable, ValuesType } from "utility-types";
import {
  FetchCategoriesQuery,
  FetchCategoryHighlightsQuery,
} from "@/gql/graphql";

export type CategoriesType =
  DeepNonNullable<FetchCategoriesQuery>["categories"]["categoriesCollection"]["items"];
export type HighLightsType = ValuesType<
  DeepNonNullable<FetchCategoryHighlightsQuery>["categoryHighlightCollection"]["items"]
>["highlightSlidesCollection"]["items"];

export interface CategoryStoreType {
  categories: CategoriesType;
  categoryHighlights: Record<string, HighLightsType>;
  setCategories: (categories: CategoriesType) => void;
}

export const useCategoryStore = create<CategoryStoreType>()((set) => ({
  categories: [],
  categoryHighlights: {},
  setCategories: (categories) => set(() => ({ categories })),
}));
