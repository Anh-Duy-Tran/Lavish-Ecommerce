"use client";

import React, { Children, useEffect, useState } from "react";
import "./slider.css";
import { useElementSize } from "usehooks-ts";
import { useMousePosition } from "@/context/useMousePosition";
import { useUIStore } from "@/context/useUIStore";

interface SliderProps {
  children: React.ReactNode;
  arrow?: boolean;
  direction?: "horizontal" | "vertical";
  type?: "slide" | "overlay";
  discreteInput?: boolean;

  crrSlide?: number;
  onChange?: (i: number) => void;

  // for arrow keyboard button navigation
  buttonNav?: boolean;
  id?: number;
}

export function SliderSyncWithStore(props: SliderProps) {
  // get current slide index from UIStore
  const { currentCategoryIndex, setCurrentCategoryIndex } = useUIStore();

  useEffect(() => {
    const totalSlide = Children.count(props.children);
    const handleArrowKeyPress = (e: KeyboardEvent) => {
      switch (e.key) {
        case "ArrowLeft":
          setCurrentCategoryIndex(
            currentCategoryIndex - 1 < 0 ? 0 : currentCategoryIndex - 1
          );
          break;
        case "ArrowRight":
          setCurrentCategoryIndex(
            currentCategoryIndex + 1 > totalSlide - 1
              ? totalSlide - 1
              : currentCategoryIndex + 1
          );
          break;
        default:
          break;
      }
    };

    document.addEventListener("keydown", handleArrowKeyPress);

    // Remove the event listener on unmount
    return () => {
      document.removeEventListener("keydown", handleArrowKeyPress);
    };
  }, [currentCategoryIndex, props.children, setCurrentCategoryIndex]);

  return (
    <Slider
      buttonNav
      {...props}
      crrSlide={currentCategoryIndex}
      onChange={setCurrentCategoryIndex}
    />
  );
}

export function Slider({
  children,
  arrow,
  id,
  onChange = () => {},
  crrSlide = 0,
  buttonNav = false,
  discreteInput = false,
  type = "slide",
  direction = "horizontal",
}: SliderProps) {
  const { currentCategoryIndex } = useUIStore();
  const { dragging, dragDirection, mouse, handleMouseDown } =
    useMousePosition();
  const [currentSlide, setCurrentSlide] = useState(crrSlide);
  const [squareRef, { width, height }] = useElementSize();
  const [thisDragging, setThisDragging] = useState(false);

  useEffect(() => {
    setThisDragging((prev) => (dragging === true ? prev : false));
  }, [dragging]);

  // Arrow Button navigation hook
  useEffect(() => {
    const totalSlide = Children.count(children);
    const handleArrowKeyPress = (e: KeyboardEvent) => {
      if (!buttonNav || currentCategoryIndex !== id) return;
      switch (e.key) {
        case "ArrowUp":
          setCurrentSlide((prev) => (prev - 1 < 0 ? 0 : prev - 1));
          break;
        case "ArrowDown":
          setCurrentSlide((prev) =>
            prev + 1 > totalSlide - 1 ? totalSlide - 1 : prev + 1
          );
          break;
        default:
          break;
      }
    };

    document.addEventListener("keydown", handleArrowKeyPress);

    // Remove the event listener on unmount
    return () => {
      document.removeEventListener("keydown", handleArrowKeyPress);
    };
  }, [buttonNav, children, currentCategoryIndex, id]);

  // Sync with global state for slide
  useEffect(() => {
    setCurrentSlide(crrSlide);
  }, [crrSlide]);

  useEffect(() => {
    onChange(currentSlide);
  }, [currentSlide, onChange]);
  //

  useEffect(() => {
    const correctDiscreteInput = !discreteInput || direction === dragDirection;
    const totalSlide = Children.count(children);
    const handleChangeSlide = (n: number) => {
      setCurrentSlide((prev) =>
        prev + n >= totalSlide ? totalSlide - 1 : prev + n < 0 ? 0 : prev + n
      );
    };
    if (thisDragging && !dragging) {
      const threshold = 0.35;
      const prevOffset = correctDiscreteInput
        ? direction === "horizontal"
          ? mouse.offSetX / width
          : mouse.offSetY / height
        : 0;

      if (prevOffset > threshold) {
        handleChangeSlide(-1);
      } else if (prevOffset < -threshold) {
        handleChangeSlide(1);
      }

      setThisDragging(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [thisDragging, dragging]);

  const correctDiscreteInput = !discreteInput || direction === dragDirection;

  // slide standard calculation
  const offsetHorizontal =
    thisDragging && correctDiscreteInput
      ? (mouse.offSetX * 100) / width - 100 * currentSlide
      : -100 * currentSlide;

  const offsetVertical =
    thisDragging && correctDiscreteInput
      ? (mouse.offSetY * 100) / height - 100 * currentSlide
      : -100 * currentSlide;

  // slide overlay calculation
  const offsetCurrentSlide =
    thisDragging && correctDiscreteInput
      ? Math.max(mouse.offSetY * 100, 0) / height
      : 0;

  const offsetNextSlide =
    thisDragging && correctDiscreteInput
      ? Math.min(mouse.offSetY * 100, 0) / height + 100
      : 100;

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
      {type === "slide" ? (
        // type slide
        <div
          onMouseDown={(e) => {
            setThisDragging(true);
            handleMouseDown(e);
          }}
          style={{
            transition: "transform 700ms cubic-bezier(.17,.79,.42,1)",
            transform:
              direction === "horizontal"
                ? `translateX(${offsetHorizontal}%)`
                : `translateY(${offsetVertical}%)`,
          }}
          ref={squareRef}
          className={
            direction === "horizontal"
              ? "slider-container"
              : "slider-vertical-container"
          }
        >
          {Children.toArray(children).map((child, i) => (
            <Slide key={i}>{child}</Slide>
          ))}
        </div>
      ) : (
        // type overlay
        <div
          onMouseDown={(e) => {
            setThisDragging(true);
            handleMouseDown(e);
          }}
          ref={squareRef}
          className="slider-overlay-container"
        >
          {Children.toArray(children).map((child, i) => (
            <SlideOverlay
              translateY={
                i === currentSlide
                  ? offsetCurrentSlide
                  : i === currentSlide + 1
                  ? offsetNextSlide
                  : i < currentSlide
                  ? 0
                  : 100
              }
              key={i}
            >
              {child}
            </SlideOverlay>
          ))}
        </div>
      )}
    </>
  );
}

interface SlideProps {
  children: React.ReactNode;
}

function Slide({ children }: SlideProps) {
  return <div className="slide-container">{children}</div>;
}

function SlideOverlay({
  children,
  translateY,
}: SlideProps & { translateY: number }) {
  return (
    <div
      className="slide-overlay-container"
      style={{
        transform: `translateY(${translateY}%)`,
        transition: "transform 700ms cubic-bezier(.17,.79,.42,1)",
      }}
    >
      {children}
    </div>
  );
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
