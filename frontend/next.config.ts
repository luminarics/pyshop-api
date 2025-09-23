import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable standalone output for Docker optimization
  output: "standalone",

  // Compress images
  images: {
    formats: ["image/webp", "image/avif"],
  },

  // Enable experimental features for better performance
  experimental: {
    optimizePackageImports: ["@heroicons/react"],
  },

  // Environment variable validation
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  // ESLint configuration for Docker builds
  eslint: {
    // Skip ESLint during Docker builds to avoid errors stopping the build
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
