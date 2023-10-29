"use client";

import "./sidebar.css";
import { useTransition, animated } from "@react-spring/web";
import React, { useEffect } from "react";
import { useFilterStore } from "@/context/useFilterStore";
import { Button } from "../Button";

export function ProductFilterModal() {
  const { filters, currentOpenFilter, isFilterOpen, closeFilter } =
    useFilterStore();

  const transition = useTransition(isFilterOpen, {
    from: {
      opacity: 0,
    },
    enter: {
      opacity: 1,
    },
    leave: {
      opacity: 0,
    },
    config: {
      duration: 100,
    },
  });

  return (
    <>
      {transition((style, isOpen) => (
        <>
          {isOpen ? (
            <>
              <div
                className="fixed w-full h-full z-10"
                onClick={closeFilter}
              ></div>
              <animated.div className={`filter-modal-wrapper`} style={style}>
                <div
                  className="flex page-container add-padding-top mt-12"
                  onClick={closeFilter}
                >
                  <div
                    className={`filter-modal-container`}
                    onClick={(e) => e.stopPropagation()}
                  >
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(100px, 1fr))",
                        // gridAutoRows: "20px",
                        gridGap: "5px",
                      }}
                    >
                      {Object.keys(filters[currentOpenFilter as string]).map(
                        (value) => (
                          <div key={value}>
                            <Button fullWidth variant="outlined">{value}</Button>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                </div>
              </animated.div>
            </>
          ) : null}
        </>
      ))}
    </>
  );
}
