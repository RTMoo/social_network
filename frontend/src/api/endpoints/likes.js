import api from '../baseApi';

export const likePost = (postId) => api.post(`/likes/post/${postId}/`);
export const likeComment = (commentId) => api.post(`/likes/comment/${commentId}/`);
export const getUserLikedPosts = (username) => api.get(`/likes/users/${username}/posts/`);
export const getUserLikedComments = (username) => api.get(`/likes/users/${username}/comments/`);
