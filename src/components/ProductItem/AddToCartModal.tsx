"use client";

import { ProductVariantOverviewType } from "@/app/[lang]/[categorySlug]/page";
import { useTransition, animated } from "@react-spring/web";
import React, { useState } from "react";
import { Button } from "../Button";
import { useUIStore } from "@/context/useUIStore";
import { useAddToCart } from "@/hooks/useAddToCart";

interface AddToCartModalProps {
  productVariant: ProductVariantOverviewType;
}

export function AddToCartModal({ productVariant }: AddToCartModalProps) {
  const { viewmode } = useUIStore();
  const { addToCart } = useAddToCart();
  const [isOpen, setIsOpen] = useState(false);
  const [selectedSku, setSelectedSku] = useState<string>();
  const { setLoadingModalContent } = useUIStore();

  const transition = useTransition(isOpen, {
    from: {
      opacity: 0,
    },
    enter: {
      opacity: 1,
    },
    leave: {
      opacity: 0,
    },
    config: {
      duration: 100,
    },
  });

  return (
    <>
      {viewmode !== 2 ? (
        <>
          <button onClick={() => setIsOpen((prev) => !prev)}>
            <div className="absolute left-[50%] -translate-x-[50%] bottom-4 w-7 h-7 z-10 p-[8px] rounded-full bg-white/50 hover:bg-white/90 flex">
              <svg
                className="pr-[1px]"
                viewBox="0 0 7 7"
                fill="black"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M4 3.505V.255h-.5v3.25H.25v.5H3.5v3.25H4v-3.25h3.25v-.5H4z"></path>
              </svg>
            </div>
          </button>
          {transition((style, isOpen) => (
            <>
              {isOpen ? (
                <animated.div
                  className="absolute flex flex-col p-2 w-full z-20 bottom-[50px]"
                  style={style}
                >
                  <div className="bg-white dark:bg-black">
                    <div className="grid grid-cols-2 gap-2 p-2 w-full">
                      {productVariant.skuList.map((sku) => {
                        const skuValue = sku.split("-").at(-1);
                        return (
                          <Button
                            active={selectedSku === sku}
                            onClick={() => setSelectedSku(sku)}
                            variant="outlined"
                            fullWidth
                            key={sku}
                          >
                            {skuValue}
                          </Button>
                        );
                      })}
                    </div>
                    <div className="flex w-full">
                      <Button
                        variant="contained"
                        onClick={() => setIsOpen(false)}
                      >
                        CLOSE
                      </Button>
                      <Button
                        variant="outlined"
                        fullWidth
                        onClick={() => {
                          if (!selectedSku) {
                            // size not selected
                            return;
                          }

                          setIsOpen(false);

                          setLoadingModalContent(
                            addToCart({
                              name: productVariant.linkedFrom.productCollection
                                .items[0].name,
                              variantSlug:
                                productVariant.linkedFrom.productCollection
                                  .items[0].slug,
                              media:
                                productVariant.mediaCollection.items[0].url,
                              price: productVariant.price,
                              size: selectedSku.split("-").at(-1) as string,
                              sku: selectedSku,
                              variantRef: productVariant.ref,
                              variantName: productVariant.colorName,
                              quantity: 1,
                              // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            } as any),
                            (res) => {
                              if (res) {
                                return {
                                  message: "ABC",
                                  productAddedToCart: res,
                                  title: "ADDED TO CART",
                                };
                              }
                              return {
                                message: "ABC",
                                title: "FAILED",
                              };
                            },
                          );
                        }}
                      >
                        ADD TO CART
                      </Button>
                    </div>
                  </div>
                </animated.div>
              ) : null}
            </>
          ))}
        </>
      ) : null}
    </>
  );
}
