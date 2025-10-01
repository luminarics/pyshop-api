import React from "react";
import { cn } from "@/lib/utils";

interface LoadingSpinnerProps {
  className?: string | undefined;
  size?: "sm" | "md" | "lg" | "xl";
}

const sizeClasses = {
  sm: "w-4 h-4",
  md: "w-6 h-6",
  lg: "w-8 h-8",
  xl: "w-12 h-12",
};

export function LoadingSpinner({ className, size = "md" }: LoadingSpinnerProps) {
  return (
    <div
      className={cn(
        "inline-block animate-spin rounded-full border-2 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]",
        sizeClasses[size],
        className
      )}
      role="status"
      aria-label="Loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}

interface LoadingDotsProps {
  className?: string | undefined;
  size?: "sm" | "md" | "lg";
}

export function LoadingDots({ className, size = "md" }: LoadingDotsProps) {
  const dotSize = {
    sm: "w-1 h-1",
    md: "w-2 h-2",
    lg: "w-3 h-3",
  };

  return (
    <div className={cn("flex space-x-1", className)} role="status" aria-label="Loading">
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className={cn(
            "bg-current rounded-full animate-pulse",
            dotSize[size]
          )}
          style={{
            animationDelay: `${i * 0.15}s`,
            animationDuration: "1s",
          }}
        />
      ))}
      <span className="sr-only">Loading...</span>
    </div>
  );
}

interface LoadingSkeletonProps {
  className?: string | undefined;
  variant?: "text" | "rectangle" | "circle" | "card";
  lines?: number;
}

export function LoadingSkeleton({
  className,
  variant = "text",
  lines = 1,
}: LoadingSkeletonProps) {
  const variantClasses = {
    text: "h-4 rounded",
    rectangle: "h-32 rounded-md",
    circle: "rounded-full aspect-square",
    card: "h-48 rounded-lg",
  };

  if (variant === "text" && lines > 1) {
    return (
      <div className={cn("space-y-2", className)}>
        {Array.from({ length: lines }).map((_, i) => (
          <div
            key={i}
            className={cn(
              "bg-muted animate-pulse",
              variantClasses.text,
              i === lines - 1 && "w-3/4"
            )}
          />
        ))}
      </div>
    );
  }

  return (
    <div
      className={cn(
        "bg-muted animate-pulse",
        variantClasses[variant],
        className
      )}
      role="status"
      aria-label="Loading content"
    />
  );
}

interface LoadingStateProps {
  children?: React.ReactNode;
  className?: string | undefined;
  variant?: "spinner" | "dots" | "skeleton";
  size?: "sm" | "md" | "lg";
  text?: string;
}

export function LoadingState({
  children,
  className,
  variant = "spinner",
  size = "md",
  text = "Loading...",
}: LoadingStateProps) {
  const renderLoader = () => {
    switch (variant) {
      case "dots":
        return <LoadingDots size={size} />;
      case "skeleton":
        return <LoadingSkeleton />;
      default:
        return <LoadingSpinner size={size} />;
    }
  };

  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center space-y-4 p-8",
        className
      )}
      role="status"
      aria-label={text}
    >
      {renderLoader()}
      {text && (
        <p className="text-sm text-muted-foreground font-medium">{text}</p>
      )}
      {children}
    </div>
  );
}

interface LoadingOverlayProps {
  isVisible: boolean;
  children?: React.ReactNode;
  className?: string | undefined;
  variant?: "spinner" | "dots";
  text?: string;
}

export function LoadingOverlay({
  isVisible,
  children,
  className,
  variant = "spinner",
  text = "Loading...",
}: LoadingOverlayProps) {
  if (!isVisible) return null;

  return (
    <div
      className={cn(
        "fixed inset-0 z-50 bg-background/80 backdrop-blur-sm",
        className
      )}
    >
      <LoadingState variant={variant} text={text} className="h-full">
        {children}
      </LoadingState>
    </div>
  );
}

interface LoadingButtonProps {
  isLoading: boolean;
  children: React.ReactNode;
  className?: string | undefined;
  disabled?: boolean;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
}

export function LoadingButton({
  isLoading,
  children,
  className,
  disabled,
  onClick,
  type = "button",
}: LoadingButtonProps) {
  return (
    <button
      type={type}
      disabled={disabled || isLoading}
      onClick={onClick}
      className={cn(
        "inline-flex items-center justify-center space-x-2 px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors",
        className
      )}
    >
      {isLoading && <LoadingSpinner size="sm" />}
      <span>{children}</span>
    </button>
  );
}

interface LoadingCardProps {
  className?: string | undefined;
  lines?: number;
  showImage?: boolean;
  showButton?: boolean;
}

export function LoadingCard({
  className,
  lines = 3,
  showImage = true,
  showButton = false,
}: LoadingCardProps) {
  return (
    <div className={cn("p-6 border rounded-lg space-y-4", className)}>
      {showImage && <LoadingSkeleton variant="rectangle" className="h-48" />}
      <LoadingSkeleton variant="text" lines={lines} />
      {showButton && <LoadingSkeleton className="h-10 w-24" />}
    </div>
  );
}