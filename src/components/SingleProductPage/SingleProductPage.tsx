"use client";

import React, { useState, useMemo } from "react";
import { FetchProductQuery } from "@/gql/graphql";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";
import { ProductSlider } from "@/components/ProductSlider";
import { Button } from "@/components/Button";
import { DeepNonNullable, ValuesType } from "utility-types";
import { useSearchParams, usePathname, useRouter } from "next/navigation";

interface SingleProductPageProps {
  product: ValuesType<
    DeepNonNullable<FetchProductQuery>["productCollection"]["items"]
  >;
  variantRef: string | undefined;
}

export function SingleProductPage({
  product,
  variantRef,
}: SingleProductPageProps) {
  const searchParams = useSearchParams();
  const [currentProductVariantRef, setProductVariantRef] = useState(variantRef);
  const [selectedSku, setSelectedSku] = useState<string>();
  const pathname = usePathname();
  const { replace } = useRouter();

  // Logic to put the variant ref in the search param in the begining of the variant list
  // 
  // const currentProductVariantIdx = product.variantsCollection.items.findIndex(
  //   (item) => item.ref === variantRef
  // );
  // product.variantsCollection.items.unshift(
  //   product.variantsCollection.items.splice(currentProductVariantIdx, 1)[0]
  // );

  const currentProductVariant =
    product.variantsCollection.items.find(
      (item) => item.ref === currentProductVariantRef
    ) || product.variantsCollection.items[0];

  const mediaSrcs = useMemo(
    () =>
      currentProductVariant.mediaCollection?.items.map(
        (src) => src?.url
      ) as string[],
    [currentProductVariant]
  );

  const handleChangeProductVariant = (ref: string) => {
    setProductVariantRef(ref);
    const params = new URLSearchParams(searchParams);
    params.set("v1", ref);
    replace(`${pathname}?${params.toString()}`);
  };

  return (
    <div className="page-wrapper">
      <UseStartMouseListener />
      <div className="page-container flex gap-2 border border-red-500 justify-center">
        <div></div>
        <div className="aspect-[2/3] h-[70vh] laptop:h-[82vh] overflow-hidden">
          <ProductSlider
            direction="vertical"
            shouldLoadAllMedia={true}
            srcs={mediaSrcs}
          />
        </div>
        <div className="invisible tablet:visible tablet:w-[160px] laptop:w-[210px] laptopHD:w-[280px] desktop:w-[330px] desktopHD:w-[370px] border border-green-500">
          <div className="flex flex-col gap-[20px] p-3 border dark:border-white border-black">
            <div className="flex flex-col gap-4">
              <h1>{product?.name}</h1>
              {currentProductVariant.price ? (
                <h2>{`${currentProductVariant.price / 100} EUR`}</h2>
              ) : null}
              <h2>{product?.description}</h2>
              <div>
                {product.variantsCollection.items.length !== 1
                  ? product.variantsCollection.items.map((item) => (
                      <Button
                        key={item.ref}
                        className="p-3"
                        active={item.ref === currentProductVariantRef}
                      >
                        <div
                          onClick={() => handleChangeProductVariant(item.ref)}
                          className={`h-8 w-8 border border-black/10 dark:border-white/70`}
                          style={{ backgroundColor: item.colorCode }}
                        ></div>
                      </Button>
                    ))
                  : null}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-2 p-2 w-full">
              {currentProductVariant.skuList.map((sku) => {
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
            <Button variant="contained">ADD TO CART</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
