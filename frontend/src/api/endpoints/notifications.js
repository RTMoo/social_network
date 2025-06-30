import api from '../baseApi';

// Получить уведомления с фильтрацией
export const getNotifications = (isRead = null) => {
  const params = new URLSearchParams();
  if (isRead !== null) {
    params.append('is_read', isRead.toString());
  }
  
  return api.get(`/notifications${params.toString() ? `?${params.toString()}` : ''}`);
};

// Отметить уведомление как прочитанное
export const markAsRead = (notificationId) => {
  return api.post(`/notifications/${notificationId}/mark-read/`);
};

// Удалить уведомление
export const deleteNotification = (notificationId) => {
  return api.delete(`/notifications/${notificationId}/delete/`);
}; 