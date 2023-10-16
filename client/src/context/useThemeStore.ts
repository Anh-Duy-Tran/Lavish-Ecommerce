import { create } from "zustand";
import { persist } from "zustand/middleware";

type ThemeState = {
  mode: "dark" | "light";
  toggleMode: () => void;
};

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      mode: "light",
      toggleMode: () => set({ mode: get().mode === "dark" ? "light" : "dark" }),
    }),
    {
      name: "theme-storage",
    }
  )
);
