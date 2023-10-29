"use client";

import React from "react";
import { ProductVariantOverviewType } from "@/app/[lang]/[categorySlug]/page";
import { ProductItem } from "../ProductItem/ProductItem";
import { useUIStore } from "@/context/useUIStore";

interface ProductOverviewProps {
  productVariants: ProductVariantOverviewType[];
}

export function ProductOverview({ productVariants }: ProductOverviewProps) {
  const { viewmode } = useUIStore();

  return (
    <div className="flex flex-col justify-center overflow-x-hidden">
      <div
        className={`grid ${
          viewmode === 1
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
