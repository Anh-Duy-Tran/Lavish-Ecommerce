import React from "react";
import { CartItem } from "@prisma/client";
import Image from "next/image";
import { CartItemQuantity } from "./CartItemQuantity";

interface CartItemProps {
  cartItem: CartItem;
}

export function CartItem({ cartItem }: CartItemProps) {
  return (
    <div className="w-full">
      <div className="relative aspect-[2/3] w-full overflow-hidden">
        <div className="relative h-full w-full">
          <Image
            src={cartItem.media}
            alt={cartItem.name}
            style={{
              userSelect: "none",
              pointerEvents: "none",
              objectFit: "cover",
            }}
            sizes="(max-width: 768px) 50vw, 20vw"
            priority
            fill
          />
        </div>
      </div>
      <div className="flex p-2 justify-between">
        <div className="flex flex-col">
          <div className="inline-block w-full overflow-hidden">
            <h3 className="whitespace-nowrap overflow-hidden text-ellipsis max-w-[40vw] tablet:max-w-[15vw]">
              {cartItem.name}
            </h3>
          </div>
          <h3>{`${cartItem.price / 100} EUR`}</h3>
          <h3>{`${cartItem.size} | ${cartItem.variantName}`}</h3>
          <CartItemQuantity id={cartItem.id} />
        </div>

        <div>
          <button>{removeCartItemIcon}</button>
        </div>
      </div>
    </div>
  );
}

const removeCartItemIcon = (
  <svg
    width="20"
    height="20"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    fill="inherit"
    stroke="inherit"
    className="icon"
  >
    <path d="M12 12.707l6.846 6.846.708-.707L12.707 12l6.847-6.846-.707-.708L12 11.293 5.154 4.446l-.707.708L11.293 12l-6.846 6.846.707.707L12 12.707z"></path>
  </svg>
);
