import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Providers } from "./providers";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AI Procurement Control Tower",
  description:
    "Real-time supplier performance, inventory risk, and spend visibility - powered by an AI operations agent.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      // next-themes sets the "dark" class on this element after the page
      // loads (it has to run client-side to read the saved preference), so
      // the server-rendered HTML and the first client render briefly
      // disagree on this one attribute. suppressHydrationWarning tells React
      // that's expected here, instead of logging a false-positive warning.
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
