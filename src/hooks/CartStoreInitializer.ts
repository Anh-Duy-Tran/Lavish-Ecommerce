"use client";

import { CartStoreType, useCartStore } from "@/context/useCartStore";
import { useRef } from "react";

function CartStoreInitializer(props: Partial<CartStoreType>) {
  const initialized = useRef(false);
  if (!initialized.current) {
    useCartStore.setState(props);
    initialized.current = true;
  }
  return null;
}

export default CartStoreInitializer;
