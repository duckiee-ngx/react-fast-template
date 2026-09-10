import type {
  AxiosError,
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios";
import { refreshToken } from "./api";
import { useAuthStore } from "./store";
import { logoutAndClearSession } from "./utils/session";

interface RetryRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

type QueueItem = {
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
};

let isRefreshing = false;
let failedQueue: QueueItem[] = [];

const processQueue = (error: unknown, token?: string) => {
  const queue = failedQueue;
  failedQueue = [];

  queue.forEach((promise) => {
    if (token) {
      promise.resolve(token);
    } else {
      promise.reject(error ?? new Error("Failed to refresh token"));
    }
  });
};

export function attachAuthInterceptors(axiosInstance: AxiosInstance) {
  axiosInstance.interceptors.request.use((config) => {
    const accessToken = useAuthStore.getState().accessToken;
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  });

  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
      const originalRequest = error.config as RetryRequestConfig;

      // Treat 401 as expired access token and try refresh.
      // Auth endpoints use a separate authClient (no interceptors), so no URL skip needed.
      // When the API distinguishes expired vs forbidden, gate on the error body.
      if (error.response?.status !== 401 || originalRequest._retry) {
        return Promise.reject(error);
      }

      originalRequest._retry = true;
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({
            resolve: (token: string) => {
              originalRequest.headers.Authorization = `Bearer ${token}`;

              resolve(axiosInstance(originalRequest));
            },
            reject,
          });
        });
      }
      isRefreshing = true;

      try {
        const data = await refreshToken();
        const newAccessToken = data.accessToken;
        useAuthStore.getState().setAccessToken(newAccessToken);
        processQueue(null, newAccessToken);
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return axiosInstance(originalRequest);
      } catch (err) {
        processQueue(err);
        await logoutAndClearSession();
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    },
  );
}
