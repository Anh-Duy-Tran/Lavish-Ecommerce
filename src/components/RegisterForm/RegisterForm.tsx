"use client";

import React, { useState } from "react";
import "./registerForm.css";
import { InputField } from "../InputField/InputField";
import { SubmitHandler, useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as Yup from "yup";
import { Button } from "../Button";

import prefixes from "./allowedPrefix.json";
import { myAction } from "./action";
import { useUIStore } from "@/context/useUIStore";

export type RegisterFormType = {
  email: string;
  password: string;
  password_repeat: string;
  first_name: string;
  last_name: string;
  prefix: string;
  phone_number: number;
};

export function RegisterForm() {
  const { setLoadingModalContent } = useUIStore();
  const [takenEmails, setTakenEmails] = useState<string[]>([]);
  const [takenPhoneNums, setTakenPhoneNums] = useState<number[]>([]);

  const validationSchema = Yup.object().shape({
    email: Yup.string()
      .required("Required field.")
      .email("Enter a valid e-mail address.")
      .notOneOf(takenEmails, "This email address is used by another account."),
    password: Yup.string()
      .required("Required field.")
      .min(8, "Password must be at least 8 characters long.")
      .matches(/[A-Z]/, "Password must contain at least one uppercase letter.")
      .matches(/[a-z]/, "Password must contain at least one lowercase letter.")
      .matches(/[0-9]/, "Password must contain at least one digit."),
    password_repeat: Yup.string()
      .required("Repeat required")
      .oneOf([Yup.ref("password")], "Passwords must match"),
    first_name: Yup.string().required("Required field."),
    last_name: Yup.string().required("Required field."),
    phone_number: Yup.number()
      .required("Required field.")
      .notOneOf(
        takenPhoneNums,
        "This phone number is used by another account.",
      ),
    prefix: Yup.string()
      .required("Required field.")
      .oneOf(prefixes, "Enter an valid prefix!"),
  });

  const { handleSubmit, register, control, setError } =
    useForm<RegisterFormType>({
      mode: "all",
      resolver: yupResolver(validationSchema),
      reValidateMode: "onChange",
    });

  const onSubmit: SubmitHandler<RegisterFormType> = async (data) => {
    await setLoadingModalContent(myAction(data), (res) => {
      if (res.errorField) {
        if (res.errorField === "email") {
          setTakenEmails((prev) => prev.concat(data.email));
        }
        if (res.errorField === "phone_number") {
          setTakenPhoneNums((prev) => prev.concat(data.phone_number));
        }
        setError(res.errorField, { message: res.message, type: "manual" });
      }
      return res.ok
        ? { title: "REGISTER SUCCESS", message: res.message }
        : { title: "REGISTER FAILED", message: res.message };
    });
  };

  return (
    <div className="register-form-container">
      <h1>PERSONAL DETAILS</h1>
      <form noValidate onSubmit={handleSubmit(onSubmit)}>
        <div className="register-form-grid">
          <div className="register-form-grid-item">
            <InputField
              title="E-MAIL"
              type="email"
              name="email"
              register={register("email")}
              helperText="Enter your email address."
              control={control}
            />
          </div>
          <div className="register-form-grid-item" />
        </div>
        <div className="register-form-grid">
          <div className="register-form-grid-item">
            <InputField
              autoComplete="new-password"
              title="PASSWORD"
              type="password"
              name="password"
              register={register("password")}
              helperText="Enter a password (at least 8 characters long)."
              control={control}
            />
          </div>
          <div className="register-form-grid-item">
            <InputField
              autoComplete="new-password"
              title="REPEAT PASSWORD"
              type="password"
              name="password_repeat"
              register={register("password_repeat")}
              helperText="Repeat the password to confirm."
              control={control}
            />
          </div>
        </div>
        <div className="register-form-grid">
          <div className="register-form-grid-item">
            <InputField
              autoComplete="given-name"
              title="FIRST NAME"
              type="text"
              name="first_name"
              register={register("first_name")}
              helperText="Enter your first name."
              control={control}
            />
          </div>
          <div className="register-form-grid-item">
            <InputField
              autoComplete="family-name"
              title="LAST NAME"
              type="text"
              name="last_name"
              helperText="Enter your last name."
              register={register("last_name")}
              control={control}
            />
          </div>
        </div>

        <div className="register-form-grid">
          <div className="register-form-grid-item">
            <div className="grid grid-cols-[1fr_4fr] gap-4">
              <InputField
                autoComplete="tel-country-code"
                title="PREFIX"
                type="text"
                name="prefix"
                register={register("prefix")}
                control={control}
              />

              <InputField
                autoComplete="tel-national"
                title="TELEPHONE"
                type="text"
                name="phone_number"
                register={register("phone_number")}
                helperText="Enter your phone number without the prefix."
                control={control}
              />
            </div>
          </div>
          <div className="register-form-grid-item" />
        </div>
        <div className="register-form-grid">
          <div className="register-form-grid-item">
            <Button
              type="submit"
              className="mt-[60px]"
              variant="contained"
              fullWidth
            >
              REGISTER
            </Button>
          </div>
          <div className="register-form-grid-item" />
        </div>
      </form>
    </div>
  );
}
