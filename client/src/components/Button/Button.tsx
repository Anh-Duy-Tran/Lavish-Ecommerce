"use client";
import { useUIStore } from "@/context/useUIStore";
import React from "react";

export function Button() {
  const { bears, increase } = useUIStore();

  return (
    <button onClick={() => increase(1)}>Current num of bears: {bears}</button>
  );
}
