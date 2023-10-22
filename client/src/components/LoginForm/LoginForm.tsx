"use client";

import React, { useEffect } from "react";
import "./loginForm.css";
import { InputField } from "../InputField/InputField";
import { SubmitHandler, useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as Yup from "yup";
import { Button } from "../Button";
import Link from "next/link";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";

export type LoginFormType = {
  email: string;
  password: string;
};

interface LoginFormProps {
  callbackUrl?: string;
  error?: string;
}

export function LoginForm({ callbackUrl, error }: LoginFormProps) {
  const router = useRouter();
  const validationSchema = Yup.object().shape({
    email: Yup.string()
      .required("Required field.")
      .email("Enter a valid e-mail address."),
    password: Yup.string().required("Required field."),
  });

  const { handleSubmit, register, control } = useForm<LoginFormType>({
    mode: "all",
    resolver: yupResolver(validationSchema),
    reValidateMode: "onChange",
  });

  useEffect(() => {
    if (error) {
      alert("Wrong credentials");
    }
  }, [error]);

  const onSubmit: SubmitHandler<LoginFormType> = async (data) => {
    const signInResponse = await signIn("credentials", {
      ...data,
      redirect: false,
    });

    console.log(signInResponse);

    if (signInResponse?.ok) {
      router.push(callbackUrl ? callbackUrl : "/");
    }
  };

  return (
    <div className="login-form-container">
      <div className="login-form-grid">
        <div className="login-form-grid-item">
          <h1>LOG IN TO YOUR ACCOUNT</h1>
          <form noValidate onSubmit={handleSubmit(onSubmit)}>
            <InputField
              title="E-MAIL"
              type="email"
              name="email"
              register={register("email")}
              helperText="Enter your email address."
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
        <div className="login-form-grid-item">
          <h1>NEED AN ACCOUNT?</h1>
          <Link href={"/register"} passHref>
            <Button variant="outlined" fullWidth>
              REGISTER
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
