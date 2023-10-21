"use client";

import { useCategoryStore } from "@/context/useCategoryStore";
import "./sidebar.css";
import { useUIStore } from "@/context/useUIStore";
import { usePathname } from "next/navigation";
import React from "react";
import { Button } from "@/components/Button";

export function Sidebar() {
  const { isSidebarOpen } = useUIStore();
  const pathname = usePathname() || "/";

  return (
    <div className={`sidebar-wrapper${!isSidebarOpen ? " hidden" : " flex"}`}>
      <div className="page-container">
        <div className="sidebar-container">
          <div className="add-padding-top mt-[-20px] z-30">
            {pathname !== "/" ? <SidebarCategoryButton /> : <div />}
          </div>
        </div>
      </div>
    </div>
  );
}

export function SidebarCategoryButton() {
  const { currentCategoryIndex, setCurrentCategoryIndex } = useUIStore();
  const { categories } = useCategoryStore();
  return (
    <div className="flex gap-2 laptop:gap-4">
      {categories.map((category, i) => (
        <Button
          size="compact"
          active={i === currentCategoryIndex}
          key={i}
          onClick={() => setCurrentCategoryIndex(i)}
        >
          {category.name}
        </Button>
      ))}
    </div>
  );
}
