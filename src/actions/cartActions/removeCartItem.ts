"use server";

import prisma from "@/lib/prisma";
import { getServerSession } from "next-auth/next";
import { options } from "@/app/api/auth/[...nextauth]/options";

export async function removeCartItem(cartItemId: string) {
  const session = await getServerSession(options);

  if (session?.user?.email) {
    const user = await prisma.user.findUnique({
      where: { email: session.user.email },
    });

    if (user) {
      const cartItem = await prisma.cartItem.findFirst({
        where: { id: cartItemId },
      });

      if (!cartItem) {
        // should send message to client and not throw ?
        throw new Error("User not found.");
      }

      const deletedCartItem = await prisma.cartItem.delete({
        where: {
          id: cartItemId,
        },
      });
      return deletedCartItem;
    } else {
      throw new Error("User not found.");
    }
  }
  throw new Error("Not authenticated");
}
