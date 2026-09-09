import { useMutation } from "@tanstack/react-query";
import { login, logout } from "./api";
import { useAuthStore } from "./store";
import { clearSessionAndRedirect } from "./utils/session";

export const useLoginMutation = () => {
  return useMutation({
    mutationFn: login,
    onSuccess: (data) => {
      useAuthStore.getState().setAccessToken(data.accessToken);
    },
  });
};

export const useLogoutMutation = () => {
  return useMutation({
    mutationFn: logout,
    onSettled: () => clearSessionAndRedirect(),
  });
};
