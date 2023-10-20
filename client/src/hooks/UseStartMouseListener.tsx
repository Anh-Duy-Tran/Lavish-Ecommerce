"use client";

import { useMousePosition } from "@/context/useMousePosition";
import { useEffect } from "react";

export function UseStartMouseListener() {
  const { handleMouseUp, handleMouseMove } = useMousePosition();

  useEffect(() => {
    window.document.documentElement.addEventListener(
      "mousemove",
      handleMouseMove,
    );

    window.document.documentElement.addEventListener("mouseup", handleMouseUp);

    return () => {
      window.document.documentElement.removeEventListener(
        "mousemove",
        handleMouseMove,
      );
      window.document.documentElement.removeEventListener(
        "mouseup",
        handleMouseUp,
      );
    };
  }, [handleMouseMove, handleMouseUp]);

  return null;
}
