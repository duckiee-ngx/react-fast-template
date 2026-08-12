import { httpClient } from "@src/shared/api/http-client";
import { AUTH_API_ENDPOINTS } from "./constants";
import { loginMapper, refreshTokenMapper } from "./mapper";
import type { LoginRequest } from "./schemas";

export const login = async (body: LoginRequest) => {
  const response = await httpClient.post(AUTH_API_ENDPOINTS.LOGIN, loginMapper.toRequest(body));
  return loginMapper.fromResponse(response.data);
};

export const logout = async () => {
  return await httpClient.post(AUTH_API_ENDPOINTS.LOGOUT);
};

export const refreshToken = async () => {
  const response = await httpClient.post(AUTH_API_ENDPOINTS.REFRESH_TOKEN);
  return refreshTokenMapper.fromResponse(response.data);
};
