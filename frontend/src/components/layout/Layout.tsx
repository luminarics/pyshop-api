import React from "react";
import { Header } from "./Header";
import { Footer } from "./Footer";
import { cn } from "@/lib/utils";

interface LayoutProps {
  children: React.ReactNode;
  className?: string;
  hideHeader?: boolean;
  hideFooter?: boolean;
  maxWidth?: "sm" | "md" | "lg" | "xl" | "2xl" | "full";
}

export function Layout({
  children,
  className,
  hideHeader = false,
  hideFooter = false,
  maxWidth = "full",
}: LayoutProps) {
  const containerClasses = {
    sm: "max-w-screen-sm",
    md: "max-w-screen-md",
    lg: "max-w-screen-lg",
    xl: "max-w-screen-xl",
    "2xl": "max-w-screen-2xl",
    full: "max-w-full",
  };

  return (
    <div className="min-h-screen flex flex-col">
      {!hideHeader && <Header />}

      <main className={cn("flex-1", className)}>
        <div
          className={cn(
            "mx-auto px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16",
            maxWidth !== "full" && containerClasses[maxWidth]
          )}
        >
          {children}
        </div>
      </main>

      {!hideFooter && <Footer />}
    </div>
  );
}

export default Layout;
