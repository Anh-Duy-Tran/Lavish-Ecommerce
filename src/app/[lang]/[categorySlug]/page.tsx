/* eslint-disable @typescript-eslint/no-explicit-any */
import {
  FetchCategoryAttributesDocument,
  FetchProductVariantsInCategoryDocument,
} from "@/gql/graphql";
import { getClient } from "@/lib/graphql";
import React from "react";

import { FetchProductVariantsInCategoryQuery } from "@/gql/graphql";
import { DeepNonNullable, ValuesType } from "utility-types";
import { ProductOverview } from "@/components/ProductOverview/ProductOverview";
import { ProductFilter, ProductFilterModal } from "@/components/ProductFilter";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";
import { FilterType } from "@/context/useFilterStore";

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
      })) as any,
      unionCondition: unionAttributes?.items.map((attribute) => ({
        attributes: { slug: attribute?.slug as string },
      })) as any,
    })
  ).data?.productVariantCollection?.items;

  const filter: FilterType = {};
  productVariants?.forEach((variant) => {
    variant?.attributesCollection?.items.forEach((attribute) => {
      const value = attribute?.name as string;
      const name = attribute?.type as string;

      if (!(name in filter)) {
        filter[name] = {};
      }
      if (!(value in filter[name])) {
        filter[name][value] = { selected: false, value: [] };
      }
      filter[name][value].value.push(variant.ref as string);
    });
  });

  return (
    <>
      <ProductFilterModal />
      <ProductFilter />
      <UseStartMouseListener />
      <div className="add-padding-top mt-20 w-full">
        <ProductOverview
          filters={filter}
          productVariants={productVariants as any}
        />
      </div>
    </>
  );
}
