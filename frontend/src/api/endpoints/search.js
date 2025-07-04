import api from '../baseApi';

export const searchProfiles = (query) => api.get(`/search/?q=${encodeURIComponent(query)}`); 