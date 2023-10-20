import React from "react";
import { Slider, SliderSyncWithStore } from "@/components/Slider";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";
import { useCategoryStore } from "@/context/useCategoryStore";
import Image from "next/image";

export function HighlightSlider() {
  // const categories = useCategoryStore.getState().categories;
  const categories = useCategoryStore.getState().categories;

  return (
    <>
      <UseStartMouseListener />
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
