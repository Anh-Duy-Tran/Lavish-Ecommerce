"use client";

import React, { useEffect, useState } from "react";
import "./slider.css";
import { useMousePosition } from "@/context/useMousePosition";

interface SliderProps {
  children: React.ReactNode;
}

export function Slider({ children }: SliderProps) {
  const { dragging, mouse, handleMouseDown } = useMousePosition();
  const [thisDragging, setThisDragging] = useState(false);

  useEffect(() => {
    if (!dragging) {
      setThisDragging(dragging);
    }
  }, [dragging]);

  if (thisDragging) console.log(mouse, thisDragging);

  return (
    <ul
      onMouseDown={(e) => {
        console.log(123);
        setThisDragging(true);
        handleMouseDown(e);
      }}
      className="slider-container bg-red-500"
    >
      {children}
    </ul>
  );
}

interface SlideProps {
  children: React.ReactNode;
}

export function Slide({ children }: SlideProps) {
  return <li className="slide-container">{children}</li>;
}
