// API Configuration
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const API_ENDPOINTS = {
  // Auth endpoints
  LOGIN: "/auth/jwt/login",
  REGISTER: "/auth/register",
  LOGOUT: "/auth/jwt/logout",
  ME: "/users/me",

  // Product endpoints
  PRODUCTS: "/products",
  PRODUCT_BY_ID: (id: number) => `/products/${id}`,

  // Cart endpoints
  CART: "/cart",
  CART_ITEMS: "/cart/items",
  CART_ITEM_BY_ID: (id: string) => `/cart/items/${id}`,
} as const;

// App Configuration
export const APP_CONFIG = {
  NAME: "PyShop",
  DESCRIPTION: "E-commerce platform built with Next.js and FastAPI",
  VERSION: "1.0.0",
} as const;

// UI Constants
export const ROUTES = {
  HOME: "/",
  LOGIN: "/auth/login",
  REGISTER: "/auth/register",
  DASHBOARD: "/dashboard",
  PRODUCTS: "/products",
  CART: "/cart",
  CHECKOUT: "/checkout",
  PROFILE: "/profile",
  SETTINGS: "/settings",
} as const;

export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_LIMIT: 10,
  MAX_LIMIT: 100,
} as const;
