import React from "react";

import { Montserrat } from "next/font/google";
import { ThemeProvider } from "./theme-prodiver";
import "./globals.css";
import { Navbar } from "@/components/Navbar";
import { useCategoryStore } from "@/context/useCategoryStore";
import mockData from "./mockdata.json";
import { Sidebar } from "@/components/Sidebar";
import CategoryStoreInitializer from "@/hooks/CategoryStoreInitializer";

export const font = Montserrat({
  weight: ["200", "400", "700"],
  subsets: ["latin"],
});

export const metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const fetch = await Promise.resolve(mockData);

  useCategoryStore.setState({ categories: fetch });

  return (
    <html lang="en">
      <body>
        <CategoryStoreInitializer categories={fetch} />
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <main className={font.className}>
            <Navbar />
            {/* <Sidebar /> */}
            {children}
          </main>
        </ThemeProvider>
      </body>
    </html>
  );
}
