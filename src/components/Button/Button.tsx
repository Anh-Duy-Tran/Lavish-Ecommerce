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
        className={`absolute bg-fg dark:bg-dfg transform -translate-x-1/2 
        -translate-y-1/2 left-1/2 bottom-0 h-[2px] transition-width duration-100`}
        style={{ width: active ? "25px" : "0px" }}
      />
      <h2 style={{ whiteSpace: "nowrap"}}>{children}</h2>
    </button>
  );
}

const buttonVariant = tv({
  base: "relative box-border text-fg dark:text-dfg bg-transparent px-4 py-2 cursor-pointer \
       active:bg-gray-100/20 dark:active:bg-gray-800/20 transition duration-config select-none",
  variants: {
    variant: {
      contained:
        "text-dfg dark:text-fg bg-dbg dark:bg-bg active:bg-gray-800\
         dark:active:bg-gray-100",
      outlined: "border border-fg dark:border-dfg",
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
