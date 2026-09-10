import { env } from "@src/configs/env";
import axios from "axios";

export const createAxiosInstance = (baseURL: string) => {
  const axiosInstance = axios.create({
    baseURL,
    withCredentials: true,
    paramsSerializer: (params) => {
      const searchParams = new URLSearchParams();

      Object.entries(params).forEach(([key, value]) => {
        // skip null, undefined, empty string
        if (value === null || value === undefined || value === "") return;

        if (Array.isArray(value)) {
          value.forEach((v) => {
            if (v === null || v === undefined || v === "") return;
            searchParams.append(key, String(v));
          });
        } else {
          searchParams.append(key, String(value));
        }
      });

      return searchParams.toString();
    },
  });

  return axiosInstance;
};

export const httpClient = createAxiosInstance(env.VITE_API_URL);
