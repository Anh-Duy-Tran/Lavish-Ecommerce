import { ProductSlider } from "@/components/ProductSlider";
import { FetchProductDocument } from "@/gql/graphql";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";
import { getClient } from "@/lib/graphql";
import React from "react";

interface ProductPageProps {
  params: { productSlug: string };
}

export default async function ProductPage({ params }: ProductPageProps) {
  const { productSlug } = params;
  const product = (
    await getClient().query(FetchProductDocument, {
      productSlug,
    })
  ).data?.productCollection?.items[0];

  return (
    <div className="page-wrapper">
      <div className="page-container flex gap-2 border border-red-500">
        <UseStartMouseListener />
        <div></div>
        <div className="aspect-[2/3] h-[70vh] laptop:h-[82vh] overflow-hidden">
          <ProductSlider
            direction="vertical"
            srcs={
              product?.variantsCollection?.items[0]?.mediaCollection?.items.map(
                (src) => src?.url
              ) as string[]
            }
          />
        </div>
        <div className="flex invisible tablet:visible tablet:w-[160px] laptop:w-[210px] laptopHD:w-[280px] desktop:w-[330px] desktopHD:w-[370px] border border-green-500">
          <div className="flex flex-col gap-4 p-3 border border-white">
            <h1>{product?.name}</h1>
            <h2>{`${
              product?.variantsCollection?.items[0]?.price / 100
            } EUR`}</h2>
            <h2>{product?.description}</h2>
          </div>
        </div>
      </div>
    </div>
  );
}
