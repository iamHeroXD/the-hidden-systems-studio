import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "The Hidden Systems Studio | Autonomous Documentary Platform",
  description: "Autonomous AI Animated Documentary Production Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-studio-950 text-studio-chalk antialiased selection:bg-studio-amber selection:text-studio-950">
        {children}
      </body>
    </html>
  );
}
