"use server";

import prisma from "@/lib/prisma";
import { CartItem } from "@prisma/client";
import { getServerSession } from "next-auth/next";
import { options } from "@/app/api/auth/[...nextauth]/options";

export async function addProductToCart(cartItemData: CartItem) {
  const session = await getServerSession(options);

  if (session?.user?.email) {
    const user = await prisma.user.findUnique({
      where: { email: session.user.email },
    });

    if (user) {
      const cartItem = await prisma.cartItem.create({
        data: {
          ...cartItemData,
        },
      });
      console.log("Added to account cart:", cartItem);
      return cartItem;
    } else {
      throw new Error("User not found.");
    }
  } else {
    console.log("Add to local storage");
  }
}
