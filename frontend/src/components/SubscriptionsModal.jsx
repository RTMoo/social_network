import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import * as subscriptionsApi from '../api/endpoints/subscriptions';

export default function SubscriptionsModal({ 
  isOpen, 
  onClose, 
  username, 
  type, // 'subscriptions' или 'subscribers'
  backendUrl,
  currentUser, // добавляем текущего пользователя для проверки прав
  onSubscriptionChange // callback для уведомления об изменениях
}) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [actionLoading, setActionLoading] = useState({}); // для отслеживания загрузки действий

  useEffect(() => {
    if (isOpen && username) {
      fetchUsers();
    }
  }, [isOpen, username, type]);

  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const apiCall = type === 'subscriptions' ? subscriptionsApi.getSubscriptions : subscriptionsApi.getSubscribers;
      const res = await apiCall(username);
      setUsers(res.data);
    } catch (e) {
      setError('Ошибка загрузки данных');
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleUnsubscribe = async (targetUsername) => {
    if (!window.confirm('Вы уверены, что хотите отписаться от этого пользователя?')) return;
    
    setActionLoading(prev => ({ ...prev, [targetUsername]: true }));
    try {
      await subscriptionsApi.unsubscribe(targetUsername);
      // Обновляем список после отписки
      await fetchUsers();
      // Уведомляем родительский компонент об изменении
      if (onSubscriptionChange) {
        onSubscriptionChange();
      }
    } catch (e) {
      setError('Ошибка при отписке');
      console.error(e);
    } finally {
      setActionLoading(prev => ({ ...prev, [targetUsername]: false }));
    }
  };

  const handleRemoveSubscriber = async (targetUsername) => {
    if (!window.confirm('Вы уверены, что хотите удалить этого подписчика?')) return;
    
    setActionLoading(prev => ({ ...prev, [targetUsername]: true }));
    try {
      // Используем специальный API для удаления подписчика
      await subscriptionsApi.deleteSubscriber(targetUsername);
      // Обновляем список после удаления
      await fetchUsers();
      // Уведомляем родительский компонент об изменении
      if (onSubscriptionChange) {
        onSubscriptionChange();
      }
    } catch (e) {
      setError('Ошибка при удалении подписчика');
      console.error(e);
    } finally {
      setActionLoading(prev => ({ ...prev, [targetUsername]: false }));
    }
  };

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const title = type === 'subscriptions' ? 'Подписки' : 'Подписчики';
  const isCurrentUserProfile = currentUser?.username === username;

  return (
    <div className="fixed inset-0 bg-[#00000099] flex items-center justify-center z-50 p-4" onClick={handleBackdropClick}>
      <div className="bg-white rounded-lg w-full max-w-lg max-h-[85vh] flex flex-col overflow-hidden shadow-2xl">
        {/* Заголовок */}
        <div className="flex justify-between items-center p-4 border-b">
          <h3 className="text-lg font-semibold">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        {/* Содержимое */}
        <div className="flex-1 overflow-y-auto">
          {error && (
            <div className="p-4 text-red-500 text-center">{error}</div>
          )}
          
          {loading ? (
            <div className="p-8 text-center text-gray-500">Загрузка...</div>
          ) : users.length > 0 ? (
            <div className="p-4">
              {users.map((user) => (
                <div key={user.username} className="flex items-center gap-4 p-4 hover:bg-gray-50 rounded-lg transition-colors">
                  <Link
                    to={`/profile/${user.username}`}
                    onClick={onClose}
                    className="flex items-center gap-4 flex-1 min-w-0"
                  >
                    <div className="w-14 h-14 rounded-full bg-gray-200 overflow-hidden flex-shrink-0">
                      {user.avatar ? (
                        <img 
                          src={`${backendUrl}${user.avatar}`} 
                          alt={user.username} 
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-gray-400 text-xl">
                          👤
                        </div>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-gray-900 truncate text-base">
                        {user.first_name && user.last_name 
                          ? `${user.first_name} ${user.last_name}` 
                          : user.username
                        }
                      </div>
                      <div className="text-sm text-gray-500 truncate">
                        @{user.username}
                      </div>
                    </div>
                  </Link>
                  
                  {/* Кнопки действий */}
                  {currentUser && (
                    <div className="flex-shrink-0">
                      {type === 'subscriptions' && isCurrentUserProfile && (
                        <button
                          onClick={() => handleUnsubscribe(user.username)}
                          disabled={actionLoading[user.username]}
                          className="px-4 py-2 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors disabled:opacity-50"
                        >
                          {actionLoading[user.username] ? '...' : 'Отписаться'}
                        </button>
                      )}
                      {type === 'subscribers' && isCurrentUserProfile && (
                        <button
                          onClick={() => handleRemoveSubscriber(user.username)}
                          disabled={actionLoading[user.username]}
                          className="px-4 py-2 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors disabled:opacity-50"
                        >
                          {actionLoading[user.username] ? '...' : 'Удалить'}
                        </button>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="p-8 text-center text-gray-500">
              <span className="text-4xl mb-4 block">
                {type === 'subscriptions' ? '👥' : '👤'}
              </span>
              <p>
                {type === 'subscriptions' 
                  ? 'Пока нет подписок' 
                  : 'Пока нет подписчиков'
                }
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 