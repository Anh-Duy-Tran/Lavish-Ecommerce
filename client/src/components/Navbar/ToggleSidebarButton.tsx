"use client";

import { useUIStore } from "@/context/useUIStore";
import React from "react";

export function ToggleSidebarButton() {
  const { isSidebarOpen, toggleSidebar } = useUIStore();

  return (
    <button id="toggle-sidebar-button" onClick={toggleSidebar}>
      <div className="icon">
        {isSidebarOpen ? closeSidebarIcon : openSidebarIcon}
      </div>
    </button>
  );
}

const openSidebarIcon = (
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
      d="M20.4 6.9H3.6v-1h16.8v1zm0 11.2H3.6v-1h16.8v1z"
    ></path>
  </svg>
);

const closeSidebarIcon = (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    fill="inherit"
    stroke="inherit"
    className="layout-header-icon__icon"
  >
    <path d="M12 12.707l6.846 6.846.708-.707L12.707 12l6.847-6.846-.707-.708L12 11.293 5.154 4.446l-.707.708L11.293 12l-6.846 6.846.707.707L12 12.707z"></path>
  </svg>
);
