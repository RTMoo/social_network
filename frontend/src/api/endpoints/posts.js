import api from '../baseApi';

export const createPost = (formData) => api.post('/posts/create/', formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const getUserPosts = (username) => api.get(`/posts/list/${username}/`);
export const getPost = (postId) => api.get(`/posts/get/${postId}/`);
export const updatePost = (postId, data) => api.patch(`/posts/update/${postId}/`, data);
export const deletePost = (postId) => api.delete(`/posts/delete/${postId}/`);
export const getSubscriptionPosts = () => api.get('/posts/subscriptions_posts/');
export const getAllPosts = () => api.get('/posts/all/');
