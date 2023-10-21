import React from "react";
interface RegisterLayoutProps {
  children: React.ReactNode;
}

export default function RegisterLayout({ children }: RegisterLayoutProps) {
  return (
    <div className="page-wrapper">
      <div className="page-container">{children}</div>
    </div>
  );
}
