"use client";

import { useState, useEffect } from "react";
import {
  type Breakpoint,
  mediaQueries,
  deviceTypes,
  getCurrentBreakpoint,
} from "@/config/breakpoints";

// Hook to get current breakpoint
export function useBreakpoint(): Breakpoint {
  const [breakpoint, setBreakpoint] = useState<Breakpoint>("sm");

  useEffect(() => {
    const updateBreakpoint = () => {
      setBreakpoint(getCurrentBreakpoint());
    };

    // Set initial breakpoint
    updateBreakpoint();

    // Create media query listeners for each breakpoint
    const mediaQueryLists = Object.entries(mediaQueries).map(([bp, query]) => ({
      breakpoint: bp as Breakpoint,
      mql: window.matchMedia(query),
    }));

    // Add listeners
    mediaQueryLists.forEach(({ mql }) => {
      mql.addEventListener("change", updateBreakpoint);
    });

    // Cleanup listeners
    return () => {
      mediaQueryLists.forEach(({ mql }) => {
        mql.removeEventListener("change", updateBreakpoint);
      });
    };
  }, []);

  return breakpoint;
}

// Hook to check if a specific breakpoint is active
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState<boolean>(false);

  useEffect(() => {
    const mediaQueryList = window.matchMedia(query);

    const updateMatches = () => {
      setMatches(mediaQueryList.matches);
    };

    // Set initial state
    updateMatches();

    // Listen for changes
    mediaQueryList.addEventListener("change", updateMatches);

    return () => {
      mediaQueryList.removeEventListener("change", updateMatches);
    };
  }, [query]);

  return matches;
}

// Hook to check if breakpoint is active or above
export function useBreakpointValue(breakpoint: Breakpoint): boolean {
  return useMediaQuery(mediaQueries[breakpoint]);
}

// Hook to get device type
export function useDeviceType(): "mobile" | "tablet" | "desktop" {
  const isMobile = useMediaQuery(deviceTypes.mobile);
  const isTablet = useMediaQuery(deviceTypes.tablet);
  const isDesktop = useMediaQuery(deviceTypes.desktop);

  if (isMobile) return "mobile";
  if (isTablet) return "tablet";
  if (isDesktop) return "desktop";

  return "mobile"; // fallback
}

// Hook for responsive values
export function useResponsiveValue<T>(
  values: Partial<Record<Breakpoint, T>>
): T | undefined {
  const currentBreakpoint = useBreakpoint();

  // Get the value for current breakpoint or closest smaller one
  const breakpointOrder: Breakpoint[] = ["xs", "sm", "md", "lg", "xl", "2xl"];
  const currentIndex = breakpointOrder.indexOf(currentBreakpoint);

  for (let i = currentIndex; i >= 0; i--) {
    const bp = breakpointOrder[i];
    if (bp && values[bp] !== undefined) {
      return values[bp];
    }
  }

  return undefined;
}

// Hook for window dimensions
export function useWindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: 0,
    height: 0,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Set initial size
    handleResize();

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return windowSize;
}

// Hook to check if screen is smaller than a breakpoint
export function useIsMobile(): boolean {
  return useMediaQuery(deviceTypes.mobile);
}

export function useIsTablet(): boolean {
  return useMediaQuery(deviceTypes.tablet);
}

export function useIsDesktop(): boolean {
  return useMediaQuery(deviceTypes.desktop);
}

// Hook for responsive grid columns
export function useResponsiveColumns(
  mobile: number = 1,
  tablet: number = 2,
  desktop: number = 3,
  wide: number = 4
): number {
  const isMobile = useIsMobile();
  const isTablet = useIsTablet();
  const isDesktop = useIsDesktop();
  const isWide = useBreakpointValue("xl");

  if (isMobile) return mobile;
  if (isTablet) return tablet;
  if (isDesktop && !isWide) return desktop;
  return wide;
}
