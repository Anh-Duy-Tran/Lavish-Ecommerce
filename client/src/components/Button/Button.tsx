import React from "react";
import { Palette } from "@/theme/palettes";
import { usePalette } from "@/theme/usePalette";
import {
  Button as ButtonMUI,
  ButtonProps as ButtonMUIProps,
  buttonClasses,
} from "@mui/base";
import { styled } from "@mui/system";
import { Typography } from "@/components/Typography";

export type ButtonVariantType = "text" | "contained" | "outlined";

export type ButtonSizeType = "compact" | "standard" | "large";

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
      <Typography variant="text" compact>
        {label || children}
      </Typography>
    </StyledButton>
  );
}

export const StyledButton = styled(ButtonMUI, {
  shouldForwardProp: (props) =>
    !["fullWidth", "active", "palette"].includes(props as string),
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

  min-height: 20px;
  min-width: 20px;
  cursor: pointer;
  width: ${width ? `${width}px` : fullWidth ? "100%" : `auto`};
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;

  padding: ${
    size === "large"
      ? "18px 14px"
      : size === "compact"
      ? "4px 12px"
      : "12px 14px"
  };
  border: ${
    variant === "outlined" ? `1px solid ${palette.primary.text}` : "none"
  };
  color: ${
    variant === "contained" ? palette.primary.background : palette.primary.text
  };
  background-color: ${
    variant === "contained" ? palette.primary.text : "transparent"
  };
  
  &::before {
    content: "";
    position: absolute;
    transform-origin: center;
    left: 50%;
    bottom: 0;
    transform: translate(-50%, -50%);
    border-radius: 4px;
    height: 3px;
    width: ${active ? "25px" : "0"};
    background-color: ${palette.primary.text};
    transition: width 100ms ease;
  }
  
  transition: background-color 300ms ease;
  transition: color 300ms ease;

  &.${buttonClasses.active} {
    ${
      variant === "contained"
        ? `background-color: ${palette.secondary.text};`
        : `color: ${palette.secondary.text};
           border-color: ${palette.secondary.text};`
    }
  }
`
);
