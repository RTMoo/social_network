import api from '../baseApi';

export const subscribe = (username) => api.post(`/subscriptions/subscribe/${username}/`);
export const unsubscribe = (username) => api.delete(`/subscriptions/subscribe/${username}/`);
export const getSubscriptions = (username) => api.get(`/subscriptions/${username}/subscription-list/`);
export const getSubscribers = (username) => api.get(`/subscriptions/${username}/subscriber-list/`);
