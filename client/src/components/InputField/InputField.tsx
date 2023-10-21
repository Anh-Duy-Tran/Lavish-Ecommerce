"use client";

import React, { InputHTMLAttributes, useState } from "react";
import {
  Control,
  FieldValues,
  Path,
  UseFormRegisterReturn,
  useController,
} from "react-hook-form";
import { twMerge } from "tailwind-merge";
import { VariantProps, tv } from "tailwind-variants";

interface InputFieldProps<T extends FieldValues>
  extends InputHTMLAttributes<HTMLInputElement>,
    VariantProps<typeof inputFieldVariant> {
  title: string;
  name: Path<T>;
  helperText?: string;
  register?: UseFormRegisterReturn;
  control?: Control<T>;
}

export function InputField<T extends FieldValues>({
  name,
  title,
  className,
  control,
  defaultValue,
  helperText,
  register,
  ...props
}: InputFieldProps<T>) {
  const [hasValue, setHasValue] = useState(!!defaultValue);
  const { onChange, ...registerFunc } = register
    ? register
    : { onChange: () => {} };

  const handleChange = (e: React.FocusEvent<HTMLInputElement>) => {
    setHasValue(e.target.value.length !== 0);
    onChange(e);
  };

  const {
    fieldState: { error },
  } = useController({
    name,
    control,
  });

  return (
    <div className="flex flex-col relative pt-6 w-full">
      <input
        {...registerFunc}
        {...props}
        name={name}
        onChange={handleChange}
        className={twMerge(inputFieldVariant({ error: !!error }), className)}
      />
      <label
        className={`absolute opacity-50 origin-left peer-focus:-translate-y-5 peer-focus:scale-75 
        transition-all linear duration-config select-none pointer-events-none ${
          hasValue ? "-translate-y-5 scale-75" : ""
        }`}
      >
        <p>{title}</p>
      </label>

      <div
        className={twMerge(
          `flex items-center gap-3 mt-0.5 dark:fill-white peer-focus:visible`,
          error
            ? "text-red-500 fill-red-500 dark:fill-red-500 visible"
            : "invisible"
        )}
      >
        {(error && error.message) || helperText ? infoIcon : null}
        <h3 className="">{(error && error.message) || helperText}</h3>
      </div>
    </div>
  );
}

const inputFieldVariant = tv({
  base: "peer bg-transparent border-b border-black/20 dark:border-white/20 focus:border-black focus:dark:border-white w-full outline-none transition-all duration-config",
  variants: {
    error: {
      true: "border-red-500 dark:border-red-500",
    },
  },
});

const infoIcon = (
  <svg
    width="20"
    height="20"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    fill="inherit"
    stroke="inherit"
  >
    <path d="M11.5 16.8v-1.2h1v1.2h-1zm0-9.6v7.2h1V7.2h-1z"></path>
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M12 21.6a9.6 9.6 0 0 0 9.6-9.6 9.6 9.6 0 1 0-19.2 0 9.6 9.6 0 0 0 9.6 9.6zm0-1a8.6 8.6 0 1 0 0-17.2 8.6 8.6 0 0 0 0 17.2z"
    ></path>
  </svg>
);
