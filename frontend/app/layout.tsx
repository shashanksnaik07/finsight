import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FinSight — Personal Financial Intelligence",
  description: "Upload your financial documents and ask anything about your money.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ background: "#0A0F1E" }}>{children}</body>
    </html>
  );
}