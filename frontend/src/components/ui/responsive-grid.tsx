import React from "react";
import { cn } from "@/lib/utils";

interface ResponsiveGridProps {
  children: React.ReactNode;
  className?: string | undefined;
  // Column counts for different breakpoints
  cols?: {
    xs?: number;
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
    "2xl"?: number;
  };
  // Gap sizes for different breakpoints
  gap?: {
    xs?: number;
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
    "2xl"?: number;
  };
  // Auto-fit columns with minimum width
  autoFit?: {
    minWidth: string; // e.g., "250px", "20rem"
    maxCols?: number; // Maximum number of columns
  };
}

export function ResponsiveGrid({
  children,
  className,
  cols = { xs: 1, sm: 2, md: 3, lg: 4, xl: 4, "2xl": 5 },
  gap = { xs: 4, sm: 4, md: 6, lg: 6, xl: 8, "2xl": 8 },
  autoFit,
}: ResponsiveGridProps) {
  // Generate column classes
  const generateColumnClasses = () => {
    const classes: string[] = [];

    if (autoFit) {
      classes.push(
        `grid-cols-[repeat(auto-fit,minmax(${autoFit.minWidth},1fr))]`
      );
      if (autoFit.maxCols) {
        classes.push(`max-grid-cols-${autoFit.maxCols}`);
      }
    } else {
      // Default to mobile-first approach
      if (cols.xs) classes.push(`grid-cols-${cols.xs}`);
      if (cols.sm) classes.push(`sm:grid-cols-${cols.sm}`);
      if (cols.md) classes.push(`md:grid-cols-${cols.md}`);
      if (cols.lg) classes.push(`lg:grid-cols-${cols.lg}`);
      if (cols.xl) classes.push(`xl:grid-cols-${cols.xl}`);
      if (cols["2xl"]) classes.push(`2xl:grid-cols-${cols["2xl"]}`);
    }

    return classes.join(" ");
  };

  // Generate gap classes
  const generateGapClasses = () => {
    const classes: string[] = [];

    if (gap.xs) classes.push(`gap-${gap.xs}`);
    if (gap.sm) classes.push(`sm:gap-${gap.sm}`);
    if (gap.md) classes.push(`md:gap-${gap.md}`);
    if (gap.lg) classes.push(`lg:gap-${gap.lg}`);
    if (gap.xl) classes.push(`xl:gap-${gap.xl}`);
    if (gap["2xl"]) classes.push(`2xl:gap-${gap["2xl"]}`);

    return classes.join(" ");
  };

  const gridClasses = cn(
    "grid",
    generateColumnClasses(),
    generateGapClasses(),
    className
  );

  return <div className={gridClasses}>{children}</div>;
}

// Predefined grid layouts
export const ProductGrid = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string | undefined;
}) => (
  <ResponsiveGrid
    cols={{ xs: 1, sm: 2, md: 2, lg: 3, xl: 4, "2xl": 5 }}
    gap={{ xs: 4, sm: 4, md: 6, lg: 6, xl: 6, "2xl": 8 }}
    className={className}
  >
    {children}
  </ResponsiveGrid>
);

export const CategoryGrid = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string | undefined;
}) => (
  <ResponsiveGrid
    cols={{ xs: 2, sm: 3, md: 4, lg: 6, xl: 8, "2xl": 10 }}
    gap={{ xs: 3, sm: 4, md: 4, lg: 6, xl: 6, "2xl": 6 }}
    className={className}
  >
    {children}
  </ResponsiveGrid>
);

export const FeatureGrid = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string | undefined;
}) => (
  <ResponsiveGrid
    cols={{ xs: 1, sm: 1, md: 2, lg: 3, xl: 3, "2xl": 3 }}
    gap={{ xs: 6, sm: 6, md: 8, lg: 8, xl: 10, "2xl": 12 }}
    className={className}
  >
    {children}
  </ResponsiveGrid>
);

export const BlogGrid = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string | undefined;
}) => (
  <ResponsiveGrid
    cols={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 3, "2xl": 3 }}
    gap={{ xs: 6, sm: 6, md: 6, lg: 8, xl: 8, "2xl": 10 }}
    className={className}
  >
    {children}
  </ResponsiveGrid>
);

// Container component with responsive padding
interface ResponsiveContainerProps {
  children: React.ReactNode;
  className?: string | undefined;
  size?: "sm" | "md" | "lg" | "xl" | "2xl" | "full";
  padding?: {
    xs?: number;
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
    "2xl"?: number;
  };
}

export function ResponsiveContainer({
  children,
  className,
  size = "full",
  padding = { xs: 4, sm: 6, md: 8, lg: 8, xl: 12, "2xl": 16 },
}: ResponsiveContainerProps) {
  const sizeClasses = {
    sm: "max-w-screen-sm",
    md: "max-w-screen-md",
    lg: "max-w-screen-lg",
    xl: "max-w-screen-xl",
    "2xl": "max-w-screen-2xl",
    full: "max-w-full",
  };

  const generatePaddingClasses = () => {
    const classes: string[] = [];

    if (padding.xs) classes.push(`px-${padding.xs}`);
    if (padding.sm) classes.push(`sm:px-${padding.sm}`);
    if (padding.md) classes.push(`md:px-${padding.md}`);
    if (padding.lg) classes.push(`lg:px-${padding.lg}`);
    if (padding.xl) classes.push(`xl:px-${padding.xl}`);
    if (padding["2xl"]) classes.push(`2xl:px-${padding["2xl"]}`);

    return classes.join(" ");
  };

  return (
    <div
      className={cn(
        "mx-auto",
        sizeClasses[size],
        generatePaddingClasses(),
        className
      )}
    >
      {children}
    </div>
  );
}

// Responsive text component
interface ResponsiveTextProps {
  children: React.ReactNode;
  as?: "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "p" | "span";
  className?: string | undefined;
  size?: {
    xs?: string;
    sm?: string;
    md?: string;
    lg?: string;
    xl?: string;
    "2xl"?: string;
  };
}

export function ResponsiveText({
  children,
  as: Component = "p",
  className,
  size = { xs: "text-base", sm: "sm:text-lg", md: "md:text-xl" },
}: ResponsiveTextProps) {
  const generateTextClasses = () => {
    const classes: string[] = [];

    if (size.xs) classes.push(size.xs);
    if (size.sm) classes.push(size.sm);
    if (size.md) classes.push(size.md);
    if (size.lg) classes.push(size.lg);
    if (size.xl) classes.push(size.xl);
    if (size["2xl"]) classes.push(size["2xl"]);

    return classes.join(" ");
  };

  return (
    <Component className={cn(generateTextClasses(), className)}>
      {children}
    </Component>
  );
}
