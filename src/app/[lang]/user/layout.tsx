import { Button } from "@/components/Button";
import Link from "next/link";
import React from "react";
interface PageProps {
  children: React.ReactNode;
}

export default function layout({ children }: PageProps) {
  return (
    <div className="page-wrapper">
      <div className="page-container">
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
        </div>
        {children}
      </div>
    </div>
  );
}
