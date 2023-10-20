import React from "react";
import { Slider, Slide } from "../Slider";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";

export async function HighlightSlider() {
  return (
    <>
      <UseStartMouseListener />
      <div className="w-screen h-screen overflow-hidden">
        <Slider arrow buttonNav>
          <Slide>
            111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
          </Slide>
          <Slide>
            222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
          </Slide>
          <Slide>
            333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
          </Slide>
        </Slider>
      </div>
    </>
  );
}
