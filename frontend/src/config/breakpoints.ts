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

// Common responsive patterns
export const responsivePatterns = {
  // Grid columns
  gridCols: {
    mobile: "grid-cols-1",
    tablet: "md:grid-cols-2",
    desktop: "lg:grid-cols-3",
    wide: "xl:grid-cols-4",
  },

  // Product grid
  productGrid: {
    mobile: "grid-cols-1",
    tablet: "sm:grid-cols-2",
    desktop: "lg:grid-cols-3",
    wide: "xl:grid-cols-4",
    ultraWide: "2xl:grid-cols-5",
  },

  // Container sizes
  container: {
    mobile: "px-4",
    tablet: "sm:px-6",
    desktop: "lg:px-8",
    wide: "xl:px-12",
    ultraWide: "2xl:px-16",
  },

  // Text sizes
  headings: {
    h1: {
      mobile: "text-2xl",
      tablet: "sm:text-3xl",
      desktop: "lg:text-4xl",
      wide: "xl:text-5xl",
    },
    h2: {
      mobile: "text-xl",
      tablet: "sm:text-2xl",
      desktop: "lg:text-3xl",
      wide: "xl:text-4xl",
    },
    h3: {
      mobile: "text-lg",
      tablet: "sm:text-xl",
      desktop: "lg:text-2xl",
      wide: "xl:text-3xl",
    },
  },

  // Navigation
  nav: {
    mobile: "flex-col space-y-2",
    desktop: "lg:flex-row lg:space-y-0 lg:space-x-6",
  },

  // Sidebar
  sidebar: {
    mobile: "w-full",
    tablet: "sm:w-64",
    desktop: "lg:w-72",
    wide: "xl:w-80",
  },

  // Cards
  card: {
    mobile: "p-4",
    tablet: "sm:p-6",
    desktop: "lg:p-8",
  },

  // Images
  image: {
    mobile: "w-full h-48",
    tablet: "sm:h-56",
    desktop: "md:h-64",
    wide: "lg:h-72",
  },
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
