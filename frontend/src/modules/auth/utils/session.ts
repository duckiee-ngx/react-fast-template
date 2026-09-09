import { queryClient } from "@src/providers/query-provider";
import { refreshToken } from "../api";
import { useAuthStore } from "../store";

let inflight: Promise<boolean> | null = null;
let epoch = 0;
let goLogin: (() => void) | null = null;

export function registerSessionNavigator(navigateToLogin: () => void) {
  goLogin = navigateToLogin;
}

export function clearSessionAndRedirect() {
  epoch += 1;
  inflight = null;
  useAuthStore.getState().clearAccessToken();
  queryClient.clear();
  goLogin?.();
}

export function ensureSession(): Promise<boolean> {
  if (useAuthStore.getState().accessToken) {
    return Promise.resolve(true);
  }

  const started = epoch;
  inflight ??= refreshToken()
    .then((data) => {
      if (started !== epoch) return false;
      useAuthStore.getState().setAccessToken(data.accessToken);
      return true;
    })
    .catch(() => false)
    .finally(() => {
      inflight = null;
    });

  return inflight;
}
