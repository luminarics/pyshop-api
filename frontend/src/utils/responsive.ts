import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { type Breakpoint } from "@/config/breakpoints";

// Enhanced cn function with responsive utilities
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Helper function to generate responsive classes
export function responsive<T extends Record<Breakpoint, string>>(
  breakpointValues: Partial<T>
): string {
  const classes: string[] = [];

  // Order matters for mobile-first approach
  const breakpointOrder: Breakpoint[] = ["xs", "sm", "md", "lg", "xl", "2xl"];

  for (const bp of breakpointOrder) {
    const value = breakpointValues[bp];
    if (value) {
      if (bp === "xs") {
        classes.push(value);
      } else {
        classes.push(`${bp}:${value}`);
      }
    }
  }

  return classes.join(" ");
}

// Simple responsive utilities - prefer direct Tailwind classes
export const responsiveUtils = {
  // Common patterns as string constants
  productGrid: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5",
  featureGrid: "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
  categoryGrid: "grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6",

  containerPadding: "px-4 sm:px-6 lg:px-8 xl:px-12",
  sectionPadding: "py-8 sm:py-12 lg:py-16 xl:py-20",
  cardPadding: "p-4 sm:p-6 lg:p-8",

  headingLarge: "text-2xl sm:text-3xl lg:text-4xl xl:text-5xl",
  headingMedium: "text-xl sm:text-2xl lg:text-3xl",
  headingSmall: "text-lg sm:text-xl lg:text-2xl",
};


// Simple visibility utilities (prefer Tailwind's hidden/block classes directly)
export const visibility = {
  mobileOnly: "block md:hidden",
  tabletOnly: "hidden md:block lg:hidden",
  desktopOnly: "hidden lg:block",
  mobileAndTablet: "block lg:hidden",
  tabletAndDesktop: "hidden md:block",
};
