"use client";

import { useCategoryStore } from "@/context/useCategoryStore";
import "./sidebar.css";
import { useUIStore } from "@/context/useUIStore";
import { usePathname } from "next/navigation";
import React from "react";
import { Button } from "@/components/Button";
import { isRootPath } from "@/utils/isRootPath";

export function Sidebar() {
  const { isSidebarOpen } = useUIStore();
  const pathname = usePathname() || "/";

  return (
    <div className={`sidebar-wrapper`}>
      <div className="page-container">
        <div
          className={`sidebar-container${
            isSidebarOpen ? " opacity-100 visible" : " opacity-0 invisible"
          }`}
        >
          <div className="add-padding-top mt-[-20px] z-30 ml-3 tablet:ml-0">
            {!isRootPath(pathname) ? <SidebarCategoryButton /> : <div />}
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
          {category.displayName}
        </Button>
      ))}
    </div>
  );
}
