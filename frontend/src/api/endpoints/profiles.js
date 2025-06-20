import api from '../baseApi';

export const getProfile = (username) => api.get(`/profiles/${username}/`);
export const updateProfile = (data) => api.patch('/profiles/me/update/', data);
