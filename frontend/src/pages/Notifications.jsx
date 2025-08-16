import { useState, useEffect } from 'react';
import { getNotifications, markAsRead, deleteNotification, postsApi } from '../api';
import { Link } from 'react-router-dom';
import PostModal from '../components/PostModal';

const Notifications = () => {
  const [activeTab, setActiveTab] = useState('unread');
  const [unreadNotifications, setUnreadNotifications] = useState([]);
  const [readNotifications, setReadNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedPost, setSelectedPost] = useState(null);

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    setLoading(true);
    try {
      const [unreadResponse, readResponse] = await Promise.all([
        getNotifications(false),
        getNotifications(true)
      ]);
      
      setUnreadNotifications(unreadResponse.data);
      setReadNotifications(readResponse.data);
    } catch (error) {
      console.error('Ошибка загрузки уведомлений:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (notificationId) => {
    try {
      await markAsRead(notificationId);
      await loadNotifications();
    } catch (error) {
      console.error('Ошибка при отметке как прочитанное:', error);
    }
  };

  const handleDelete = async (notificationId) => {
    try {
      await deleteNotification(notificationId);
      await loadNotifications();
    } catch (error) {
      console.error('Ошибка при удалении уведомления:', error);
    }
  };

  const getNotificationText = (notification, onPostTitleClick) => {
    const fromUserLink = (
      <Link to={`/profile/${notification.from_user}`} className="text-blue-600 hover:underline font-semibold" onClick={e => e.stopPropagation()}>
        {notification.from_user || 'Пользователь'}
      </Link>
    );
    const postTitle = notification.post_id ? (
      <span
        className="text-blue-600 hover:underline font-semibold cursor-pointer"
        onClick={e => {
          e.stopPropagation();
          onPostTitleClick(notification);
        }}
      >
        {notification.post_title || 'пост'}
      </span>
    ) : (notification.post_title || 'пост');

    switch (notification.type) {
      case 'new_post':
        return <>{fromUserLink} опубликовал пост: {postTitle}</>;
      case 'like':
        return <>{fromUserLink} поставил лайк вашему посту: {postTitle}</>;
      case 'comment':
        return <>{fromUserLink} написал комментарий к посту: {postTitle}: "{notification.comment_text || ''}"</>;
      case 'subscribe':
        return <>{fromUserLink} подписался на вас</>;
      default:
        return 'Новое уведомление';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) {
      return 'Только что';
    } else if (diffInHours < 24) {
      return `${diffInHours} ч. назад`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays} дн. назад`;
    }
  };

  const handleNotificationClick = async (notification) => {
    if (notification.post_id) {
      try {
        const res = await postsApi.getPost(notification.post_id);
        setSelectedPost(res.data);
        setIsModalOpen(true);
      } catch (e) {
        console.error('Ошибка загрузки поста:', e);
      }
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedPost(null);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Уведомления</h1>

      {/* Вкладки */}
      <div className="flex border-b mb-6">
        <button
          onClick={() => setActiveTab('unread')}
          className={`px-6 py-3 font-medium border-b-2 transition-colors ${
            activeTab === 'unread'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Непрочитанные ({unreadNotifications.length})
        </button>
        <button
          onClick={() => setActiveTab('read')}
          className={`px-6 py-3 font-medium border-b-2 transition-colors ${
            activeTab === 'read'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Прочитанные ({readNotifications.length})
        </button>
      </div>

      {/* Содержимое */}
      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-500">Загрузка уведомлений...</p>
        </div>
      ) : (
        <div className="space-y-4">
          {activeTab === 'unread' && (
            <>
              {unreadNotifications.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">🔔</div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Нет непрочитанных уведомлений
                  </h3>
                  <p className="text-gray-500">
                    Когда появятся новые уведомления, они будут показаны здесь
                  </p>
                </div>
              ) : (
                unreadNotifications.map((notification) => (
                  <div
                    key={notification.id}
                    className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-blue-600 font-semibold">
                              {notification.from_user?.charAt(0).toUpperCase() || 'U'}
                            </span>
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">
                              {getNotificationText(notification, handleNotificationClick)}
                            </p>
                            <p className="text-sm text-gray-500">
                              {formatDate(notification.created_at)}
                            </p>
                          </div>
                        </div>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleMarkAsRead(notification.id);
                        }}
                        className="ml-4 px-4 py-2 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                      >
                        Прочитано
                      </button>
                    </div>
                  </div>
                ))
              )}
            </>
          )}

          {activeTab === 'read' && (
            <>
              {readNotifications.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">📖</div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Нет прочитанных уведомлений
                  </h3>
                  <p className="text-gray-500">
                    Прочитанные уведомления будут показаны здесь
                  </p>
                </div>
              ) : (
                readNotifications.map((notification) => (
                  <div
                    key={notification.id}
                    className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                            <span className="text-gray-600 font-semibold">
                              {notification.from_user?.charAt(0).toUpperCase() || 'U'}
                            </span>
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">
                              {getNotificationText(notification, handleNotificationClick)}
                            </p>
                            <p className="text-sm text-gray-400">
                              {formatDate(notification.created_at)}
                            </p>
                          </div>
                        </div>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(notification.id);
                        }}
                        className="ml-4 px-4 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                      >
                        Удалить
                      </button>
                    </div>
                  </div>
                ))
              )}
            </>
          )}
        </div>
      )}

      <PostModal
        post={selectedPost}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </div>
  );
};

export default Notifications; 