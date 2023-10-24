"use client";

import {
  CategoryStoreType,
  useCategoryStore,
} from "@/context/useCategoryStore";
import { useRef } from "react";

function CategoryStoreInitializer(props: Partial<CategoryStoreType>) {
  const initialized = useRef(false);
  if (!initialized.current) {
    useCategoryStore.setState(props);
    initialized.current = true;
  }
  return null;
}

export default CategoryStoreInitializer;
