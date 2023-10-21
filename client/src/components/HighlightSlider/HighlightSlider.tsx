import React from "react";
import { Slider, SliderSyncWithStore } from "@/components/Slider";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";
import { useCategoryStore } from "@/context/useCategoryStore";
import Image from "next/image";
import { SidebarCategoryButton } from "../Sidebar/Sidebar";

export function HighlightSlider() {
  // const categories = useCategoryStore.getState().categories;
  const categories = useCategoryStore.getState().categories;

  return (
    <>
      <UseStartMouseListener />
      <div className="flex absolute w-full left-0 justify-center">
        <div className="page-container mt-2 ml-[-17px] add-padding-top z-30">
          <SidebarCategoryButton />
        </div>
      </div>
      <div className="w-screen h-screen overflow-hidden">
        <SliderSyncWithStore discreteInput arrow>
          {categories.map((category, i) => (
            <Slider
              type="overlay"
              direction="vertical"
              discreteInput
              buttonNav
              key={i}
              id={i}
            >
              {category.highlightSrcs.map((src) => (
                <div key={src} className="relative h-full w-auto">
                  <Image
                    style={{
                      userSelect: "none",
                      pointerEvents: "none",
                      objectFit: "cover",
                    }}
                    priority
                    fill
                    src={src}
                    alt={src}
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
