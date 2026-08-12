import { useAuthStore } from "../store";

export function clearSessionAndRedirect(loginPath = "/auth/login") {
  useAuthStore.getState().clearAccessToken();
  window.location.href = loginPath;
}
