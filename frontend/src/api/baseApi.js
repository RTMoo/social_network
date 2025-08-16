import axios from 'axios';

// Базовый URL API
const API_BASE_URL = "http://94.131.82.187/api/"

// Создаём инстанс axios
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // для передачи cookie
});

// Публичные эндпоинты, для которых не делаем refresh или редирект
const PUBLIC_ENDPOINTS = [
  '/accounts/register/',
  '/accounts/login/',
  '/accounts/confirm_code/',
];

// Флаг, чтобы не делать несколько refresh одновременно
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    // Игнорируем публичные эндпоинты
    if (PUBLIC_ENDPOINTS.some(url => originalRequest.url.endsWith(url))) {
      return Promise.reject(error);
    }

    // Обработка 401 для защищённых эндпоинтов
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(() => api(originalRequest))
          .catch(err => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;
      try {
        await api.post('/accounts/refresh/');
        processQueue(null);
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        // Можно добавить logout-логику здесь
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;
