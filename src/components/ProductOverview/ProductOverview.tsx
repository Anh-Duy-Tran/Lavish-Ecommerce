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
  const { setFilters } = useFilterStore();

  useEffect(() => {
    setFilters(filters);
  }, [filters, setFilters]);

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
        {productVariants.map((variant) => (
          <ProductItem
            viewmode={viewmode}
            key={variant.ref}
            productVariant={variant}
          />
        ))}
      </div>
    </div>
  );
}
