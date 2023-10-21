"use client";

import { useCategoryStore } from "@/context/useCategoryStore";
import { useRef } from "react";

function CategoryStoreInitializer(props) {
  const initialized = useRef(false);
  if (!initialized.current) {
    useCategoryStore.setState(props);
    initialized.current = true;
  }
  return null;
}

export default CategoryStoreInitializer;
