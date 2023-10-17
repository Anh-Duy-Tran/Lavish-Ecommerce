export type ScreenType =
  | "mobile"
  | "tablet"
  | "laptop"
  | "laptopHD"
  | "desktop"
  | "desktopHD"
  | "wide"
  | "ultraWide";

export const breakpoints: Record<ScreenType, number> = {
  mobile: 0,
  tablet: 767,
  laptop: 1024,
  laptopHD: 1280,
  desktop: 1600,
  desktopHD: 1920,
  wide: 2160,
  ultraWide: 2560,
};

export const containerWidthInString: Record<ScreenType, string> = {
  mobile: "100%",
  tablet: "676px",
  laptop: "892px",
  laptopHD: "1180px",
  desktop: "1372px",
  desktopHD: "1564px",
  wide: "1996px",
  ultraWide: "2092px",
};
