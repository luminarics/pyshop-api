// Responsive breakpoints configuration
export const breakpoints = {
  xs: 475, // Extra small devices (small phones)
  sm: 640, // Small devices (phones)
  md: 768, // Medium devices (tablets)
  lg: 1024, // Large devices (desktops)
  xl: 1280, // Extra large devices (large desktops)
  "2xl": 1536, // 2X large devices (larger desktops)
} as const;

export type Breakpoint = keyof typeof breakpoints;

// Simple responsive patterns - use Tailwind classes directly
export const commonPatterns = {
  // Common grid patterns (use directly in components)
  productGrid: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5",
  featureGrid: "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
  categoryGrid: "grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6",

  // Common spacing patterns
  containerPadding: "px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16",
  sectionPadding: "py-8 sm:py-12 lg:py-16 xl:py-20",

  // Common text patterns
  headingLarge: "text-2xl sm:text-3xl lg:text-4xl xl:text-5xl",
  headingMedium: "text-xl sm:text-2xl lg:text-3xl xl:text-4xl",
  headingSmall: "text-lg sm:text-xl lg:text-2xl",
} as const;

// Media query strings for JavaScript
export const mediaQueries = {
  xs: `(min-width: ${breakpoints.xs}px)`,
  sm: `(min-width: ${breakpoints.sm}px)`,
  md: `(min-width: ${breakpoints.md}px)`,
  lg: `(min-width: ${breakpoints.lg}px)`,
  xl: `(min-width: ${breakpoints.xl}px)`,
  "2xl": `(min-width: ${breakpoints["2xl"]}px)`,
} as const;

// Device type detection based on breakpoints
export const deviceTypes = {
  mobile: `(max-width: ${breakpoints.md - 1}px)`,
  tablet: `(min-width: ${breakpoints.md}px) and (max-width: ${breakpoints.lg - 1}px)`,
  desktop: `(min-width: ${breakpoints.lg}px)`,
} as const;

// Utility functions
export const getBreakpointValue = (breakpoint: Breakpoint): number => {
  return breakpoints[breakpoint];
};

export const isBreakpointActive = (breakpoint: Breakpoint): boolean => {
  if (typeof window === "undefined") return false;
  return window.matchMedia(mediaQueries[breakpoint]).matches;
};

export const getCurrentBreakpoint = (): Breakpoint => {
  if (typeof window === "undefined") return "sm";

  if (window.matchMedia(mediaQueries["2xl"]).matches) return "2xl";
  if (window.matchMedia(mediaQueries.xl).matches) return "xl";
  if (window.matchMedia(mediaQueries.lg).matches) return "lg";
  if (window.matchMedia(mediaQueries.md).matches) return "md";
  if (window.matchMedia(mediaQueries.sm).matches) return "sm";
  return "xs";
};
