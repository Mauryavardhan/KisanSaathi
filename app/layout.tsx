import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { Providers } from "@/components/providers"
import { Toaster } from "react-hot-toast"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Kisan Saathi - AI-Powered Farmer Advisory System",
  description: "An intelligent agricultural advisory platform providing personalized farming guidance, crop recommendations, disease detection, and market insights for farmers.",
  keywords: [
    "agriculture",
    "farming",
    "AI",
    "crop recommendation",
    "disease detection",
    "farmer advisory",
    "agricultural technology",
    "precision farming",
    "smart agriculture"
  ],
  authors: [{ name: "Kisan Saathi Team" }],
  creator: "Kisan Saathi",
  publisher: "Kisan Saathi",
  robots: "index, follow",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://kisan-saathi.vercel.app",
    title: "Kisan Saathi - AI-Powered Farmer Advisory System",
    description: "Empowering farmers with AI-driven agricultural insights and recommendations",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Kisan Saathi - AI-Powered Farmer Advisory System",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Kisan Saathi - AI-Powered Farmer Advisory System",
    description: "Empowering farmers with AI-driven agricultural insights and recommendations",
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
