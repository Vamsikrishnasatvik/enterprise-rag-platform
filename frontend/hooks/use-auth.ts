"use client";

import { useMutation, useQuery } from "@tanstack/react-query";

import {
  getCurrentUser,
  login,
  register,
  type LoginRequest,
  type RegisterRequest,
} from "@/services/auth.service";

import { useAuthStore } from "@/store/auth.store";

export function useLogin() {
  const setAuth = useAuthStore(
    (state) => state.setAuth,
  );

  return useMutation({
    mutationFn: (request: LoginRequest) =>
      login(request),

    onSuccess: async (tokenResponse) => {
      const user = await getCurrentUser(
        tokenResponse.access_token,
      );

      setAuth(
        tokenResponse.access_token,
        user,
      );
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: (
      request: RegisterRequest,
    ) => register(request),
  });
}

export function useCurrentUser() {
  const token = useAuthStore(
    (state) => state.token,
  );

  return useQuery({
    queryKey: ["current-user"],
    queryFn: () => {
      if (!token) {
        throw new Error("No authentication token.");
      }

      return getCurrentUser(token);
    },
    enabled: Boolean(token),
  });
}
