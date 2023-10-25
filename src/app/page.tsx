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
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    {} as { [key: string]: any },
  );

  useCategoryStore.setState({ categoryHighlights: fetchedCategories });

  return <HighlightSlider />;
}
