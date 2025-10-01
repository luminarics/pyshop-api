import React from "react";
import { cn } from "@/lib/utils";
import { AlertTriangle, RefreshCw, XCircle, Wifi, Server } from "lucide-react";
import { Button } from "./button";

interface ErrorMessageProps {
  className?: string | undefined;
  variant?: "destructive" | "warning" | "info";
  children: React.ReactNode;
}

export function ErrorMessage({
  className,
  variant = "destructive",
  children,
}: ErrorMessageProps) {
  const variantClasses = {
    destructive: "text-destructive border-destructive/20 bg-destructive/10",
    warning: "text-yellow-600 border-yellow-200 bg-yellow-50 dark:text-yellow-400 dark:border-yellow-800 dark:bg-yellow-900/20",
    info: "text-blue-600 border-blue-200 bg-blue-50 dark:text-blue-400 dark:border-blue-800 dark:bg-blue-900/20",
  };

  return (
    <div
      className={cn(
        "rounded-md border p-4 text-sm",
        variantClasses[variant],
        className
      )}
      role="alert"
    >
      {children}
    </div>
  );
}

interface ErrorStateProps {
  title?: string;
  message?: string;
  children?: React.ReactNode;
  className?: string | undefined;
  variant?: "error" | "warning" | "network" | "server" | "not-found";
  onRetry?: (() => void) | undefined;
  retryText?: string;
  showRetry?: boolean;
}

export function ErrorState({
  title,
  message,
  children,
  className,
  variant = "error",
  onRetry,
  retryText = "Try again",
  showRetry = true,
}: ErrorStateProps) {
  const getIcon = () => {
    switch (variant) {
      case "warning":
        return <AlertTriangle className="w-12 h-12 text-yellow-500" />;
      case "network":
        return <Wifi className="w-12 h-12 text-red-500" />;
      case "server":
        return <Server className="w-12 h-12 text-red-500" />;
      case "not-found":
        return <XCircle className="w-12 h-12 text-gray-500" />;
      default:
        return <XCircle className="w-12 h-12 text-red-500" />;
    }
  };

  const getDefaultContent = () => {
    switch (variant) {
      case "network":
        return {
          title: title || "Network Error",
          message: message || "Please check your internet connection and try again.",
        };
      case "server":
        return {
          title: title || "Server Error",
          message: message || "Something went wrong on our end. Please try again later.",
        };
      case "not-found":
        return {
          title: title || "Not Found",
          message: message || "The page or resource you're looking for doesn't exist.",
        };
      case "warning":
        return {
          title: title || "Warning",
          message: message || "Please review the information and try again.",
        };
      default:
        return {
          title: title || "Something went wrong",
          message: message || "An unexpected error occurred. Please try again.",
        };
    }
  };

  const content = getDefaultContent();

  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center text-center space-y-4 p-8",
        className
      )}
      role="alert"
    >
      {getIcon()}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold text-foreground">{content.title}</h3>
        <p className="text-sm text-muted-foreground max-w-md">{content.message}</p>
      </div>
      {children}
      {showRetry && onRetry && (
        <Button
          onClick={onRetry}
          variant="outline"
          className="mt-4"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          {retryText}
        </Button>
      )}
    </div>
  );
}

interface ErrorBoundaryFallbackProps {
  error: Error;
  resetError: () => void;
  className?: string | undefined;
}

export function ErrorBoundaryFallback({
  error,
  resetError,
  className,
}: ErrorBoundaryFallbackProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center min-h-[400px] space-y-4 p-8",
        className
      )}
      role="alert"
    >
      <XCircle className="w-16 h-16 text-red-500" />
      <div className="text-center space-y-2">
        <h2 className="text-xl font-semibold text-foreground">
          Oops! Something went wrong
        </h2>
        <p className="text-sm text-muted-foreground">
          An unexpected error occurred. Please try refreshing the page.
        </p>
        {process.env.NODE_ENV === "development" && (
          <details className="mt-4 text-left">
            <summary className="cursor-pointer text-sm font-medium">
              Error details (development only)
            </summary>
            <pre className="mt-2 p-4 bg-muted rounded text-xs overflow-auto max-w-md">
              {error.stack}
            </pre>
          </details>
        )}
      </div>
      <Button onClick={resetError} variant="outline">
        <RefreshCw className="w-4 h-4 mr-2" />
        Try again
      </Button>
    </div>
  );
}

