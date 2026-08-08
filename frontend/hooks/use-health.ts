"use client";

import { useQuery } from "@tanstack/react-query";

import { getHealth } from "@/services/health.service";

export function useHealth() {
  return useQuery({
    queryKey: ["backend-health"],
    queryFn: getHealth,
    retry: 1,
    refetchInterval: 30_000,
  });
}