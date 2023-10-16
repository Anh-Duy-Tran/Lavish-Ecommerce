"use client";

import React from "react";
import { Palette } from "@/theme/palettes";
import { usePalette } from "@/theme/usePalette";
import {
  Button as ButtonMUI,
  ButtonProps as ButtonMUIProps,
  buttonClasses,
} from "@mui/base";
import { styled } from "@mui/system";

export type ButtonVariantType = "text" | "contained" | "outlined";

export type ButtonSizeType = "small" | "standard" | "large";

export interface ButtonProps extends ButtonMUIProps {
  /**
   * Defines the visual style of the button as either "text", "contained", or "outlined".
   * - "text": A button with no background and a basic appearance.
   * - "contained": A button with a solid background color, ideally used for the principal call to action on the page.
   * - "outlined": A button with a border and no background color.
   */
  variant?: ButtonVariantType;
  /**
   * Specifies the size of the button.
   */
  size?: ButtonSizeType;
  /**
   * Defines the button contents.
   */
  label?: string;
  /**
   * Sets the button width in number of pixels.
   */
  width?: number;
  /**
   * Determines whether the button should occupy all available space.
   */
  fullWidth?: boolean;
  /**
   * toggleable button (only visible in "text" button varian)
   */
  active?: boolean;
}

export function Button({
  variant = "outlined",
  size = "standard",
  label,
  children,
  ...props
}: ButtonProps) {
  const palette = usePalette();

  return (
    <StyledButton palette={palette} variant={variant} size={size} {...props}>
      {label || children}
    </StyledButton>
  );
}

const StyledButton = styled(ButtonMUI, {
  shouldForwardProp: (props) => props !== "fullWidth" && props !== "active",
})(
  ({
    palette,
    active,
    variant,
    size,
    width,
    fullWidth,
  }: ButtonProps & { palette: Palette }) => `
  all: unset;
  position: relative;
  font-weight: 600;
  text-align: center;
  width: ${fullWidth ? "100%" : width ? `${width}px` : "auto"};
  font-size: 1,125rem;
  background-color: ${variant === "contained" ? palette.primary : "white"};
  padding: ${
    size === "large" ? "18px 14px" : size === "small" ? "4px 12px" : "12px 14px"
  };
  border-radius: 4px;
  
  &::before {
    content: ""; /* Create an empty pseudo-element for the line indicator */
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 4px;
    height: ${
      active ? "4px" : "0"
    }; /* Set the height of the line based on 'active' */
    background-color: ${palette.primary}; /* Color of the line */
    transition: height 100ms ease; /* Transition only the height property */
  }

  outline: ${variant === "outlined" ? `2px solid ${palette.primary}` : "none"};
  color: ${variant === "contained" ? "white" : palette.primary};
  transition: all 150ms ease;
  cursor: pointer;
  box-sizing: border-box;

  &:hover {
    background-color: ${
      variant === "contained" ? palette.primary : palette.primary
    };
  }

  &.${buttonClasses.active} {
    background-color: ${
      variant === "contained" ? palette.primary : palette.primary
    };
  }
`,
);
