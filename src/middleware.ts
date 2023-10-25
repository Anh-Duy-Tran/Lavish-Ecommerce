import { match } from "@formatjs/intl-localematcher";
import Negotiator from "negotiator";
import type { NextRequest } from "next/server";

// Supported locale: English and Vietnamese
export const locales = ["en", "vi"];

function getLocale(request: NextRequest) {
  const languages = new Negotiator({
    headers: {
      "accept-language": request.headers.get("accept-language") as string,
    },
  }).languages();
  const defaultLocale = "en";

  return match(languages, locales, defaultLocale);
}

export function middleware(request: NextRequest) {
  // Check if the pathname ends with .svg
  console.log(request.nextUrl.pathname);
  if (
    request.nextUrl.pathname.startsWith("/api") ||
    request.nextUrl.pathname.endsWith(".svg")
  ) {
    return;
  }

  // Check if there is any supported locale in the pathname
  const { pathname } = request.nextUrl;
  const pathnameHasLocale = locales.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  );

  if (pathnameHasLocale) return;

  // Redirect if there is no locale
  const locale = getLocale(request);
  request.nextUrl.pathname = `/${locale}${pathname}`;
  // e.g. incoming request is /products
  // The new URL is now /en/products
  return Response.redirect(request.nextUrl);
}

export const config = {
  matcher: [
    // Skip all internal paths (_next)
    "/((?!_next).*)",
    // Optional: only run on root (/) URL
    "/",
  ],
};
