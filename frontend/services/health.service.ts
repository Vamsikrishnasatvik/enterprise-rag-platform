import { apiClient } from "@/lib/api-client";

export interface HealthResponse {
  status: string;
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await apiClient<HealthResponse>("/health");

  return response;
}