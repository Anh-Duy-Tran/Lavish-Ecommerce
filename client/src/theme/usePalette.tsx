"use client";

import React, {
  createContext,
  useContext,
  ReactNode,
  useEffect,
  useState,
} from "react";
import { Palette, darkPalette, lightPalette } from "./palettes";
import { useThemeStore } from "@/context/useThemeStore";

interface PaletteProviderProps {
  children: ReactNode;
  modeProps?: "light" | "dark";
}

const PaletteContext = createContext<Palette | undefined>(undefined);

export const PaletteProvider: React.FC<PaletteProviderProps> = ({
  children,
  modeProps,
}) => {
  const themeStore = useThemeStore();
  const mode = modeProps || themeStore.mode;
  const [palette, setPalette] = useState<Palette>(lightPalette);

  useEffect(() => {
    // Update the palette when the mode changes
    setPalette(mode === "dark" ? darkPalette : lightPalette);
  }, [mode]);

  return (
    <PaletteContext.Provider value={palette}>
      {children}
    </PaletteContext.Provider>
  );
};

export const usePalette = (): Palette => {
  const context = useContext(PaletteContext);
  if (!context) {
    throw new Error("usePalette must be used within a PaletteProvider");
  }
  return context;
};
