import type { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const options: NextAuthOptions = {
  secret: process.env.NEXTAUTH_URL,
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: {
          label: "Email:",
          type: "email",
          placeholder: "email",
        },
        password: {
          label: "Password:",
          type: "password",
        },
      },
      async authorize(credentials) {
        // This is where you need to retrieve user data
        // to verify with credentials
        // Docs: https://next-auth.js.org/configuration/providers/credentials
        const user = {
          id: "42",
          name: "Duy",
          email: "duy@gmail.com",
          password: "nextauth",
        };

        if (
          credentials?.email === user.email &&
          credentials?.password === user.password
        ) {
          return await new Promise((resolve) =>
            setTimeout(() => resolve(user), 3000),
          );
        } else {
          return await new Promise((resolve) =>
            setTimeout(() => resolve(null), 3000),
          );
        }
      },
    }),
  ],
  pages: {
    signIn: "/login",
  },
};
