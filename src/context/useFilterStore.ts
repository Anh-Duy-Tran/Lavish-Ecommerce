import { create } from "zustand";

export type FilterType = {
  [name: string]: {
    [value: string]: {
      selected: boolean;
      value: Array<string>;
    };
  };
};

interface FilterStoreType {
  filters: FilterType;
  isFilterOpen: boolean;
  currentOpenFilter?: string;
  filterActive: boolean;

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
  filterActive: false,
  filteredProductVariantRefs: [],
  openFilter: (filter: string) =>
    set({ currentOpenFilter: filter, isFilterOpen: true }),
  closeFilter: () => set({ isFilterOpen: false }),
  toggleFilter: (name: string, value: string) => {
    let filterActive = false;

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

      const refList: { [filterType: string]: string[][] } = {};
      for (const key in newFilters) {
        if (!(key in refList)) {
          refList[key] = [];
        }
        for (const filterKey in newFilters[key]) {
          if (newFilters[key][filterKey].selected) {
            filterActive = true;
            refList[key].push(newFilters[key][filterKey].value);
          }
        }
      }

      const newFilteredProductRefList = mergeWithoutDuplicates(refList);

      return {
        filterActive,
        filters: newFilters,
        filteredProductVariantRefs: newFilteredProductRefList,
      };
    });
  },
  clearSelectedFilter: () =>
    set({ filteredProductVariantRefs: [], filterActive: false }),
  setFilters: (filters: FilterType) => {
    // filter out all the filter that only have 1 outcome
    filters = Object.keys(filters)
      .filter((key) => Object.keys(filters[key]).length > 1)
      .reduce((res, key) => ((res[key] = filters[key]), res), {} as FilterType);
    set({ filters });
  },
}));

function mergeWithoutDuplicates(lists: {
  [filterType: string]: string[][];
}): string[] {
  console.log(lists);
  let mergedIntersect = new Set<string>();

  for (const type in lists) {
    // Use a Set to automatically filter out duplicates
    if (lists[type].length === 0) {
      continue;
    }

    const mergedSet = new Set<string>();

    for (const list of lists[type]) {
      for (const item of list) {
        mergedSet.add(item);
      }
    }

    if (mergedIntersect.size === 0) {
      mergedSet.forEach((item) => mergedIntersect.add(item));
    } else {
      mergedIntersect = new Set(
        [...mergedSet].filter((i) => mergedIntersect.has(i))
      );
    }
  }

  // Convert the Set back to an array
  return [...mergedIntersect];
}
