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

      <div className="p-2 flex flex-col relative">
        <div className="inline-block w-full overflow-hidden">
          <h3 className="whitespace-nowrap overflow-hidden text-ellipsis max-w-[40vw] tablet:max-w-[15vw]">
            {cartItem.name}
          </h3>
        </div>
        <h3>{`${cartItem.price / 100} EUR`}</h3>
        <h3>{`${cartItem.size} | ${cartItem.variantName}`}</h3>
        <CartItemQuantity id={cartItem.id} />
      </div>
    </div>
  );
}
