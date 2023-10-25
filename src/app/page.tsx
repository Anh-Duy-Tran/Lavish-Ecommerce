import { HighlightSlider } from "@/components/HighlightSlider";
import { useCategoryStore } from "@/context/useCategoryStore";
import { FetchCategoryHighlightsDocument } from "@/gql/graphql";
import { getClient } from "@/lib/graphql";
import React from "react";

export default async function Home() {
  const fetchedCategories = (
    await getClient().query(FetchCategoryHighlightsDocument, {})
  ).data?.categoryHighlightCollection?.items.reduce(
    (a, c) => {
      a[c?.category?.slug || ""] = c?.highlightSlidesCollection?.items;
      return a;
    },
    {} as Record<string, unknown>
  );

  useCategoryStore.setState({ categoryHighlights: fetchedCategories });

  return <HighlightSlider />;
}
