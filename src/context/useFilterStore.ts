import { create } from "zustand";

export type FilterType = {
  [name: string]: {
    [value: string]: {
      selected: boolean;
      value: Array<string>;
    };
  };
};

function mergeWithoutDuplicates(lists: string[][]): string[] {
  // Use a Set to automatically filter out duplicates
  const mergedSet = new Set<string>();

  for (const list of lists) {
    for (const item of list) {
      mergedSet.add(item);
    }
  }

  // Convert the Set back to an array
  return [...mergedSet];
}
interface FilterStoreType {
  filters: FilterType;
  isFilterOpen: boolean;
  currentOpenFilter?: string;

  openFilter: (filter: string) => void;
  closeFilter: () => void;
  clearSelectedFilter: () => void;
  setFilters: (filters: FilterType) => void;
  toggleFilter: (name: string, value: string) => void;

  filteredProductVariantRefs: Array<string>;
}

export const useFilterStore = create<FilterStoreType>()((set) => ({
  filters: {},
  isFilterOpen: false,
  filteredProductVariantRefs: [],
  openFilter: (filter: string) =>
    set({ currentOpenFilter: filter, isFilterOpen: true }),
  closeFilter: () => set({ isFilterOpen: false }),
  toggleFilter: (name: string, value: string) => {
    set((state) => {
      const newFilters = {
        ...state.filters,
        [name]: {
          ...state.filters[name],
          [value]: {
            ...state.filters[name][value],
            selected: !state.filters[name][value].selected,
          },
        },
      };

      const refList: string[][] = [];
      for (const key in newFilters) {
        for (const filterKey in newFilters[key]) {
          if (newFilters[key][filterKey].selected) {
            refList.push(newFilters[key][filterKey].value);
          }
        }
      }
      const newFilteredProductRefList = mergeWithoutDuplicates(refList);

      return {
        filters: newFilters,
        filteredProductVariantRefs: newFilteredProductRefList,
      };
    });
  },
  clearSelectedFilter: () => set({ filteredProductVariantRefs: [] }),
  setFilters: (filters: FilterType) => {
    // filter out all the filter that only have 1 outcome
    filters = Object.keys(filters)
      .filter((key) => Object.keys(filters[key]).length > 1)
      .reduce((res, key) => ((res[key] = filters[key]), res), {} as FilterType);
    set({ filters });
  },
}));
