import { useMutation } from "@tanstack/react-query";
import { login } from "./api";
import { useAuthStore } from "./store";
import { logoutAndClearSession } from "./utils/session";

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
    mutationFn: logoutAndClearSession,
  });
};
