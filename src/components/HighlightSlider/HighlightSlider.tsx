import React from "react";
import { Slider, SliderSyncWithStore } from "@/components/Slider";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";
import { useCategoryStore } from "@/context/useCategoryStore";
import Image from "next/image";
import { SidebarCategoryButton } from "../Sidebar/Sidebar";

export function HighlightSlider() {
  const { categories, categoryHighlights } = useCategoryStore.getState();

  return (
    <>
      <UseStartMouseListener />
      <div className="flex absolute w-full left-0 justify-center">
        <div className="page-container mt-2 ml-[-17px] add-padding-top z-20">
          <SidebarCategoryButton />
        </div>
      </div>
      <div className="w-screen h-screen overflow-hidden">
        <SliderSyncWithStore discreteInput arrow>
          {categories.map(({ slug }, i) => (
            <Slider
              type="overlay"
              direction="vertical"
              discreteInput
              buttonNav
              key={i}
              id={i}
            >
              {categoryHighlights[slug]?.map(({ media }) => (
                <div key={media.url} className="relative h-full w-auto">
                  <Image
                    style={{
                      userSelect: "none",
                      pointerEvents: "none",
                      objectFit: "cover",
                    }}
                    priority
                    fill
                    src={media.url}
                    alt={media.url}
                  />
                </div>
              ))}
            </Slider>
          ))}
        </SliderSyncWithStore>
      </div>
    </>
  );
}
