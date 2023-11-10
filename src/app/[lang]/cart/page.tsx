"use client";

import { useCartStore } from "@/context/useCartStore";
import React from "react";

export default function page() {
  const { cart } = useCartStore();

  return <div>{JSON.stringify(cart)}</div>;
}
