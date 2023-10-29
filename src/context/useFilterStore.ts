import { create } from "zustand";

export type FilterType = {
  [attributeType: string]: {
    [attributeName: string]: string[];
  };
};
interface FilterStoreType {
  filters: FilterType;
  isFilterOpen: boolean;
  currentOpenFilter?: string;

  openFilter: (filter: string) => void;
  closeFilter: () => void;
  setFilters: (filters: FilterType) => void;
}

export const useFilterStore = create<FilterStoreType>()((set) => ({
  filters: {},
  isFilterOpen: false,
  openFilter: (filter: string) => set({ currentOpenFilter: filter, isFilterOpen: true }),
  closeFilter: () => set({ isFilterOpen: false }),
  setFilters: (filters: FilterType) => {
    // filter out all the filter that only have 1 outcome
    filters = Object.keys(filters)
      .filter((key) => Object.keys(filters[key]).length > 1)
      .reduce((res, key) => ((res[key] = filters[key]), res), {} as FilterType);
    set({ filters });
  },
}));
