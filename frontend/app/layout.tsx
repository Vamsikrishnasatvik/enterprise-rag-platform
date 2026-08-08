import "./globals.css";

import QueryProvider from "@/providers/react-query-provider";
import AppShell from "@/components/layout/app-shell";

export const metadata = {
  title: "Enterprise RAG Platform",
  description:
    "Enterprise Agentic Retrieval-Augmented Generation Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>
          <AppShell>{children}</AppShell>
        </QueryProvider>
      </body>
    </html>
  );
}