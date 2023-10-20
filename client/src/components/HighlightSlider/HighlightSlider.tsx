import React from "react";
import { Slider, SliderSyncWithStore } from "@/components/Slider";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";
import { useCategoryStore } from "@/context/useCategoryStore";
import Image from "next/image";

export function HighlightSlider() {
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
                    style={{ userSelect: "none", pointerEvents: "none" }}
                    priority
                    fill
                    objectFit="cover"
                    src={src}
                    alt={src}
                  />
                </div>
              ))}
            </Slider>
          ))}
          {/* <Slider
            type="overlay"
            direction="vertical"
            discreteInput
            buttonNav
            id={0}
          >
            <p>
              111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
            </p>
            <p>
              222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
            </p>
            <p>
              333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
            </p>
          </Slider>
          <Slider
            type="overlay"
            direction="vertical"
            discreteInput
            buttonNav
            id={1}
          >
            <p>
              111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
            </p>
            <p>
              222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
            </p>
            <p>
              333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
            </p>
          </Slider>
          <Slider
            type="overlay"
            direction="vertical"
            discreteInput
            buttonNav
            id={2}
          >
            <p>
              111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
            </p>
            <p>
              222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
            </p>
            <p>
              333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
            </p>
          </Slider>
          <Slider
            type="overlay"
            direction="vertical"
            discreteInput
            buttonNav
            id={3}
          >
            <p>
              111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
            </p>
            <p>
              222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
            </p>
            <p>
              333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
            </p>
          </Slider> */}
        </SliderSyncWithStore>
      </div>
    </>
  );
}
