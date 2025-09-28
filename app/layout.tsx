import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { Providers } from "@/components/providers"
import { Toaster } from "react-hot-toast"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Kisan Saathi - Farmer Advisory System",
  description: "A comprehensive agricultural advisory platform providing farming guidance, crop recommendations, and agricultural insights for farmers.",
  keywords: [
    "agriculture",
    "farming",
    "crop recommendation",
    "disease detection",
    "farmer advisory",
    "agricultural technology",
    "farming platform",
    "agricultural guidance"
  ],
  authors: [{ name: "Kisan Saathi Team" }],
  creator: "Kisan Saathi",
  publisher: "Kisan Saathi",
  robots: "index, follow",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "http://localhost:3000",
    title: "Kisan Saathi - Farmer Advisory System",
    description: "Supporting farmers with agricultural guidance and recommendations",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Kisan Saathi - Farmer Advisory System",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Kisan Saathi - Farmer Advisory System",
    description: "Supporting farmers with agricultural guidance and recommendations",
    images: ["/og-image.jpg"],
  },
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/site.webmanifest",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className} suppressHydrationWarning>
        <Providers>
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'hsl(var(--card))',
                color: 'hsl(var(--card-foreground))',
                border: '1px solid hsl(var(--border))',
              },
            }}
          />
        </Providers>
      </body>
    </html>
  )
}
