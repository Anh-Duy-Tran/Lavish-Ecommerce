"use server";

import prisma from "@/lib/prisma";
import { RegisterFormType } from "./RegisterForm";
import bcrypt from "bcryptjs";
import { Path } from "react-hook-form";

export async function myAction(formData: RegisterFormType): Promise<{
  ok: boolean;
  message: string;
  errorField?: Path<RegisterFormType>;
}> {
  const {
    prefix,
    phone_number,
    last_name,
    first_name,
    password,
    password_repeat,
    email,
  } = formData;

  // Validate passwords
  if (password !== password_repeat) {
    return {
      ok: true,
      message: "Passwords don't match",
    };
  }

  // Hash the password
  const hashedPassword = await bcrypt.hash(password, 10);

  try {
    if (await prisma.user.findFirst({ where: { email: email } })) {
      return {
        ok: false,
        errorField: "email",
        message: `Email: ${email} has already been taken by another account.`,
      };
    }

    if (
      await prisma.user.findFirst({
        where: { phoneNumber: phone_number.toString() },
      })
    ) {
      return {
        ok: false,
        errorField: "phone_number",
        message: `Phone number: ${phone_number} has already been taken by another account.`,
      };
    }

    // Create a new user
    const newUser = await prisma.user.create({
      data: {
        firstName: first_name,
        lastName: last_name,
        email: email,
        password: hashedPassword,
        phoneNumber: phone_number.toString(),
        prefix: prefix,
      },
    });

    return {
      ok: true,
      message: `Welcome ${newUser.firstName}, your account has been successfully created.`,
    };
  } catch (error) {
    console.log(error);
    return {
      ok: false,
      message: "Something went wrong.",
    };
  }
}
