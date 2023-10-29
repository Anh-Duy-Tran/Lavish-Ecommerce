import {
  FetchCategoryAttributesDocument,
  FetchProductVariantsInCategoryDocument,
} from "@/gql/graphql";
import { getClient } from "@/lib/graphql";
import React from "react";

import { FetchProductVariantsInCategoryQuery } from "@/gql/graphql";
import { DeepNonNullable, ValuesType } from "utility-types";
import { ProductOverview } from "@/components/ProductOverview/ProductOverview";
import { ProductFilter } from "@/components/ProductFilter";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";

export type ProductVariantOverviewType = ValuesType<
  DeepNonNullable<FetchProductVariantsInCategoryQuery>["productVariantCollection"]["items"]
>;

interface CategoryPageProps {
  params: { categorySlug: string };
}

export default async function CategoryPage({ params }: CategoryPageProps) {
  const { categorySlug } = params;
  const categoryAttributes = (
    await getClient().query(FetchCategoryAttributesDocument, { categorySlug })
  ).data?.categoryCollection?.items[0];

  const intersectAttributes = categoryAttributes?.intersectAttributesCollection;
  const unionAttributes = categoryAttributes?.unionAttributesCollection;

  const productVariants = (
    await getClient().query(FetchProductVariantsInCategoryDocument, {
      intersectCondition: intersectAttributes?.items.map((attribute) => ({
        attributes: { slug: attribute?.slug as string },
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
      })) as any,
      unionCondition: unionAttributes?.items.map((attribute) => ({
        attributes: { slug: attribute?.slug as string },
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
      })) as any,
    })
  ).data?.productVariantCollection?.items;
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return (
    <>
      <ProductFilter/>
      <UseStartMouseListener/>
      <div className="add-padding-top mt-20">
        <ProductOverview productVariants={productVariants as any} />
      </div>
    </>
  );
}
