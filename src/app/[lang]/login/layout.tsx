import React from "react";
interface LoginLayoutProps {
  children: React.ReactNode;
}

export default function LoginLayout({ children }: LoginLayoutProps) {
  return (
    <div className="page-wrapper">
      <div className="page-container">{children}</div>
    </div>
  );
}
