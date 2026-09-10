import { env } from "@src/configs/env";
import { createAxiosInstance } from "@src/shared/api/http-client";
import { AUTH_API_ENDPOINTS } from "./constants";
import { loginMapper, refreshTokenMapper } from "./mapper";
import type { LoginRequest } from "./schemas";

const authClient = createAxiosInstance(env.VITE_API_URL);

export const login = async (body: LoginRequest) => {
  const response = await authClient.post(
    AUTH_API_ENDPOINTS.LOGIN,
    loginMapper.toRequest(body),
  );
  return loginMapper.fromResponse(response.data);
};

export const logout = async () => {
  return await authClient.post(AUTH_API_ENDPOINTS.LOGOUT);
};

export const refreshToken = async () => {
  const response = await authClient.post(AUTH_API_ENDPOINTS.REFRESH_TOKEN);
  return refreshTokenMapper.fromResponse(response.data);
};
