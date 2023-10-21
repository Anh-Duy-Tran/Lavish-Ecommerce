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
    extend: {
      width: {
        inherit: "inherit",
        mobile: "100%",
        tablet: "606px",
        laptop: "852px",
        laptopHD: "1130px",
        desktop: "1372px",
        desktopHS: "1564px",
        wide: "1996px",
        ultraWide: "2092px",
      },
      fontSize: {
        xxs: [
          "10px",
          {
            lineHeight: "12px",
          },
        ],
      },
      colors: {
        //background color
        bg: "#fff",
        //foreground color
        fg: "#000",
        //dark background color
        dbg: "#000",
        //dark foreground color
        dfg: "#fff",
      },
      transitionDuration: {
        config: "300ms",
      },
    },
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
