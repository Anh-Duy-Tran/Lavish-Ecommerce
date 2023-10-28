import { ProductVariantOverviewType } from "@/app/[lang]/[categorySlug]/page";
import React from "react";
interface ProductItemProps {
  productVariant: ProductVariantOverviewType;
}

export function ProductItem({ productVariant }: ProductItemProps) {
  const productName = productVariant.linkedFrom.productCollection.items[0].name;
  const numPeerVariant =
    productVariant.linkedFrom.productCollection.items[0].variantsCollection
      .total;

  return (
    <div>
      <p>{`${productName} +${numPeerVariant}`}</p>
    </div>
  );
}
