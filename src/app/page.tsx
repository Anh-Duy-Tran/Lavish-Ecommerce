import { HighlightSlider } from "@/components/HighlightSlider";
import React from "react";

export default async function Home() {
  // const fetchCategoryHighlights =
  //   await client.getEntries<TypeCategoryHighlightSkeleton>({
  //     content_type: "categoryHighlight",
  //   });

  // console.log(fetchCategoryHighlights.includes?.Entry[0].fields.media);

  return (
    // <CategoryStoreInitializer categoryHighlights={}>
    <HighlightSlider />
    // </CategoryStoreInitializer>
  );
}
