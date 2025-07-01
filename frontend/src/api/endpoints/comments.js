import api from '../baseApi';

export const createComment = (data) => api.post('/comments/create/', data);
export const getPostComments = (postId) => api.get(`/comments/post/${postId}/`);
export const getCommentReplies = (commentId) => api.get(`/comments/${commentId}/replies/`);
export const getUserComments = (username) => api.get(`/comments/user/${username}/`);
export const updateComment = (commentId, data) => api.patch(`/comments/${commentId}/update/`, data);
export const deleteComment = (commentId) => api.delete(`/comments/${commentId}/delete/`);
export const getComment = (commentId) => api.get(`/comments/${commentId}/`);
