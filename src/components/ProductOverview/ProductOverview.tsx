"use client";

import React, { useEffect } from "react";
import { ProductVariantOverviewType } from "@/app/[lang]/[categorySlug]/page";
import { ProductItem } from "../ProductItem/ProductItem";
import { useUIStore } from "@/context/useUIStore";
import { FilterType, useFilterStore } from "@/context/useFilterStore";

interface ProductOverviewProps {
  productVariants: ProductVariantOverviewType[];
  filters: FilterType;
}

export function ProductOverview({
  productVariants,
  filters,
}: ProductOverviewProps) {
  const { viewmode } = useUIStore();
  const {
    filterActive,
    filteredProductVariantRefs,
    setFilters,
    clearSelectedFilter,
    closeFilter,
  } = useFilterStore();

  useEffect(() => {
    setFilters(filters);
    clearSelectedFilter();
    closeFilter();
  }, [closeFilter, clearSelectedFilter, filters, setFilters]);

  return (
    <div className="flex flex-col justify-center overflow-x-hidden">
      <div
        className={`grid ${
          viewmode === 0
            ? "grid-cols-2 tablet:grid-cols-4 gap-2"
            : viewmode === 1
              ? "grid-cols-2 tablet:grid-cols-6 gap-2"
              : "grid-cols-4 tablet:grid-cols-10"
        }`}
      >
        {productVariants
          .filter((variant) =>
            filterActive
              ? filteredProductVariantRefs.includes(variant.ref)
              : true,
          )
          .map((variant) => (
            <ProductItem
              viewmode={viewmode}
              key={variant.ref}
              productVariant={variant}
            />
          ))}
      </div>
      {filterActive &&
      productVariants.filter((variant) =>
        filteredProductVariantRefs.includes(variant.ref),
      ).length === 0 ? (
        <div className="w-full flex flex-col items-center">
          {emptyStoreDueToFilter}
          <p>NO PRODUCTS WERE FOUND.</p>
          <p>TRY REMOVING A FILTER.</p>
        </div>
      ) : null}
    </div>
  );
}

const emptyStoreDueToFilter = (
  <svg
    className="icon"
    aria-hidden="true"
    width="32"
    height="32"
    viewBox="0 0 32 32"
    xmlns="http://www.w3.org/2000/svg"
    fill="inherit"
    stroke="inherit"
  >
    <path d="M15.212 6.184c.67-.06 1.585.013 2.35.646a.492.492 0 0 1 .025.022c.731.691 1.044 1.588 1.121 2.41.075.8-.066 1.573-.306 2.102-.22.69-.485 1.22-.875 1.698a5.356 5.356 0 0 1-.682.685 538.236 538.236 0 0 1 3.73 2.226c2.304 1.39 4.939 3.012 6.204 3.909.377.242.964.696 1.346 1.359.4.696.562 1.603.07 2.649-.564 1.2-1.477 1.688-2.399 1.859a6.277 6.277 0 0 1-1.29.081 21.306 21.306 0 0 1-.518-.02c-.187-.008-.355-.016-.528-.016H8.54c-.118 0-.252.003-.4.007-.559.014-1.303.032-1.997-.11-.916-.186-1.842-.664-2.342-1.808-.487-1.043-.325-1.948.075-2.642.381-.663.968-1.117 1.345-1.36 1.264-.895 3.862-2.516 6.15-3.907 1.15-.7 2.227-1.343 3.026-1.813a71.391 71.391 0 0 1 1.09-.63c.583-.416.973-.744 1.266-1.102.295-.361.51-.778.704-1.395a.495.495 0 0 1 .025-.063c.165-.352.292-.96.23-1.615-.06-.642-.296-1.283-.8-1.766-.476-.387-1.075-.459-1.61-.41a3.738 3.738 0 0 0-.889.196 2.422 2.422 0 0 0-1.2 1.508 1.539 1.539 0 0 0-.031.147.5.5 0 0 1-.995-.104l.497.052-.497-.052v-.005l.001-.007.003-.019.01-.06c.008-.05.021-.117.042-.199.042-.163.113-.384.234-.632a3.425 3.425 0 0 1 1.538-1.547l.19.463-.19-.463h.001l.003-.001.006-.003.021-.008.072-.026a4.741 4.741 0 0 1 1.094-.235zm-2.03 2.847v.003-.003zm2.806 5.371l-.03.016a.516.516 0 0 1-.048.022l-.053.03c-.23.13-.555.319-.953.553-.794.467-1.867 1.108-3.013 1.806-2.3 1.398-4.875 3.005-6.101 3.875a.533.533 0 0 1-.02.014c-.314.2-.757.552-1.028 1.022-.255.444-.37 1.006-.032 1.724l.006.014c.33.761.921 1.09 1.627 1.234.57.116 1.155.102 1.703.09.169-.004.334-.008.494-.008h14.92c.179 0 .4.01.618.02.157.006.313.013.452.017.37.009.737-.001 1.084-.066.667-.123 1.274-.444 1.677-1.3.337-.72.222-1.282-.033-1.725-.27-.47-.713-.822-1.027-1.022a.548.548 0 0 1-.02-.014c-1.226-.869-3.833-2.476-6.152-3.875a469.966 469.966 0 0 0-3.964-2.364l-.107-.063z"></path>
  </svg>
);
