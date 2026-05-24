import type React from "react"
import type { Metadata } from "next"
import "./globals.css"
import "./framer-fonts.css"
import "./framer-styles.css"

export const metadata: Metadata = {
  title: "Stratigo Collectives",
  description:
    "Stratigo Collectives is a leading UI/UX and product design agency based in Nepal, helping startups and enterprises across Southeast Asia create intuitive digital presence and brand design.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  )
}