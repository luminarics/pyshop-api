import React from "react";
import { cn } from "@/lib/utils";

interface ResponsiveGridProps {
  children: React.ReactNode;
  className?: string | undefined;
  variant?: "product" | "feature" | "category" | "blog" | "custom";
  gap?: "sm" | "md" | "lg";
}

const gridVariants = {
  product: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5",
  feature: "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
  category: "grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6",
  blog: "grid-cols-1 md:grid-cols-2 xl:grid-cols-3",
  custom: "",
};

const gapSizes = {
  sm: "gap-4",
  md: "gap-6",
  lg: "gap-8",
};

export function ResponsiveGrid({
  children,
  className,
  variant = "product",
  gap = "md",
}: ResponsiveGridProps) {
  return (
    <div
      className={cn(
        "grid",
        gridVariants[variant],
        gapSizes[gap],
        className
      )}
    >
      {children}
    </div>
  );
}

// Simplified predefined grid layouts
export const ProductGrid = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => (
  <ResponsiveGrid variant="product" className={className}>
    {children}
  </ResponsiveGrid>
);

export const CategoryGrid = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => (
  <ResponsiveGrid variant="category" gap="sm" className={className}>
    {children}
  </ResponsiveGrid>
);

export const FeatureGrid = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => (
  <ResponsiveGrid variant="feature" gap="lg" className={className}>
    {children}
  </ResponsiveGrid>
);

export const BlogGrid = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => (
  <ResponsiveGrid variant="blog" gap="lg" className={className}>
    {children}
  </ResponsiveGrid>
);

// Container component with responsive padding
interface ResponsiveContainerProps {
  children: React.ReactNode;
  className?: string | undefined;
  size?: "sm" | "md" | "lg" | "xl" | "2xl" | "full";
}

export function ResponsiveContainer({
  children,
  className,
  size = "full",
}: ResponsiveContainerProps) {
  const sizeClasses = {
    sm: "max-w-screen-sm",
    md: "max-w-screen-md",
    lg: "max-w-screen-lg",
    xl: "max-w-screen-xl",
    "2xl": "max-w-screen-2xl",
    full: "max-w-full",
  };

  return (
    <div
      className={cn(
        "mx-auto px-4 sm:px-6 lg:px-8 xl:px-12",
        sizeClasses[size],
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
  variant?: "h1" | "h2" | "h3" | "body" | "large";
}

const textVariants = {
  h1: "text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold",
  h2: "text-xl sm:text-2xl lg:text-3xl xl:text-4xl font-semibold",
  h3: "text-lg sm:text-xl lg:text-2xl font-medium",
  large: "text-lg sm:text-xl",
  body: "text-base",
};

export function ResponsiveText({
  children,
  as: Component = "p",
  className,
  variant = "body",
}: ResponsiveTextProps) {
  return (
    <Component className={cn(textVariants[variant], className)}>
      {children}
    </Component>
  );
}
