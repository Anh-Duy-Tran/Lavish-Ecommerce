import type { Config } from "tailwindcss";
import { withTV } from "tailwind-variants/transformer";

const config: Config = withTV({
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: ["class"],
  theme: {
    extend: {},
    screens: {
      tablet: "767px",
      laptop: "1024px",
      laptopHD: "1280px",
      desktop: "1600px",
      desktopHD: "1920px",
      wide: "2160px",
      ultraWide: "2560px",
    },
  },
  plugins: [],
});
export default config;
