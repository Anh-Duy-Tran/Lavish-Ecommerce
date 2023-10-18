import React, { ButtonHTMLAttributes } from "react";
import { twMerge } from "tailwind-merge";
import { tv, type VariantProps } from "tailwind-variants";

export type ButtonVariantType = "text" | "contained" | "outlined";

export type ButtonSizeType = "compact" | "standard" | "large";

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariant> {
  children: React.ReactNode;
  active?: boolean;
}

export function Button({
  children,
  active,
  className,
  variant,
  size,
  fullWidth,
  ...props
}: ButtonProps) {
  return (
    <button
      {...props}
      className={twMerge(
        buttonVariant({ variant, size, fullWidth }),
        className,
      )}
    >
      <div
        className={`absolute bg-black dark:bg-white transform -translate-x-1/2 
        -translate-y-1/2 left-1/2 bottom-0 h-[2px] transition-width duration-100 ease-in`}
        style={{ width: active ? "25px" : "0px" }}
      />
      {children}
    </button>
  );
}

const buttonVariant = tv({
  base: "relative box-border text-black dark:text-white bg-transparent px-4 py-2 cursor-pointer \
       active:bg-gray-100 dark:active:bg-gray-800 transition-colors duration-300",
  variants: {
    variant: {
      contained:
        "text-white dark:text-black bg-black dark:bg-white active:bg-gray-800\
         dark:active:bg-gray-100",
      outlined: "border border-black dark:border-white",
      text: "",
    },
    size: {
      compact: "px-2 py-1",
      standard: "",
      large: "px-4 py-4",
    },
    fullWidth: {
      true: "w-full",
    },
  },
});
