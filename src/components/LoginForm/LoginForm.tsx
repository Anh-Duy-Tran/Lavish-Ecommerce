"use client";

import React from "react";
import "./loginForm.css";
import { InputField } from "../InputField/InputField";
import { SubmitHandler, useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as Yup from "yup";
import { Button } from "../Button";
import Link from "next/link";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useUIStore } from "@/context/useUIStore";
import { getCart } from "@/actions/cartActions/getCart";
import { useCartStore } from "@/context/useCartStore";
import { useGuestCartStore } from "@/context/useGuestCartStore";

export type LoginFormType = {
  email: string;
  password: string;
};

export function LoginForm() {
  const router = useRouter();
  const { setInitialCart } = useCartStore();
  const { setGuestCart } = useGuestCartStore();

  const { setLoadingModalContent } = useUIStore();

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

  const onSubmit: SubmitHandler<LoginFormType> = async (data) => {
    const signInResponse = await setLoadingModalContent(
      signIn("credentials", {
        ...data,
        redirect: false,
      }),
      (res) =>
        res?.ok
          ? null
          : { title: "LOGIN FAILED", message: "Wrong credentials" },
    );

    const userCart = await getCart();
    console.log("loading from user cart db: ", userCart);

    if (userCart) {
      // flush guest cart
      setGuestCart([]);

      setInitialCart(userCart);
    } else {
      // handle this error
      console.log("some thing wrong");
    }

    if (signInResponse?.ok) {
      router.back();
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
