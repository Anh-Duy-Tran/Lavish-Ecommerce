"use client";
import React from "react";
import { useUIStore } from "@/context/useUIStore";

export function Button() {
  const { bears, increase } = useUIStore();

  return (
    <button onClick={() => increase(1)}>Current num of bears: {bears}</button>
  );
}
