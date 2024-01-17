/* eslint-disable @typescript-eslint/no-explicit-any */
import React from "react";
import { SingleProductPage } from "@/components/SingleProductPage";
import { getClient } from "@/lib/graphql";
import { FetchProductDocument } from "@/gql/graphql";

interface ProductPageProps {
  params: { productSlug: string };
  searchParams: { v1: string };
}

export default async function ProductPage({
  params,
  searchParams,
}: ProductPageProps) {
  const { productSlug } = params;

  const product = (
    await getClient().query(FetchProductDocument, {
      productSlug,
    })
  ).data?.productCollection?.items[0];

  return (
    <SingleProductPage product={product as any} variantRef={searchParams.v1} />
  );
}
