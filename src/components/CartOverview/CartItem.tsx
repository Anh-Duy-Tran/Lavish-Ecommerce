import React from "react";
import { CartItem } from "@prisma/client";
import Image from "next/image";

interface CartItemProps {
  cartItem: CartItem;
}

export function CartItem({ cartItem }: CartItemProps) {
  return (
    <div className="w-[50vw] tablet:w-[25vw]">
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
            priority
            fill
          />
        </div>
      </div>
      <div className="p-2">
        <div>
          <h3>{cartItem.name}</h3>
          <h3>{`${cartItem.price / 100} EUR`}</h3>
        </div>
      </div>
    </div>
  );
}
