"use client";

import { useCategoryStore } from "@/context/useCategoryStore";
import "./sidebar.css";
import { useUIStore } from "@/context/useUIStore";
import React from "react";
import { Button } from "@/components/Button";

export function Sidebar() {
  const { currentCategoryIndex, isSidebarOpen, setCurrentCategoryIndex } = useUIStore();
  const { categories } = useCategoryStore();

  console.log(categories);

  return (
    <div className={`sidebar-wrapper${!isSidebarOpen ? " hidden" : " flex"}`}>
      <div className="page-container">
        <div className="sidebar-container">
          <div className="add-padding-top mt-[-20px]">
            {categories.map((category, i) => (
              <Button size="compact" active={i === currentCategoryIndex} key={i} onClick={() => setCurrentCategoryIndex(i)}>
                {category.name}
              </Button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
