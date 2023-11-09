import { Button } from "@/components/Button";
import { getServerSession } from "next-auth";
import Link from "next/link";
import React from "react";
import { options } from "@/app/api/auth/[...nextauth]/options";
import { redirect } from "next/navigation";
interface PageProps {
  children: React.ReactNode;
}

export default async function layout({ children }: PageProps) {
  const session = await getServerSession(options);

  if (!session) {
    redirect("/login");
  }

  return (
    <div className="page-wrapper">
      <div className="page-container flex flex-col gap-8">
        <div className="flex gap-3">
          <Link href={"/user/orders"}>
            <Button variant="outlined" size="compact">
              PURCHASES
            </Button>
          </Link>
          <Link href={"/user/profile"}>
            <Button variant="outlined" size="compact">
              PROFILE
            </Button>
          </Link>
          <Link href={"/user/favourites"}>
            <Button variant="outlined" size="compact">
              FAVOURITE
            </Button>
          </Link>
        </div>
        {children}
      </div>
    </div>
  );
}
