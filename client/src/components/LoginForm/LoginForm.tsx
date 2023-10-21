"use client";

import React from "react";
import "./loginForm.css";
import { InputField } from "../InputField/InputField";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as Yup from "yup";
import { Button } from "../Button";

export type LoginFormType = {
  email: string;
  password: string;
};

export function LoginForm() {
  const validationSchema = Yup.object().shape({
    email: Yup.string()
      .required("Required field.")
      .email("Enter a valid e-mail address."),
    password: Yup.string().required("Required field."),
  });

  const { register, control, formState } = useForm<LoginFormType>({
    mode: "all",
    resolver: yupResolver(validationSchema),
    reValidateMode: "onChange",
  });

  console.log(formState);

  return (
    <div className="w-full p-2 tablet:p-0">
      <div className="login-form-grid">
        <div className="grid-item">
          <h1>LOG IN TO YOUR ACCOUNT</h1>
          <form>
            <InputField
              title="E-MAIL"
              type="email"
              name="email"
              register={register("email")}
              helperText="Enter you email address."
              control={control}
            />
            <InputField
              title="PASSWORD"
              type="password"
              name="password"
              register={register("password")}
              control={control}
            />
            <Button
              type="submit"
              className="mt-[60px]"
              variant="contained"
              fullWidth
            >
              LOGIN
            </Button>
          </form>
        </div>
        <div className="grid-item">
          <h1>NEED AN ACCOUNT?</h1>
          <Button variant="outlined" fullWidth>
            REGISTER
          </Button>
        </div>
      </div>
    </div>
  );
}
