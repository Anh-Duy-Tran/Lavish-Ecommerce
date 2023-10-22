import React from "react";
import "./navbar.css";
import { ThemeSwitcher } from "../ThemeSwitcher";
import Link from "next/link";
import Image from "next/image";
import { ToggleSidebarButton } from "./ToggleSidebarButton";
import { NavigationLinks } from "./NavigationLinks";
// import { useCategoryStore } from "@/context/useCategoryStore";

export function Navbar() {
  // const categories = useCategoryStore.getState().categories;
  // console.log(categories);

  return (
    <div className="navbar-component">
      <div className="navbar-logo-wrapper">
        <div className="page-container">
          <Link href={"/"} style={{ zIndex: 11 }}>
            <Image
              priority
              src="/lavish.svg"
              alt="lavish-logo"
              width={0}
              height={0}
              className="icon h-full w-auto"
            />
          </Link>
        </div>
      </div>
      <div className="navbar-content-wrapper">
        <ToggleSidebarButton />
        <div className="flex flex-col h-full justify-between items-end">
          <NavigationLinks />
          <div>
            <ThemeSwitcher />
          </div>
        </div>
      </div>
    </div>
  );
}
