"use client";

import { useMousePosition } from "@/context/useMousePositionStore";
import { useEffect } from "react";
import throttle from "lodash.throttle";

export function UseStartMouseListener() {
  const { handleMouseUp, handleMouseMove, handleTouchEnd, handleTouchMove } =
    useMousePosition();

  useEffect(() => {
    // Create a local constant for the throttled version of handleMouseMove
    const throttledFuncMouse = throttle(handleMouseMove, 50);
    const throttledFuncTouch = throttle(handleTouchMove, 50);

    window.document.documentElement.addEventListener(
      "mousemove",
      throttledFuncMouse
    );
    window.document.documentElement.addEventListener(
      "touchmove",
      throttledFuncTouch
    );

    window.document.documentElement.addEventListener("mouseup", handleMouseUp);
    window.document.documentElement.addEventListener(
      "touchend",
      handleTouchEnd
    );

    return () => {
      window.document.documentElement.removeEventListener(
        "mousemove",
        throttledFuncMouse
      );
      window.document.documentElement.removeEventListener(
        "touchmove",
        throttledFuncTouch
      );
      window.document.documentElement.removeEventListener(
        "mouseup",
        handleMouseUp
      );
      window.document.documentElement.removeEventListener(
        "touchend",
        handleTouchEnd
      );

      window.document.documentElement;

      // Cancel any scheduled throttled calls
      throttledFuncMouse.cancel();
      throttledFuncTouch.cancel();
    };
    // As handleMouseMove and handleMouseUp are dependencies,
    // they need to be passed in the dependency array.
  }, [handleMouseMove, handleMouseUp, handleTouchEnd, handleTouchMove]);

  return null;
}
