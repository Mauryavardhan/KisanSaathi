"use client"

import * as React from "react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { SessionProvider } from "next-auth/react"
import { ThemeProvider } from "next-themes"
import { ErrorBoundary } from "@/components/error-boundary"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 2,
    },
  },
})

interface ProvidersProps {
  children: React.ReactNode
}

export function Providers({ children }: ProvidersProps) {
  return (
    <ErrorBoundary>
      <SessionProvider>
        <QueryClientProvider client={queryClient}>
          <ThemeProvider
            attribute="class"
            defaultTheme="light"
            enableSystem
            disableTransitionOnChange
          >
            {children}
          </ThemeProvider>
        </QueryClientProvider>
      </SessionProvider>
    </ErrorBoundary>
  )
}
