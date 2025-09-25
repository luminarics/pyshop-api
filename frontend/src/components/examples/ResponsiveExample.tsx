"use client";

import React from "react";
import {
  ProductGrid,
  CategoryGrid,
  FeatureGrid,
  ResponsiveContainer,
  ResponsiveText,
} from "@/components/ui/responsive-grid";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useBreakpoint, useDeviceType, useIsMobile } from "@/hooks";
import {
  responsiveGridUtils,
  createResponsiveGrid,
  hideOn,
  showOn,
} from "@/utils";
import { cn } from "@/lib/utils";

export function ResponsiveExample() {
  const currentBreakpoint = useBreakpoint();
  const deviceType = useDeviceType();
  const isMobile = useIsMobile();

  return (
    <div className="space-y-12">
      {/* Debug Info */}
      <Card>
        <CardHeader>
          <CardTitle>Responsive Debug Info</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            <Badge variant="outline">Breakpoint: {currentBreakpoint}</Badge>
            <Badge variant="outline">Device: {deviceType}</Badge>
            <Badge variant="outline">Mobile: {isMobile ? "Yes" : "No"}</Badge>
          </div>
        </CardContent>
      </Card>

      {/* Responsive Text Examples */}
      <ResponsiveContainer>
        <ResponsiveText
          as="h1"
          size={{
            xs: "text-2xl",
            sm: "text-3xl",
            lg: "text-4xl",
            xl: "text-5xl",
          }}
          className="font-bold text-center mb-4"
        >
          Responsive Typography
        </ResponsiveText>

        <ResponsiveText
          as="p"
          size={{
            xs: "text-sm",
            sm: "text-base",
            lg: "text-lg",
          }}
          className="text-center text-muted-foreground"
        >
          This text adapts to different screen sizes using the responsive
          breakpoint system.
        </ResponsiveText>
      </ResponsiveContainer>

      {/* Product Grid Example */}
      <ResponsiveContainer>
        <h2 className="text-2xl font-bold mb-6">Product Grid (Responsive)</h2>
        <ProductGrid>
          {Array.from({ length: 10 }, (_, i) => (
            <Card key={i} className="overflow-hidden">
              <div className="aspect-square bg-muted"></div>
              <CardContent className="p-4">
                <h3 className="font-semibold">Product {i + 1}</h3>
                <p className="text-sm text-muted-foreground">$99.99</p>
                <Button size="sm" className="w-full mt-2">
                  Add to Cart
                </Button>
              </CardContent>
            </Card>
          ))}
        </ProductGrid>
      </ResponsiveContainer>

      {/* Category Grid Example */}
      <ResponsiveContainer>
        <h2 className="text-2xl font-bold mb-6">Category Grid</h2>
        <CategoryGrid>
          {Array.from({ length: 12 }, (_, i) => (
            <Card
              key={i}
              className="text-center p-4 hover:shadow-lg transition-shadow"
            >
              <div className="w-12 h-12 bg-primary rounded-lg mx-auto mb-2"></div>
              <p className="text-sm font-medium">Category {i + 1}</p>
            </Card>
          ))}
        </CategoryGrid>
      </ResponsiveContainer>

      {/* Feature Grid Example */}
      <ResponsiveContainer>
        <h2 className="text-2xl font-bold mb-6">Feature Grid</h2>
        <FeatureGrid>
          {Array.from({ length: 3 }, (_, i) => (
            <Card key={i}>
              <CardHeader>
                <CardTitle>Feature {i + 1}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  This is a detailed description of feature {i + 1} that
                  showcases how our responsive grid system adapts to different
                  screen sizes.
                </p>
              </CardContent>
            </Card>
          ))}
        </FeatureGrid>
      </ResponsiveContainer>

      {/* Custom Responsive Grid */}
      <ResponsiveContainer>
        <h2 className="text-2xl font-bold mb-6">Custom Responsive Grid</h2>
        <div
          className={createResponsiveGrid(
            { xs: 1, sm: 2, md: 3, lg: 4, xl: 5 },
            { xs: 4, sm: 4, md: 6, lg: 6, xl: 8 }
          )}
        >
          {Array.from({ length: 8 }, (_, i) => (
            <Card key={i} className="p-4">
              <div className="aspect-video bg-gradient-to-br from-primary/20 to-primary/5 rounded mb-3"></div>
              <h3 className="font-semibold text-sm">Item {i + 1}</h3>
            </Card>
          ))}
        </div>
      </ResponsiveContainer>

      {/* Responsive Visibility */}
      <ResponsiveContainer>
        <h2 className="text-2xl font-bold mb-6">Responsive Visibility</h2>
        <div className="space-y-4">
          <Card className={cn("p-4", hideOn(["lg", "xl", "2xl"]))}>
            <p className="text-center">
              📱 This card is only visible on mobile and tablet (hidden on lg
              and above)
            </p>
          </Card>

          <Card className={cn("p-4", showOn(["lg", "xl", "2xl"]), "hidden")}>
            <p className="text-center">
              🖥️ This card is only visible on desktop (lg and above)
            </p>
          </Card>

          <div className="flex justify-center space-x-4">
            <Badge className={cn(hideOn(["md", "lg", "xl", "2xl"]))}>
              Mobile Only
            </Badge>
            <Badge className={cn("hidden", showOn(["md"]))} variant="secondary">
              Tablet+
            </Badge>
            <Badge className={cn("hidden", showOn(["lg"]))} variant="outline">
              Desktop+
            </Badge>
          </div>
        </div>
      </ResponsiveContainer>

      {/* Responsive Layout Patterns */}
      <ResponsiveContainer>
        <h2 className="text-2xl font-bold mb-6">Responsive Layout Patterns</h2>

        {/* Sidebar Layout */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Sidebar Layout</h3>
          <div className="flex flex-col lg:flex-row gap-6">
            <aside className="w-full lg:w-64 bg-muted/30 p-4 rounded">
              <h4 className="font-medium mb-2">Sidebar</h4>
              <p className="text-sm text-muted-foreground">
                This sidebar stacks vertically on mobile and sits alongside
                content on desktop.
              </p>
            </aside>
            <main className="flex-1 bg-muted/10 p-4 rounded">
              <h4 className="font-medium mb-2">Main Content</h4>
              <p className="text-sm text-muted-foreground">
                The main content area takes full width on mobile and shares
                space with the sidebar on desktop.
              </p>
            </main>
          </div>
        </Card>

        {/* Card Stack */}
        <Card className="p-6 mt-6">
          <h3 className="text-lg font-semibold mb-4">Responsive Card Stack</h3>
          <div
            className={cn(
              responsiveGridUtils.featureGrid,
              responsiveGridUtils.gap.medium
            )}
          >
            <Card className="p-4">
              <h4 className="font-medium">Card 1</h4>
              <p className="text-sm text-muted-foreground mt-2">
                Cards stack vertically on mobile and arrange in a grid on larger
                screens.
              </p>
            </Card>
            <Card className="p-4">
              <h4 className="font-medium">Card 2</h4>
              <p className="text-sm text-muted-foreground mt-2">
                The layout automatically adapts based on available screen space.
              </p>
            </Card>
            <Card className="p-4">
              <h4 className="font-medium">Card 3</h4>
              <p className="text-sm text-muted-foreground mt-2">
                Perfect for showcasing features, testimonials, or product
                highlights.
              </p>
            </Card>
          </div>
        </Card>
      </ResponsiveContainer>
    </div>
  );
}
