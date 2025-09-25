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

// Responsive grid utilities
export const responsiveGridUtils = {
  // Product grid patterns
  productGrid: responsive({
    xs: "grid-cols-1",
    sm: "grid-cols-2",
    md: "grid-cols-2",
    lg: "grid-cols-3",
    xl: "grid-cols-4",
    "2xl": "grid-cols-5",
  }),

  // Category grid patterns
  categoryGrid: responsive({
    xs: "grid-cols-2",
    sm: "grid-cols-3",
    md: "grid-cols-4",
    lg: "grid-cols-6",
    xl: "grid-cols-8",
    "2xl": "grid-cols-10",
  }),

  // Feature grid patterns
  featureGrid: responsive({
    xs: "grid-cols-1",
    sm: "grid-cols-1",
    md: "grid-cols-2",
    lg: "grid-cols-3",
  }),

  // Blog/article grid patterns
  blogGrid: responsive({
    xs: "grid-cols-1",
    sm: "grid-cols-1",
    md: "grid-cols-2",
    lg: "grid-cols-2",
    xl: "grid-cols-3",
  }),

  // Common gap patterns
  gap: {
    small: responsive({
      xs: "gap-3",
      sm: "gap-4",
      md: "gap-4",
      lg: "gap-6",
    }),
    medium: responsive({
      xs: "gap-4",
      sm: "gap-6",
      md: "gap-6",
      lg: "gap-8",
    }),
    large: responsive({
      xs: "gap-6",
      sm: "gap-8",
      md: "gap-8",
      lg: "gap-10",
      xl: "gap-12",
    }),
  },

  // Padding patterns
  padding: {
    container: responsive({
      xs: "px-4",
      sm: "px-6",
      lg: "px-8",
      xl: "px-12",
      "2xl": "px-16",
    }),
    section: responsive({
      xs: "py-8",
      sm: "py-12",
      lg: "py-16",
      xl: "py-20",
      "2xl": "py-24",
    }),
    card: responsive({
      xs: "p-4",
      sm: "p-6",
      lg: "p-8",
    }),
  },

  // Text size patterns
  text: {
    h1: responsive({
      xs: "text-2xl",
      sm: "text-3xl",
      lg: "text-4xl",
      xl: "text-5xl",
    }),
    h2: responsive({
      xs: "text-xl",
      sm: "text-2xl",
      lg: "text-3xl",
      xl: "text-4xl",
    }),
    h3: responsive({
      xs: "text-lg",
      sm: "text-xl",
      lg: "text-2xl",
      xl: "text-3xl",
    }),
    body: responsive({
      xs: "text-sm",
      sm: "text-base",
      lg: "text-lg",
    }),
  },
};

// Common responsive patterns as functions
export const createResponsiveGrid = (
  cols: Partial<Record<Breakpoint, number>>,
  gap?: Partial<Record<Breakpoint, number>>
): string => {
  const gridCols = responsive(
    Object.fromEntries(
      Object.entries(cols).map(([bp, value]) => [bp, `grid-cols-${value}`])
    ) as Partial<Record<Breakpoint, string>>
  );

  const gridGap = gap
    ? responsive(
        Object.fromEntries(
          Object.entries(gap).map(([bp, value]) => [bp, `gap-${value}`])
        ) as Partial<Record<Breakpoint, string>>
      )
    : "";

  return cn("grid", gridCols, gridGap);
};

export const createResponsivePadding = (
  padding: Partial<Record<Breakpoint, number>>
): string => {
  return responsive(
    Object.fromEntries(
      Object.entries(padding).map(([bp, value]) => [bp, `p-${value}`])
    ) as Partial<Record<Breakpoint, string>>
  );
};

export const createResponsiveMargin = (
  margin: Partial<Record<Breakpoint, number>>
): string => {
  return responsive(
    Object.fromEntries(
      Object.entries(margin).map(([bp, value]) => [bp, `m-${value}`])
    ) as Partial<Record<Breakpoint, string>>
  );
};

// Visibility utilities
export const hideOn = (breakpoints: Breakpoint[]): string => {
  return breakpoints
    .map(bp => (bp === "xs" ? "hidden" : `${bp}:hidden`))
    .join(" ");
};

export const showOn = (breakpoints: Breakpoint[]): string => {
  return breakpoints
    .map(bp => (bp === "xs" ? "block" : `${bp}:block`))
    .join(" ");
};

// Flex direction utilities
export const responsiveFlex = (
  directions: Partial<
    Record<Breakpoint, "row" | "col" | "row-reverse" | "col-reverse">
  >
): string => {
  return responsive(
    Object.fromEntries(
      Object.entries(directions).map(([bp, direction]) => [
        bp,
        direction === "row"
          ? "flex-row"
          : direction === "col"
            ? "flex-col"
            : direction === "row-reverse"
              ? "flex-row-reverse"
              : "flex-col-reverse",
      ])
    ) as Partial<Record<Breakpoint, string>>
  );
};

export default {
  cn,
  responsive,
  responsiveGridUtils,
  createResponsiveGrid,
  createResponsivePadding,
  createResponsiveMargin,
  hideOn,
  showOn,
  responsiveFlex,
};
