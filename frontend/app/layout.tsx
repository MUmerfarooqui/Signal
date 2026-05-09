import type { Metadata } from "next"
import { Geist } from "next/font/google"
import { ClerkProvider } from "@clerk/nextjs"
import Script from "next/script"
import { ThemeProvider } from "@/components/theme-provider"
import "./globals.css"

const geist = Geist({ subsets: ["latin"], variable: "--font-geist-sans" })

export const metadata: Metadata = {
  title: "Signal",
  description: "AI-native product intelligence",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en" className={`${geist.variable} h-full`} suppressHydrationWarning>
        <body className="h-full antialiased">
          <Script id="theme-init" strategy="beforeInteractive">{`try{var t=localStorage.getItem('signal-theme');if(t==='dark')document.documentElement.classList.add('dark')}catch(e){}`}</Script>
          <ThemeProvider>
            {children}
          </ThemeProvider>
        </body>
      </html>
    </ClerkProvider>
  )
}
