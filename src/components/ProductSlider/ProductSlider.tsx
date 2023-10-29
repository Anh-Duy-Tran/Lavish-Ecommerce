"use client";

import { useMousePosition } from "@/context/useMousePositionStore";
import React, { useEffect, useState } from "react";
import Image from "next/image";
import "./slider.css";
import { useElementSize } from "usehooks-ts";
interface ProductSliderProps {
  direction?: "horizontal" | "vertical";
  srcs: string[];
}

export function ProductSlider({ direction, srcs }: ProductSliderProps) {
  const { dragging, mouse, handleMouseDown } = useMousePosition();
  const [currentSlide, setCurrentSlide] = useState(0);
  const [squareRef, { width, height }] = useElementSize();
  const [thisDragging, setThisDragging] = useState(false);
  const [loadAll, setLoadAll] = useState(false);

  useEffect(() => {
    if (currentSlide > 0) {
      setLoadAll(true);
    }
  }, [currentSlide]);

  useEffect(() => {
    setThisDragging((prev) => (dragging === true ? prev : false));
  }, [dragging]);

  useEffect(() => {
    const totalSlide = srcs.length;
    const handleChangeSlide = (n: number) => {
      setCurrentSlide((prev) =>
        prev + n >= totalSlide ? totalSlide - 1 : prev + n < 0 ? 0 : prev + n,
      );
    };
    if (thisDragging && !dragging) {
      const threshold = 0.35;
      const prevOffset =
        direction === "horizontal"
          ? mouse.offSetX / width
          : mouse.offSetY / height;

      if (prevOffset > threshold) {
        handleChangeSlide(-1);
      } else if (prevOffset < -threshold) {
        handleChangeSlide(1);
      }

      setThisDragging(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [thisDragging, dragging]);

  const offsetHorizontal = thisDragging
    ? (mouse.offSetX * 100) / width - 100 * currentSlide
    : -100 * currentSlide;

  const offsetVertical = thisDragging
    ? (mouse.offSetY * 100) / height - 100 * currentSlide
    : -100 * currentSlide;

  return (
    <div
      onMouseDown={(e) => {
        setThisDragging(true);
        e.preventDefault();
        handleMouseDown(e);
      }}
      style={{
        transition: "transform 700ms cubic-bezier(.17,.79,.42,1)",
        transform:
          direction === "horizontal"
            ? `translate3d(${offsetHorizontal}%, 0, 0)`
            : `translate3d(0, ${offsetVertical}%, 0)`,
      }}
      ref={squareRef}
      className={
        direction === "horizontal"
          ? "slider-container"
          : "slider-vertical-container"
      }
    >
      {srcs.map((src, i) => (
        <>
          {loadAll || i < 2 ? (
            <Slide key={src}>
              <div className="relative h-full w-full">
                <Image
                  style={{
                    userSelect: "none",
                    pointerEvents: "none",
                    objectFit: "cover",
                  }}
                  priority
                  fill
                  sizes="25vw"
                  src={src}
                  alt={src}
                />
              </div>
            </Slide>
          ) : null}
        </>
      ))}
    </div>
  );
}

interface SlideProps {
  children: React.ReactNode;
}

const SlideComponent = ({ children }: SlideProps) => {
  return <div className="slide-container">{children}</div>;
};

const Slide = React.memo(SlideComponent);