import "./globals.css";
import QueryProvider from "@/providers/react-query-provider";

export const metadata = {
  title: "Enterprise RAG Platform",
  description: "Enterprise AI Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>docker compose logs frontend --tail 30
        <QueryProvider>
          {children}
        </QueryProvider>
      </body>
    </html>
  );
}