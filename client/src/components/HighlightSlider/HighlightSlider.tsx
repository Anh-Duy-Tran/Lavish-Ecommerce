import React from "react";
import { Slider } from "../Slider";
import { UseStartMouseListener } from "@/hooks/UseStartMouseListener";

export async function HighlightSlider() {
  return (
    <>
      <UseStartMouseListener />
      <div className="w-screen h-screen overflow-hidden">
        <Slider discreteInput arrow>
          <Slider type="overlay" direction="vertical" discreteInput>
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
          <Slider type="overlay" direction="vertical" discreteInput>
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
          <Slider type="overlay" direction="vertical" discreteInput>
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
        </Slider>
      </div>
    </>
  );
}
