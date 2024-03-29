import { ProductVariantOverviewType } from "@/app/[lang]/[categorySlug]/page";
import React, { useMemo } from "react";
import Image from "next/image";

import { ProductSlider } from "../ProductSlider";
import { AddToCartModal } from "./AddToCartModal";
import Link from "next/link";

interface ProductItemProps {
  productVariant: ProductVariantOverviewType;
  viewmode: number;
}

export function ProductItem({ productVariant, viewmode }: ProductItemProps) {
  const productName = productVariant.linkedFrom.productCollection.items[0].name;
  const numPeerVariant =
    productVariant.linkedFrom.productCollection.items[0].variantsCollection
      .total;

  const link = `/product/${productVariant.linkedFrom.productCollection.items[0].slug}?v1=${productVariant.ref}`;

  const media = useMemo(() => {
    const media = productVariant.mediaCollection.items.map(
      (media) => media.url,
    );
    if (productVariant.firstMediaInOverview) {
      media.unshift(media.splice(productVariant.firstMediaInOverview, 1)[0]);
    }
    return media;
  }, []);

  return (
    <div className="">
      <div className="relative aspect-[2/3] w-full overflow-hidden cursor-pointer">
        <AddToCartModal productVariant={productVariant} />
        {viewmode === 2 ? (
          <Link href={link}>
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
                src={
                  productVariant.mediaCollection.items[
                    productVariant.firstMediaInOverview || 0
                  ].url
                }
                alt={productVariant.ref}
              />
            </div>
          </Link>
        ) : (
          <ProductSlider
            href={`/product/${productVariant.linkedFrom.productCollection.items[0].slug}?v1=${productVariant.ref}`}
            direction="horizontal"
            srcs={media}
          />
        )}
      </div>
      {viewmode !== 2 ? (
        <div className="flex justify-between py-4 px-1">
          <div className="flex flex-col">
            <Link href={link}>
              <h3>{`${productName} ${
                numPeerVariant > 1 ? `+${numPeerVariant - 1}` : ""
              }`}</h3>
            </Link>
            <h3>{`${productVariant.price / 100} EUR`}</h3>
          </div>
          <div>
            <svg
              className="icon"
              preserveAspectRatio="xMidYMid slice"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              fill="inherit"
              stroke="inherit"
            >
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M12 15.238L17 20V4H7v16l5-4.762zm-4 2.429l4-3.81 4 3.81V5H8v12.667z"
              ></path>
            </svg>
          </div>
        </div>
      ) : null}
    </div>
  );
}
