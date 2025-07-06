import api from '../baseApi';

// Получить список чатов пользователя
export const getChats = () => api.get('/chats/');

// Создать новый чат с пользователем
export const createChat = (username) => api.post('/chats/create/', { to_user: username });

// Получить информацию о чате
export const getChat = (chatId) => api.get(`/chats/${chatId}/`);

// Получить сообщения чата
export const getChatMessages = (chatId) => api.get(`/chats/${chatId}/messages/`); 