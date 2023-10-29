"use client";

import { useMousePosition } from "@/context/useMousePositionStore";
import { useEffect } from "react";
import throttle from "lodash.throttle";

export function UseStartMouseListener() {
  const { handleMouseUp, handleMouseMove } = useMousePosition();

  useEffect(() => {
    // Create a local constant for the throttled version of handleMouseMove
    const throttledFunc = throttle(handleMouseMove, 50);

    window.document.documentElement.addEventListener(
      "mousemove",
      throttledFunc,
    );

    window.document.documentElement.addEventListener("mouseup", handleMouseUp);

    return () => {
      window.document.documentElement.removeEventListener(
        "mousemove",
        throttledFunc,
      );
      window.document.documentElement.removeEventListener(
        "mouseup",
        handleMouseUp,
      );

      // Cancel any scheduled throttled calls
      throttledFunc.cancel();
    };
    // As handleMouseMove and handleMouseUp are dependencies,
    // they need to be passed in the dependency array.
  }, [handleMouseMove, handleMouseUp]);

  return null;
}
