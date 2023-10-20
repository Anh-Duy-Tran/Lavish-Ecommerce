import React from "react";
import { Slider, Slide } from "../Slider";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";


export async function HighlightSlider() {
  return (
    <>
      <UseStartMouseListener />
      <div className="w-screen h-screen">
        <Slider>
          <Slide>1</Slide>
          <Slide>2</Slide>
          <Slide>3</Slide>
        </Slider>
      </div>
    </>
  );
}
