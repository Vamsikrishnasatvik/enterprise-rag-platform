"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { useHealth } from "@/hooks/use-health";

const navigation = [
  {
    label: "Dashboard",
    href: "/",
  },
  {
    label: "Chat",
    href: "/chat",
  },
  {
    label: "Documents",
    href: "/documents",
  },
  {
    label: "Conversations",
    href: "/conversations",
  },
  {
    label: "Analytics",
    href: "/analytics",
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  const {
  isLoading,
  isSuccess,
  data,
} = useHealth();

const backendOnline =
  isSuccess && data?.status === "ok";

  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col border-r border-zinc-200 bg-white">
      <div className="border-b border-zinc-200 px-6 py-5">
        <h1 className="text-lg font-semibold text-zinc-900">
          Enterprise RAG
        </h1>

        <p className="mt-1 text-xs text-zinc-500">
          AI Knowledge Platform
        </p>
      </div>

      <nav className="flex-1 space-y-1 p-4">
        {navigation.map((item) => {
          const isActive =
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={[
                "block rounded-lg px-3 py-2.5 text-sm font-medium transition",
                isActive
                  ? "bg-zinc-900 text-white"
                  : "text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900",
              ].join(" ")}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-zinc-200 p-4">
        <div className="rounded-lg bg-zinc-50 px-3 py-3">
            <p className="text-xs font-medium text-zinc-700">
            Backend Status
            </p>

            <div className="mt-2 flex items-center gap-2">
            <span
                className={[
                "h-2 w-2 rounded-full",
                isLoading
                    ? "bg-amber-400"
                    : backendOnline
                    ? "bg-emerald-500"
                    : "bg-red-500",
                ].join(" ")}
            />

            <span className="text-xs text-zinc-500">
                {isLoading
                ? "Checking..."
                : backendOnline
                    ? "Online"
                    : "Offline"}
            </span>
            </div>

            {!isLoading && (
            <p className="mt-2 text-[11px] text-zinc-400">
                {data?.status
                ? `API: ${data.status}`
                : "No health response"}
            </p>
            )}
        </div>
        </div>
    </aside>
  );
}