import { getServerSession } from "next-auth";
import { options } from "@/app/api/auth/[...nextauth]/options";
import React from "react";
import { redirect } from "next/navigation";
import Link from "next/link";
import { Signout } from "./Signout";
import prisma from "@/lib/prisma";

export default async function page() {
  const session = await getServerSession(options);

  if (!session) {
    return redirect("/login");
  }

  const user =
    session.user && session.user.email
      ? await prisma.user.findFirst({
          where: { email: session.user.email },
        })
      : undefined;

  const profileEditLinks = [
    {
      name: "ADDRESSES",
      href: "/user/address",
    },
    {
      name: "WALLET",
      href: "/user/payment",
    },
    {
      name: "EMAIL",
      href: "/user/change-data/email",
      currentValue: user?.email,
    },
    {
      name: "PHONE",
      href: "/user/change-data/phone",
      currentValue: `${user?.prefix} ${user?.phoneNumber}`,
    },
    {
      name: "CHANGE PASSWORD",
      href: "/user/change-data/password",
      currentValue: "••••••••••••",
    },
  ];
  if (!user) {
    return redirect("/login");
  }

  return (
    <div className="w-full tablet:w-[50%] flex flex-col gap-5">
      <p>{`${user.firstName.toUpperCase()} ${user.lastName.toUpperCase()}`}</p>
      <div className="w-full p-2 py-4 border border-black/40 flex flex-col gap-5">
        {profileEditLinks.map((link) => (
          <Link href={link.href} key={link.name}>
            <div className="flex justify-between p-2 items-center">
              <div>
                <p>{link.name}</p>
                {link.currentValue ? (
                  <h3 className="text-black/50">{link.currentValue}</h3>
                ) : null}
              </div>
              <div>{LinkArrow}</div>
            </div>
          </Link>
        ))}
      </div>

      <Signout />

      <h3 className="underline text-black/50 w-fit cursor-pointer">
        Delete your account
      </h3>
    </div>
  );
}

const LinkArrow = (
  <svg
    width="20"
    height="20"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    fill="inherit"
    stroke="inherit"
    className="icon"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M15.336 12 8.624 4.33l.752-.66L16.665 12l-7.289 8.33-.752-.66L15.336 12Z"
    ></path>
  </svg>
);
