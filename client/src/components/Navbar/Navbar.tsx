import React from "react";
import "./navbar.css";
import { ThemeSwitcher } from "../ThemeSwitcher";
import Link from "next/link";
import Image from "next/image";

export function Navbar() {
  return (
    <div className="navbar-component">
      <div className="navbar-logo-wrapper">
        <div className="page-container border border-blue-500">
          <Link href={"/"} style={{ zIndex: 11 }}>
            <Image
              src="/lavish.svg"
              alt="lavish-logo"
              width={0}
              height={0}
              className="dark:invert h-full w-auto transition duration-config"
            />
          </Link>
        </div>
      </div>
      <div className="navbar-content-wrapper">
        <div className="w-full h-full border border-green-500">
          <ThemeSwitcher />
        </div>
      </div>
    </div>
  );
}
