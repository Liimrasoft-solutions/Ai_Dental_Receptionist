import type { Metadata } from "next";
import { Suspense } from "react";
import { Public_Sans } from "next/font/google";
import Sidebar from "@/components/Sidebar";
import { apiGet } from "@/lib/api";
import type { Meta } from "@/lib/types";
import "./globals.css";

const sans = Public_Sans({ subsets: ["latin"], variable: "--font-sans", display: "swap" });

export const metadata: Metadata = { title: "Limra Dental AI", description: "Every AI agent at the practice, on one screen" };

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const meta = await apiGet<Meta>("/v1/meta").catch(() => null);
  return (
    <html lang="en" className={sans.variable}>
      <body className="min-h-screen font-sans">
        <div className="flex min-h-screen flex-col md:flex-row">
          <Suspense fallback={<nav className="bg-ink md:w-56" />}>
            <Sidebar agents={meta?.agents ?? []} user={meta?.user ?? null} />
          </Suspense>
          <main className="min-w-0 flex-1 px-4 py-5 md:px-8 md:py-7">{children}</main>
        </div>
      </body>
    </html>
  );
}
