import { apiClient } from "@/lib/api-client";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: number;
  tenant_id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export async function login(
  request: LoginRequest,
): Promise<TokenResponse> {
  return apiClient<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function register(
  request: RegisterRequest,
): Promise<UserResponse> {
  return apiClient<UserResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function getCurrentUser(
  token: string,
): Promise<UserResponse> {
  return apiClient<UserResponse>("/auth/me", {
    method: "GET",
    token,
  });
}