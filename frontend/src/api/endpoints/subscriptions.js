import api from '../baseApi';

export const subscribe = (username) => api.post(`/subscriptions/subscribe/${username}/`);
export const unsubscribe = (username) => api.delete(`/subscriptions/unsubscribe/${username}/`);
export const getSubscriptions = (username) => api.get(`/subscriptions/subscriptions/${username}/`);
export const getSubscribers = (username) => api.get(`/subscriptions/subscribers/${username}/`);
