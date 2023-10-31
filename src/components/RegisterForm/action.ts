"use server";

import prisma from "@/lib/prisma";
import { RegisterFormType } from "./RegisterForm";
import bcrypt from "bcryptjs";

export async function myAction(formData: RegisterFormType): Promise<{
  ok: boolean;
  message: string;
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
      message: "New account created.",
    };
  } catch (error) {
    return {
      ok: false,
      message: "Something went wrong.",
    };
  }
}
