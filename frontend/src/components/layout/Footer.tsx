import React from "react";
import Link from "next/link";
import {
  FacebookIcon,
  TwitterIcon,
  InstagramIcon,
  LinkedinIcon,
  MailIcon,
  PhoneIcon,
  MapPinIcon,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";

export function Footer() {
  return (
    <footer className="bg-muted/50 border-t">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
          {/* Company Info */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-sm">
                  PS
                </span>
              </div>
              <span className="font-bold text-xl">PyShop</span>
            </div>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Your trusted e-commerce platform offering quality products at
              competitive prices. Shop with confidence and enjoy fast, reliable
              delivery.
            </p>
            <div className="flex space-x-2">
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <FacebookIcon className="h-4 w-4" />
                <span className="sr-only">Facebook</span>
              </Button>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <TwitterIcon className="h-4 w-4" />
                <span className="sr-only">Twitter</span>
              </Button>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <InstagramIcon className="h-4 w-4" />
                <span className="sr-only">Instagram</span>
              </Button>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <LinkedinIcon className="h-4 w-4" />
                <span className="sr-only">LinkedIn</span>
              </Button>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="font-semibold text-sm uppercase tracking-wider">
              Quick Links
            </h3>
            <nav className="flex flex-col space-y-2">
              <Link
                href="/about"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                About Us
              </Link>
              <Link
                href="/contact"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Contact
              </Link>
              <Link
                href="/careers"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Careers
              </Link>
              <Link
                href="/blog"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Blog
              </Link>
              <Link
                href="/press"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Press
              </Link>
            </nav>
          </div>

          {/* Customer Service */}
          <div className="space-y-4">
            <h3 className="font-semibold text-sm uppercase tracking-wider">
              Customer Service
            </h3>
            <nav className="flex flex-col space-y-2">
              <Link
                href="/help"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Help Center
              </Link>
              <Link
                href="/shipping"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Shipping Info
              </Link>
              <Link
                href="/returns"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Returns
              </Link>
              <Link
                href="/track"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Track Order
              </Link>
              <Link
                href="/size-guide"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Size Guide
              </Link>
            </nav>
          </div>

          {/* Newsletter & Contact */}
          <div className="space-y-4">
            <h3 className="font-semibold text-sm uppercase tracking-wider">
              Stay Connected
            </h3>
            <p className="text-sm text-muted-foreground">
              Subscribe to our newsletter for the latest updates and exclusive
              offers.
            </p>
            <form className="flex space-x-2">
              <Input
                type="email"
                placeholder="Enter your email"
                className="flex-1"
              />
              <Button type="submit" size="sm">
                Subscribe
              </Button>
            </form>

            <div className="space-y-2 pt-2">
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <MailIcon className="h-4 w-4" />
                <span>support@pyshop.com</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <PhoneIcon className="h-4 w-4" />
                <span>+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <MapPinIcon className="h-4 w-4" />
                <span>123 Commerce St, City, State 12345</span>
              </div>
            </div>
          </div>
        </div>

        <Separator className="my-8" />

        {/* Bottom Section */}
        <div className="flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
          <div className="flex flex-col lg:flex-row items-center space-y-2 lg:space-y-0 lg:space-x-6 text-sm text-muted-foreground">
            <span>© 2024 PyShop. All rights reserved.</span>
            <div className="flex space-x-4">
              <Link
                href="/privacy"
                className="hover:text-foreground transition-colors"
              >
                Privacy Policy
              </Link>
              <Link
                href="/terms"
                className="hover:text-foreground transition-colors"
              >
                Terms of Service
              </Link>
              <Link
                href="/cookies"
                className="hover:text-foreground transition-colors"
              >
                Cookie Policy
              </Link>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-sm text-muted-foreground">We accept:</span>
            <div className="flex space-x-2">
              <div className="h-6 w-10 bg-muted rounded border flex items-center justify-center">
                <span className="text-xs font-bold">VISA</span>
              </div>
              <div className="h-6 w-10 bg-muted rounded border flex items-center justify-center">
                <span className="text-xs font-bold">MC</span>
              </div>
              <div className="h-6 w-10 bg-muted rounded border flex items-center justify-center">
                <span className="text-xs font-bold">AMEX</span>
              </div>
              <div className="h-6 w-10 bg-muted rounded border flex items-center justify-center">
                <span className="text-xs font-bold">PP</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
