"use client";

import { useCategoryStore } from "@/context/useCategoryStore";
import "./sidebar.css";
import { useTransition, animated } from "@react-spring/web";
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

  const transition = useTransition(isSidebarOpen, {
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
      duration: 100
    }
  });

  return (
    <>
      {transition((style, isSidebarOpen) => (
        <>
          {isSidebarOpen ? (
            <div
              className={`sidebar-wrapper`}
              style={{ opacity: style.opacity }}
            >
              <div className="page-container">
                <div className={`sidebar-container`} style={{ opacity: style.opacity}}>
                  <div className="add-padding-top z-30 ml-3 tablet:ml-0 h-16">
                    {!isRootPath(pathname) ? (
                      <SidebarCategoryButton />
                    ) : (
                      <div />
                    )}
                  </div>

                  <div className="flex-grow">
                    <div className="flex justify-end flex-wrap gap-3 mt-16 p-4 pl-20 desktop:pl-14 desktopHD:pl-24">
                      {categories[
                        currentCategoryIndex
                      ].subCategoriesCollection.items.map((category) => {
                        return (
                          <Link key={category.slug} href={`/${category.slug}`}>
                            <Button size="compact" variant="outlined">
                              {category.displayName}
                            </Button>
                          </Link>
                        );
                      })}
                    </div>
                  </div>
                  <div className="flex justify-between p-3">
                    <div className="flex items-end gap-6">
                      <Link
                        href={`${pathname.replace("vi", "en")}`}
                        onClick={() =>
                          cookieCutter.set("preferred-locale", "en", {
                            path: "/",
                          })
                        }
                      >
                        <p>English</p>
                      </Link>
                      <Link
                        href={`${pathname.replace("en", "vi")}`}
                        onClick={() =>
                          cookieCutter.set("preferred-locale", "vi", {
                            path: "/",
                          })
                        }
                      >
                        <p>Tieng Viet</p>
                      </Link>
                    </div>
                    <label className="switch">
                      <input
                        onChange={() =>
                          setTheme(theme === "dark" ? "light" : "dark")
                        }
                        checked={theme === "dark"}
                        type="checkbox"
                      />
                      <span className="slider"></span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          ) : null}
        </>
      ))}
    </>
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
