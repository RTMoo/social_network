import api from '../baseApi';

export const sendFriendRequest = (username) => api.post(`/friendships/requests/${username}/send/`);
export const acceptFriendRequest = (username) => api.post(`/friendships/requests/${username}/accept/`);
export const rejectFriendRequest = (username) => api.delete(`/friendships/requests/${username}/reject/`);
export const deleteFriend = (username) => api.delete(`/friendships/${username}/delete/`);
export const getFriends = (username) => api.get(`/friendships/${username}/list/`);
export const getReceivedRequests = () => api.get('/friendships/requests/received/');
export const getSentRequests = () => api.get('/friendships/requests/sent/');
