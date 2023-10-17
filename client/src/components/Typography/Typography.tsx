"use client";

import { breakpoints } from "@/theme/breakpoints";
import { Palette } from "@/theme/palettes";
import { usePalette } from "@/theme/usePalette";
import { styled } from "@mui/system";
import { Montserrat } from "next/font/google";
import React, { ReactNode } from "react";

export const font = Montserrat({
  weight: ["500", "600", "700", "800"],
  subsets: ["latin"],
});

export type TypographyVariant = "heading" | "text" | "subtitle";

interface TypographyProps {
  bold?: boolean;
  children: ReactNode;
  variant: TypographyVariant;
  compact?: boolean;
  inline?: boolean;
}

export function Typography({
  children,
  variant,
  bold,
  compact,
  inline,
}: TypographyProps) {
  return (
    <StyledTypography
      inline={inline}
      style={compact ? { margin: "0px" } : {}}
      bold={bold}
      className={font.className}
      variant={variant}
    >
      {children}
    </StyledTypography>
  );
}

export const fontSizeLookup = {
  mobile: {
    heading: "13px",
    text: "13px",
    subtitle: "11px",
  },
  tablet: {
    heading: "13px",
    text: "13px",
    subtitle: "10px",
  },
  laptop: {
    heading: "15px",
    text: "13px",
    subtitle: "10px",
  },
  laptopHD: {
    heading: "18px",
    text: "15px",
    subtitle: "13px",
  },
};

const StyledTypography = styled("p")<TypographyProps>(
  ({ theme, bold, variant, inline }) => ({
    whiteSpace: inline ? "nowrap" : "normal",
    fontSize: fontSizeLookup["mobile"][variant],

    fontWeight: bold ? "700" : "500",
    [theme.breakpoints.up(breakpoints.tablet)]: {
      fontWeight: bold ? "900" : "600",
      fontSize: fontSizeLookup["tablet"][variant],
    },
    [theme.breakpoints.up(breakpoints.laptop)]: {
      fontSize: fontSizeLookup["laptop"][variant],
    },
    [theme.breakpoints.up(breakpoints.laptopHD)]: {
      fontSize: fontSizeLookup["laptopHD"][variant],
    },
  })
);
