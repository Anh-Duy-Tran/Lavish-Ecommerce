import React from "react";

export default function LoginLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="page-wrapper">
      <div className="page-container">{children}</div>
    </div>
  );
}
