import api from '../baseApi';

export const register = (data) => api.post('/accounts/register/', data);
export const login = (data) => api.post('/accounts/login/', data);
export const logout = () => api.post('/accounts/logout/');
export const confirmCode = (data) => api.post('/accounts/confirm_code/', data);

// Получить профиль текущего пользователя
export const getMe = () => api.get('/profiles/me/');
