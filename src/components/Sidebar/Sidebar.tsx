"use client";

import { useCategoryStore } from "@/context/useCategoryStore";
import "./sidebar.css";
import { useUIStore } from "@/context/useUIStore";
import { usePathname } from "next/navigation";
import React from "react";
import { Button } from "@/components/Button";
import { isRootPath } from "@/utils/isRootPath";
import { useTheme } from "next-themes";
import Link from "next/link";
import cookieCutter from "@boiseitguru/cookie-cutter";

export function Sidebar() {
  const { isSidebarOpen } = useUIStore();
  const pathname = usePathname() || "/";
  const { categories } = useCategoryStore();
  const { currentCategoryIndex } = useUIStore();
  const { theme, setTheme } = useTheme();

  return (
    <div className={`sidebar-wrapper`}>
      <div className="page-container">
        <div
          className={`sidebar-container${
            isSidebarOpen ? " opacity-100 visible" : " opacity-0 invisible"
          }`}
        >
          <div className="add-padding-top z-30 ml-3 tablet:ml-0">
            {!isRootPath(pathname) ? <SidebarCategoryButton /> : <div />}
          </div>

          <div className="flex-grow">
            <div className="flex justify-end flex-wrap gap-3 mt-16 p-4 pl-20 desktop:pl-14 desktopHD:pl-24">
              {categories[
                currentCategoryIndex
              ].subCategoriesCollection.items.map((category) => {
                return (
                  <Button variant="outlined" key={category.slug}>
                    {category.displayName}
                  </Button>
                );
              })}
            </div>
          </div>
          <div className="flex justify-between p-3">
            <div className="flex items-end gap-6">
              <Link
                href={`${pathname.replace("vi", "en")}`}
                onClick={() =>
                  cookieCutter.set("preferred-locale", "en", { path: "/" })
                }
              >
                <p>English</p>
              </Link>
              <Link
                href={`${pathname.replace("en", "vi")}`}
                onClick={() =>
                  cookieCutter.set("preferred-locale", "vi", { path: "/" })
                }
              >
                <p>Tieng Viet</p>
              </Link>
            </div>
            <label className="switch">
              <input
                onChange={() => setTheme(theme === "dark" ? "light" : "dark")}
                checked={theme === "dark"}
                type="checkbox"
              />
              <span className="slider"></span>
            </label>
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
