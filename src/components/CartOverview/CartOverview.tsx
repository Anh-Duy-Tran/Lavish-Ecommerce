"use client";

import { useCartStore } from "@/context/useCartStore";

import React from "react";
import { CartItem } from "./CartItem";

export function CartOverview() {
  const { cart } = useCartStore();
  return (
    <div className="add-padding-top w-full flex justify-center flex-col items-center">
      <div className="page-container p-5 tablet:p-0 tablet:pb-6 flex flex-col">
        <h1>SHOPPING CART</h1>
        {cart.length === 0 ? (
          <div className="pt-[60px] border-t border-black dark:border-white flex flex-col gap-4">
            {emptyCart}
            <h3>YOUR CART IS EMPTY</h3>
          </div>
        ) : null}
      </div>
      <div className="grid grid-cols-2 tablet:grid-cols-4 border-b border-t border-black dark:border-white">
        {cart.map((cartItem, i) => (
          <CartItem key={i} cartItem={cartItem} />
        ))}
      </div>
    </div>
  );
}

const emptyCart = (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    fill="inherit"
    stroke="inherit"
    className="icon"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M9.708 5a2.5 2.5 0 0 1 4.584 0H9.708zM8.645 5a3.502 3.502 0 0 1 6.71 0H19v15H5V5h3.645zM6 6v13h12V6H6z"
    ></path>
  </svg>
);
