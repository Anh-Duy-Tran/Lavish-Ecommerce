"use client";

import React from "react";
import { Button } from "../Button";
import { useFilterStore } from "@/context/useFilterStore";

export function ProductFilter() {
  const { filters, openFilter } = useFilterStore();

  return (
    <div className="fixed add-padding-top w-full flex justify-center z-10">
      <div className="page-container">
        <div className="flex gap-4 px-4 tablet:px-0">
          {Object.keys(filters).map((filterKey) => {
            const numActiveFilter = Object.keys(filters[filterKey]).reduce(
              (a, c) => (a += filters[filterKey][c].selected ? 1 : 0),
              0,
            );
            return (
              <Button
                key={filterKey}
                variant="outlined"
                size="compact"
                onClick={() => openFilter(filterKey)}
              >
                {filterKey +
                  (numActiveFilter > 0 ? `  [ ${numActiveFilter} ]` : ``)}
              </Button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
