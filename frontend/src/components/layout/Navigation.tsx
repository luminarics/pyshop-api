"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { cn } from "@/lib/utils";

const navigationItems = [
  {
    title: "Home",
    href: "/",
    description: "Return to homepage",
  },
  {
    title: "Products",
    href: "/products",
    description: "Browse our product catalog",
    children: [
      {
        title: "Featured Products",
        href: "/products/featured",
        description: "Discover our hand-picked selection of premium items.",
      },
      {
        title: "Electronics",
        href: "/products/electronics",
        description: "Latest gadgets and tech accessories.",
      },
      {
        title: "Clothing",
        href: "/products/clothing",
        description: "Fashion and apparel for every occasion.",
      },
      {
        title: "Home & Garden",
        href: "/products/home-garden",
        description: "Everything for your home and outdoor spaces.",
      },
      {
        title: "Sports & Outdoors",
        href: "/products/sports",
        description: "Gear for active lifestyles and outdoor adventures.",
      },
      {
        title: "Books & Media",
        href: "/products/books",
        description: "Books, movies, music, and digital content.",
      },
    ],
  },
  {
    title: "Categories",
    href: "/categories",
    description: "Browse by product categories",
  },
  {
    title: "Deals",
    href: "/deals",
    description: "Special offers and discounts",
    children: [
      {
        title: "Daily Deals",
        href: "/deals/daily",
        description: "Limited-time offers updated daily.",
      },
      {
        title: "Weekly Specials",
        href: "/deals/weekly",
        description: "Special weekly promotions and discounts.",
      },
      {
        title: "Clearance",
        href: "/deals/clearance",
        description: "End-of-season items at reduced prices.",
      },
      {
        title: "Bundle Offers",
        href: "/deals/bundles",
        description: "Save more when you buy products together.",
      },
    ],
  },
  {
    title: "About",
    href: "/about",
    description: "Learn more about us",
  },
  {
    title: "Contact",
    href: "/contact",
    description: "Get in touch with our team",
  },
];

interface NavigationProps {
  orientation?: "horizontal" | "vertical";
  className?: string;
  showDropdowns?: boolean;
}

export function Navigation({
  orientation = "horizontal",
  className,
  showDropdowns = true,
}: NavigationProps) {
  const pathname = usePathname();

  if (orientation === "vertical") {
    return (
      <nav className={cn("flex flex-col space-y-2", className)}>
        {navigationItems.map(item => {
          const isActive =
            pathname === item.href ||
            (item.children &&
              item.children.some(child => pathname === child.href));

          if (item.children && showDropdowns) {
            return (
              <div key={item.title} className="space-y-2">
                <Link
                  href={item.href}
                  className={cn(
                    "block px-3 py-2 rounded-md text-sm font-medium transition-colors",
                    isActive
                      ? "bg-accent text-accent-foreground"
                      : "text-muted-foreground hover:text-foreground hover:bg-accent/50"
                  )}
                >
                  {item.title}
                </Link>
                <div className="pl-4 space-y-1">
                  {item.children.map(child => (
                    <Link
                      key={child.href}
                      href={child.href}
                      className={cn(
                        "block px-3 py-2 rounded-md text-sm transition-colors",
                        pathname === child.href
                          ? "bg-accent text-accent-foreground font-medium"
                          : "text-muted-foreground hover:text-foreground hover:bg-accent/50"
                      )}
                    >
                      {child.title}
                    </Link>
                  ))}
                </div>
              </div>
            );
          }

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "block px-3 py-2 rounded-md text-sm font-medium transition-colors",
                isActive
                  ? "bg-accent text-accent-foreground"
                  : "text-muted-foreground hover:text-foreground hover:bg-accent/50"
              )}
            >
              {item.title}
            </Link>
          );
        })}
      </nav>
    );
  }

  return (
    <NavigationMenu className={className}>
      <NavigationMenuList>
        {navigationItems.map(item => (
          <NavigationMenuItem key={item.title}>
            {item.children && showDropdowns ? (
              <>
                <NavigationMenuTrigger
                  className={cn(
                    pathname === item.href ||
                      (item.children &&
                        item.children.some(child => pathname === child.href))
                      ? "bg-accent text-accent-foreground"
                      : ""
                  )}
                >
                  {item.title}
                </NavigationMenuTrigger>
                <NavigationMenuContent>
                  <div className="grid gap-3 p-4 md:w-[400px] lg:w-[500px] lg:grid-cols-[.75fr_1fr]">
                    <div className="row-span-3">
                      <NavigationMenuLink asChild>
                        <Link
                          className="flex h-full w-full select-none flex-col justify-end rounded-md bg-gradient-to-b from-muted/50 to-muted p-6 no-underline outline-none focus:shadow-md"
                          href={item.href}
                        >
                          <div className="mb-2 mt-4 text-lg font-medium">
                            {item.title}
                          </div>
                          <p className="text-sm leading-tight text-muted-foreground">
                            {item.description}
                          </p>
                        </Link>
                      </NavigationMenuLink>
                    </div>
                    {item.children.slice(0, 6).map(child => (
                      <NavigationMenuLink asChild key={child.href}>
                        <Link
                          href={child.href}
                          className={cn(
                            "block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
                            pathname === child.href
                              ? "bg-accent text-accent-foreground"
                              : ""
                          )}
                        >
                          <div className="text-sm font-medium leading-none">
                            {child.title}
                          </div>
                          <p className="line-clamp-2 text-sm leading-snug text-muted-foreground">
                            {child.description}
                          </p>
                        </Link>
                      </NavigationMenuLink>
                    ))}
                  </div>
                </NavigationMenuContent>
              </>
            ) : (
              <Link href={item.href} legacyBehavior passHref>
                <NavigationMenuLink
                  className={cn(
                    navigationMenuTriggerStyle(),
                    pathname === item.href
                      ? "bg-accent text-accent-foreground"
                      : ""
                  )}
                >
                  {item.title}
                </NavigationMenuLink>
              </Link>
            )}
          </NavigationMenuItem>
        ))}
      </NavigationMenuList>
    </NavigationMenu>
  );
}
