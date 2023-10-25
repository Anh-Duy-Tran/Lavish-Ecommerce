import { locales } from "@/middleware";

export function isRootPath(path: string): boolean {
  // Check for the original root path
  if (path === "/") return true;

  // Check for locale-based root paths
  for (const locale of locales) {
    if (path === `/${locale}/` || path === `/${locale}`) {
      return true;
    }
  }

  return false;
}
