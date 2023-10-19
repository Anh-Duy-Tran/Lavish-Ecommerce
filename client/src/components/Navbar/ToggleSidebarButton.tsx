"use client";

import React from "react";

export function ToggleSidebarButton() {
  return (
    <button onClick={() => console.log("toggle sidebar")}>
      <div className="icon">{openSidebarIcon}</div>
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
