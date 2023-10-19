import React from "react";
import "./navbar.css";
import { ThemeSwitcher } from "../ThemeSwitcher";

export function Navbar() {
  return (
    <div className="navbar-component">
      <div className="navbar-logo-wrapper"></div>
      <div className="navbar-content-wrapper">
        <div className="w-full h-full border border-green-500">
          <ThemeSwitcher />
        </div>
      </div>
    </div>
  );
}
