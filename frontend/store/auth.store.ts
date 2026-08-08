import { create } from "zustand";

import type { UserResponse } from "@/services/auth.service";

interface AuthState {
  token: string | null;
  user: UserResponse | null;

  setAuth: (
    token: string,
    user: UserResponse,
  ) => void;

  setUser: (
    user: UserResponse | null,
  ) => void;

  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,

  setAuth: (token, user) =>
    set({
      token,
      user,
    }),

  setUser: (user) =>
    set({
      user,
    }),

  logout: () =>
    set({
      token: null,
      user: null,
    }),
}));