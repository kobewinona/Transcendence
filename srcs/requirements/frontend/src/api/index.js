import axios from 'axios';
import { ACCESS_TOKEN_STORAGE_KEY, API_HOST } from 'config/constants.js';
import authApi from 'shared/api/Auth';
import { auth } from 'store/auth.js';

const baseURL = `${API_HOST}/api/`;

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY);

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

let isRefreshing = false;
let refreshPromise = null;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      if (!isRefreshing) {
        isRefreshing = true;
        refreshPromise = authApi
          .refreshTokens()
          .then((refreshResponse) => {
            const newAccessToken = refreshResponse?.data?.access_token;

            if (newAccessToken) {
              localStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, newAccessToken);
              api.defaults.headers.Authorization = `Bearer ${newAccessToken}`;
            }

            return newAccessToken;
          })
          .catch((refreshError) => {
            auth.logout();
            window.location.href = '/signin';
            throw refreshError;
          })
          .finally(() => {
            isRefreshing = false;
          });
      }

      try {
        const newToken = await refreshPromise;

        if (newToken) {
          error.config.headers.Authorization = `Bearer ${newToken}`;
          return api.request(error.config);
        }
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
