"use client";

import React, { Children, useEffect, useState } from "react";
import "./slider.css";
import { useElementSize } from "usehooks-ts";
import { useMousePosition } from "@/context/useMousePosition";

interface SliderProps {
  children: React.ReactNode;
  arrow?: boolean;
  direction?: "horizontal" | "vertical";
  buttonNav?: boolean;
}

export function Slider({
  children,
  arrow,
  buttonNav,
  direction = "horizontal",
}: SliderProps) {
  const { dragging, mouse, handleMouseDown } = useMousePosition();
  const [currentSlide, setCurrentSlide] = useState(0);
  const [squareRef, { width, height }] = useElementSize();
  const [thisDragging, setThisDragging] = useState(false);

  useEffect(() => {
    const totalSlide = Children.count(children);
    const handleChangeSlide = (n: number) => {
      setCurrentSlide((prev) =>
        prev + n >= totalSlide ? totalSlide - 1 : prev + n < 0 ? 0 : prev + n
      );
    };
    if (!dragging) {
      const threshold = 0.35;
      const prev =
        direction === "horizontal"
          ? mouse.offSetX / width
          : mouse.offSetY / height;

      if (prev > threshold) {
        handleChangeSlide(-1);
      } else if (prev < -threshold) {
        handleChangeSlide(1);
      }
      setThisDragging(false);
    }
  }, [children, direction, dragging, height, mouse, width]);

  useEffect(() => {
    const handleArrowKeyPress = (e: KeyboardEvent) => {
      if (direction === "horizontal") {
        switch (e.key) {
          case "ArrowLeft":
            setCurrentSlide((prev) => prev - 1);
            break;
          case "ArrowRight":
            setCurrentSlide((prev) => prev + 1);
            break;
          default:
            break;
        }
      } else {
        switch (e.key) {
          case "ArrowUp":
            setCurrentSlide((prev) => prev - 1);
            break;
          case "ArrowDown":
            setCurrentSlide((prev) => prev + 1);
            break;
          default:
            break;
        }
      }
    };

    document.addEventListener("keydown", handleArrowKeyPress);

    // Remove the event listener on unmount
    return () => {
      document.removeEventListener("keydown", handleArrowKeyPress);
    };
  }, [buttonNav, children, direction]);

  return (
    <>
      {arrow ? (
        <>
          <button
            className="icon slide-left-button"
            style={{ visibility: currentSlide > 0 ? "visible" : "hidden" }}
            onClick={() => setCurrentSlide((prev) => prev - 1)}
          >
            {arrowIcon}
          </button>
          <button
            className="icon slide-right-button"
            style={{
              visibility:
                currentSlide < Children.count(children) - 1
                  ? "visible"
                  : "hidden",
            }}
            onClick={() => setCurrentSlide((prev) => prev + 1)}
          >
            {arrowIcon}
          </button>
        </>
      ) : null}
      <div
        onMouseDown={(e) => {
          setThisDragging(true);
          handleMouseDown(e);
        }}
        style={{
          transition: "transform 700ms cubic-bezier(.17,.79,.42,1)",
          transform:
            direction === "horizontal"
              ? thisDragging
                ? `translateX(${
                    (mouse.offSetX * 100) / width - 100 * currentSlide
                  }%)`
                : `translateX(${-100 * currentSlide}%)`
              : thisDragging
              ? `translateY(${
                  (mouse.offSetY * 100) / height - 100 * currentSlide
                }%)`
              : `translateY(${-100 * currentSlide}%)`,
        }}
        ref={squareRef}
        className={
          direction === "horizontal"
            ? "slider-container"
            : "slider-vertical-container"
        }
      >
        {children}
      </div>
    </>
  );
}

interface SlideProps {
  children: React.ReactNode;
}

export function Slide({ children }: SlideProps) {
  return <div className="slide-container">{children}</div>;
}

const arrowIcon = (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    fill="inherit"
    stroke="inherit"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M15.336 12L8.624 4.33l.752-.66L16.665 12l-7.289 8.33-.752-.66L15.336 12z"
    ></path>
  </svg>
);
