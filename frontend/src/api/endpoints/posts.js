import api from '../baseApi';

export const createPost = (data) => api.post('/posts/create/', data);
export const getUserPosts = (username) => api.get(`/posts/list/${username}/`);
export const getPost = (postId) => api.get(`/posts/get/${postId}/`);
export const updatePost = (postId, data) => api.patch(`/posts/update/${postId}/`, data);
export const deletePost = (postId) => api.delete(`/posts/delete/${postId}/`);
export const getFeed = () => api.get('/posts/subscriptions_posts/');