interface ErrorCardProps {
  title?: string;
  message?: string;
  className?: string | undefined;
  onDismiss?: () => void;
  dismissible?: boolean;
}

export function ErrorCard({
  title = "Error",
  message = "Something went wrong",
  className,
  onDismiss,
  dismissible = false,
}: ErrorCardProps) {
  return (
    <div
      className={cn(
        "border border-red-200 bg-red-50 p-4 rounded-lg dark:border-red-800 dark:bg-red-900/20",
        className
      )}
      role="alert"
    >
      <div className="flex items-start">
        <XCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
        <div className="ml-3 flex-1">
          <h4 className="text-sm font-medium text-red-800 dark:text-red-200">
            {title}
          </h4>
          <p className="mt-1 text-sm text-red-700 dark:text-red-300">
            {message}
          </p>
        </div>
        {dismissible && onDismiss && (
          <button
            onClick={onDismiss}
            className="ml-auto pl-3 text-red-400 hover:text-red-600 dark:text-red-300 dark:hover:text-red-100"
          >
            <XCircle className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
}

interface FormErrorProps {
  error?: string;
  className?: string | undefined;
}

export function FormError({ error, className }: FormErrorProps) {
  if (!error) return null;

  return (
    <p
      className={cn("text-sm text-red-600 dark:text-red-400", className)}
      role="alert"
    >
      {error}
    </p>
  );
}

interface ErrorAlertProps {
  title?: string;
  message: string;
  variant?: "destructive" | "warning";
  className?: string | undefined;
  onClose?: () => void;
}

export function ErrorAlert({
  title,
  message,
  variant = "destructive",
  className,
  onClose,
}: ErrorAlertProps) {
  const variantClasses = {
    destructive: "border-red-200 bg-red-50 text-red-800 dark:border-red-800 dark:bg-red-900/20 dark:text-red-200",
    warning: "border-yellow-200 bg-yellow-50 text-yellow-800 dark:border-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-200",
  };

  const Icon = variant === "warning" ? AlertTriangle : XCircle;

  return (
    <div
      className={cn(
        "relative rounded-lg border p-4",
        variantClasses[variant],
        className
      )}
      role="alert"
    >
      <div className="flex items-start">
        <Icon className="w-5 h-5 mt-0.5 flex-shrink-0" />
        <div className="ml-3">
          {title && (
            <h5 className="mb-1 font-medium leading-none tracking-tight">
              {title}
            </h5>
          )}
          <p className="text-sm">{message}</p>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="ml-auto pl-3 opacity-70 hover:opacity-100"
          >
            <XCircle className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
}

interface NetworkErrorProps {
  onRetry?: () => void;
  className?: string | undefined;
}

export function NetworkError({ onRetry, className }: NetworkErrorProps) {
  return (
    <ErrorState
      variant="network"
      title="Connection Problem"
      message="Unable to connect to the server. Please check your internet connection."
      onRetry={onRetry}
      className={className}
    />
  );
}

interface NotFoundErrorProps {
  resource?: string;
  onGoBack?: () => void;
  className?: string | undefined;
}

export function NotFoundError({
  resource = "page",
  onGoBack,
  className,
}: NotFoundErrorProps) {
  return (
    <ErrorState
      variant="not-found"
      title="Not Found"
      message={`The ${resource} you're looking for doesn't exist or has been moved.`}
      onRetry={onGoBack}
      retryText="Go back"
      showRetry={!!onGoBack}
      className={className}
    />
  );
}