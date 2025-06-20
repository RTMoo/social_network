import api from '../baseApi';

export const getProfile = (username) => api.get(`/profiles/${username}/`);
export const updateProfile = (data) => api.patch('/profiles/me/update/', data);
export const updateAvatar = (formData) => api.patch('/profiles/me/update/', formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});
