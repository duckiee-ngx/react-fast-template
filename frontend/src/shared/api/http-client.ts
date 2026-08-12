import { env } from "@src/configs/env"
import { AUTH_API_ENDPOINTS } from "@src/modules/auth/constants"
import { refreshTokenMapper } from "@src/modules/auth/mapper"
import { useAuthStore } from "@src/modules/auth/store"
import { clearSessionAndRedirect } from "@src/modules/auth/utils/session"
import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios"

interface RetryRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean
}

type QueueItem = {
  resolve: (token: string) => void
  reject: (error: unknown) => void
}

let isRefreshing = false
let failedQueue: QueueItem[] = []

const processQueue = (error: unknown, token?: string) => {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error)
    } else if (token) {
      promise.resolve(token)
    }
  })

  failedQueue = []
}

async function handleRefreshToken() {
  const response = await axios.post(
    `${env.VITE_API_URL}${AUTH_API_ENDPOINTS.REFRESH_TOKEN}`,
    {},
    { withCredentials: true },
  )
  return refreshTokenMapper.fromResponse(response.data)
}

async function handleLogout() {
  try {
    await axios.post(
      `${env.VITE_API_URL}${AUTH_API_ENDPOINTS.LOGOUT}`,
      {},
      { withCredentials: true },
    )
  } catch {
    // ignore
  } finally {
    clearSessionAndRedirect()
  }
}

const createAxiosInstance = (baseURL: string) => {
  const axiosInstance = axios.create({
    baseURL,
    withCredentials: true,
    paramsSerializer: (params) => {
      const searchParams = new URLSearchParams()

      Object.entries(params).forEach(([key, value]) => {
        // skip null, undefined, empty string
        if (value === null || value === undefined || value === "") return

        if (Array.isArray(value)) {
          value.forEach((v) => {
            if (v === null || v === undefined || v === "") return
            searchParams.append(key, String(v))
          })
        } else {
          searchParams.append(key, String(value))
        }
      })

      return searchParams.toString()
    },
  })

  axiosInstance.interceptors.request.use((config) => {
    const accessToken = useAuthStore.getState().accessToken
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }
    return config
  })

  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
      const originalRequest = error.config as RetryRequestConfig

      if (error.response?.status !== 401 || originalRequest._retry) {
        return Promise.reject(error)
      }

      if (
        originalRequest.url?.includes(AUTH_API_ENDPOINTS.LOGIN) ||
        originalRequest.url?.includes(AUTH_API_ENDPOINTS.REFRESH_TOKEN)
      ) {
        return Promise.reject(error)
      }

      originalRequest._retry = true
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({
            resolve: (token: string) => {
              originalRequest.headers.Authorization = `Bearer ${token}`

              resolve(axiosInstance(originalRequest))
            },
            reject,
          })
        })
      }
      isRefreshing = true

      try {
        const data = await handleRefreshToken()
        const newAccessToken = data.accessToken
        useAuthStore.getState().setAccessToken(newAccessToken)
        processQueue(null, newAccessToken)
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        return axiosInstance(originalRequest)
      } catch (err) {
        processQueue(err)
        await handleLogout()
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    },
  )

  return axiosInstance
}

export const httpClient = createAxiosInstance(env.VITE_API_URL)
