/** biome-ignore-all lint/suspicious/noExplicitAny: data is any */
import type { LoginRequest, TokenResponse } from "./schemas"

const mapTokenResponse = (data: any): TokenResponse => {
  return {
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
  }
}

export const loginMapper = {
  fromResponse: mapTokenResponse,
  toRequest: (body: LoginRequest) => ({
    email: body.email,
    password: body.password,
  }),
}

export const refreshTokenMapper = {
  fromResponse: mapTokenResponse,
}
