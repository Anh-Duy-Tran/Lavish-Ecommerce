import React from "react";

import { Montserrat } from "next/font/google";
import { ThemeProvider } from "./theme-prodiver";
import "./globals.css";
import { Navbar } from "@/components/Navbar";

export const font = Montserrat({
  weight: ["200", "400", "700"],
  subsets: ["latin"],
});

export const metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <main className={font.className}>
            <Navbar />
            {children}
          </main>
        </ThemeProvider>
      </body>
    </html>
  );
}
