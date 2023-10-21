"use client";

import { useRef } from "react";

type SetStateFunction<T> = (
  partial: T | Partial<T> | ((state: T) => T | Partial<T>),
  replace?: boolean
) => void;

type StoreInitializerProps<T> = {
  setState: SetStateFunction<T>;
  initialState: Partial<T>;
};

function StoreInitializer<T>({
  setState,
  initialState,
}: StoreInitializerProps<T>) {
  const initialized = useRef(false);
  if (!initialized.current) {
    setState(initialState);
    initialized.current = true;
  }
  return null;
}

export default StoreInitializer;
