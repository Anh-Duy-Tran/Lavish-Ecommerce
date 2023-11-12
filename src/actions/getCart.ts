"use server";

import { CartItem } from "@prisma/client";
import { getServerSession } from "next-auth/next";
import { options } from "@/app/api/auth/[...nextauth]/options";
import prisma from "@/lib/prisma";

export async function getCart(): Promise<CartItem[] | undefined> {
  const session = await getServerSession(options);

  if (session?.user?.email) {
    const userWithCart = await prisma.user.findFirst({
      where: { email: session.user.email },
      select: { cart: { orderBy: { createdAt: "desc" } } },
    });

    if (userWithCart && userWithCart.cart) {
      return userWithCart.cart;
    }
  } else {
    // handle this error
    console.log("User not found!");
  }

  return [];
}
