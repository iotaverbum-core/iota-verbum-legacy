import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Iota Verbum (IV) - Computational Theology Framework",
  description: "A computational framework combining Modal Logic, AI Ethics, and Biblical Theology for verifiable, deterministic theological analysis.",
  keywords: ["Modal Logic", "AI Ethics", "Biblical Theology", "Computational Theology", "Witness Cards", "Deterministic AI"],
  authors: [{ name: "Iota Verbum Team" }],
  icons: {
    icon: "/logo.svg",
  },
  openGraph: {
    title: "Iota Verbum (IV)",
    description: "Modal Logic + AI Ethics + Biblical Theology",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        {children}
        <Toaster />
      </body>
    </html>
  );
}
