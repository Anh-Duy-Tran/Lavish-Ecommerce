import { ProductVariantOverviewType } from "@/app/[lang]/[categorySlug]/page";
import React from "react";
import Image from "next/image";

import { ProductSlider } from "../ProductSlider";

interface ProductItemProps {
  productVariant: ProductVariantOverviewType;
  viewmode: number;
}

export function ProductItem({ productVariant, viewmode }: ProductItemProps) {
  const productName = productVariant.linkedFrom.productCollection.items[0].name;
  const numPeerVariant =
    productVariant.linkedFrom.productCollection.items[0].variantsCollection
      .total;

  return (
    <div>
      <div style={{ aspectRatio: "2/3", width: "100%", overflow: "hidden" }}>
        {viewmode === 2 ? (
          <div className="relative h-full w-full">
            <Image
              style={{
                userSelect: "none",
                pointerEvents: "none",
                objectFit: "cover",
              }}
              priority
              fill
              sizes="(max-width: 768px) 25vw, 10vw"
              src={productVariant.mediaCollection.items[0].url}
              alt={productVariant.mediaCollection.items[0].url}
            />
          </div>
        ) : (
          <ProductSlider
            direction="horizontal"
            srcs={productVariant.mediaCollection.items.map(
              (media) => media.url
            )}
          />
        )}
      </div>
      <h3>{`${productName} +${numPeerVariant}`}</h3>
    </div>
  );
}
