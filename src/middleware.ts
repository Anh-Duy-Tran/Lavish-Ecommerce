import { match } from "@formatjs/intl-localematcher";
import Negotiator from "negotiator";
import { NextResponse, type NextRequest } from "next/server";

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
  // Check if the pathname ends with .svg or is requesting api

  if (
    request.nextUrl.pathname.startsWith("/api") ||
    request.nextUrl.pathname.endsWith(".svg")
  ) {
    return;
  }

  // Check if there is any supported locale in the pathname
  const { pathname } = request.nextUrl;
  const pathnameLocaleIndex = locales.findIndex(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`,
  );
  const pathnameHasLocale = pathnameLocaleIndex !== -1;

  let cookieLocale = request.cookies.get("preferred-locale")?.value;
  if (pathnameHasLocale) {
    if (!cookieLocale) {
      const setCookieResponse = NextResponse.next();
      setCookieResponse.cookies.set(
        "preferred-locale",
        locales[pathnameLocaleIndex],
      );
      return setCookieResponse;
    } else {
      return;
    }
  }

  // Redirect if there is no locale
  cookieLocale =
    cookieLocale && locales.some((local) => local === cookieLocale)
      ? cookieLocale
      : getLocale(request);
  request.nextUrl.pathname = `/${cookieLocale}${pathname}`;

  const redirectResponse = NextResponse.redirect(request.nextUrl);

  redirectResponse.cookies.set("preferred-locale", cookieLocale);

  return redirectResponse;
}

export const config = {
  matcher: [
    // Skip all internal paths (_next)
    "/((?!_next).*)",
    // Optional: only run on root (/) URL
    "/",
  ],
};
