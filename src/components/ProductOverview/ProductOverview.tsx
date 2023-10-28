import React from "react";
import { ProductVariantOverviewType } from "@/app/[lang]/[categorySlug]/page";
import { ProductItem } from "../ProductItem/ProductItem";

interface ProductOverviewProps {
  productVariants: ProductVariantOverviewType[];
}

export function ProductOverview({ productVariants }: ProductOverviewProps) {
  return (
    <div className="flex flex-col justify-center">
      {productVariants.map((variant) => (
        <ProductItem key={variant.ref} productVariant={variant} />
      ))}
    </div>
  );
}
