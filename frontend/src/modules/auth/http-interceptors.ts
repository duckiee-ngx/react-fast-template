import { env } from "@src/configs/env";
import type {
  AxiosError,
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios";
import axios from "axios";
import { AUTH_API_ENDPOINTS } from "./constants";
import { refreshTokenMapper } from "./mapper";
import { useAuthStore } from "./store";
import { clearSessionAndRedirect } from "./utils/session";

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

async function handleRefreshToken() {
  const response = await axios.post(
    `${env.VITE_API_URL}${AUTH_API_ENDPOINTS.REFRESH_TOKEN}`,
    {},
    { withCredentials: true },
  );
  return refreshTokenMapper.fromResponse(response.data);
}

async function handleLogout() {
  try {
    await axios.post(
      `${env.VITE_API_URL}${AUTH_API_ENDPOINTS.LOGOUT}`,
      {},
      { withCredentials: true },
    );
  } catch {
    // ignore
  } finally {
    clearSessionAndRedirect();
  }
}

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

      // Treat 401 as an expired access token and try refresh (skip auth URLs
      // to avoid a retry loop). When the API distinguishes expired vs forbidden,
      // gate this on the error body instead of status alone.
      if (error.response?.status !== 401 || originalRequest._retry) {
        return Promise.reject(error);
      }

      if (
        originalRequest.url?.includes(AUTH_API_ENDPOINTS.LOGIN) ||
        originalRequest.url?.includes(AUTH_API_ENDPOINTS.REFRESH_TOKEN) ||
        originalRequest.url?.includes(AUTH_API_ENDPOINTS.LOGOUT)
      ) {
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
        const data = await handleRefreshToken();
        const newAccessToken = data.accessToken;
        useAuthStore.getState().setAccessToken(newAccessToken);
        processQueue(null, newAccessToken);
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return axiosInstance(originalRequest);
      } catch (err) {
        processQueue(err);
        await handleLogout();
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    },
  );
}
