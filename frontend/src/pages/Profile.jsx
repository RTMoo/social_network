import { useEffect, useState, useContext, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { profilesApi } from '../api';
import { postsApi } from '../api';
import { AuthContext } from '../context/AuthContext';
import PostModal from '../components/PostModal';
import SubscriptionsModal from '../components/SubscriptionsModal';
import * as subscriptionsApi from '../api/endpoints/subscriptions';
import * as friendshipsApi from '../api/endpoints/friendships';

export default function Profile() {
  const { username } = useParams();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [posts, setPosts] = useState([]);
  const [postsLoading, setPostsLoading] = useState(true);
  const [selectedPost, setSelectedPost] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { user } = useContext(AuthContext);
  const avatarInputRef = useRef(null);
  const [subscribed, setSubscribed] = useState(false);
  const [subLoading, setSubLoading] = useState(false);
  const [subscriptionsModalOpen, setSubscriptionsModalOpen] = useState(false);
  const [subscribersModalOpen, setSubscribersModalOpen] = useState(false);
  const [subscriptionsModalType, setSubscriptionsModalType] = useState('subscriptions');
  const [imageLoading, setImageLoading] = useState({});

  const backendUrl = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace('/api/', '') : 'http://localhost:8000';

  useEffect(() => {
    async function fetchProfile() {
      setLoading(true);
      setError('');
      try {
        const res = await profilesApi.getProfile(username);
        setProfile(res.data);
        setSubscribed(!!res.data.is_subscribed);
      } catch (e) {
        setError('Профиль не найден');
      } finally {
        setLoading(false);
      }
    }

    async function fetchPosts() {
      setPostsLoading(true);
      try {
        const res = await postsApi.getUserPosts(username);
        setPosts(res.data);
      } catch (e) {
        console.error('Ошибка загрузки постов:', e);
      } finally {
        setPostsLoading(false);
      }
    }

    fetchProfile();
    fetchPosts();
  }, [username, user, backendUrl]);

  const handleAvatarChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('avatar', file);

    try {
      const res = await profilesApi.updateAvatar(formData);
      setProfile(res.data); // Обновляем профиль с новым аватаром
    } catch (err) {
      setError('Ошибка при обновлении аватара');
      console.error(err);
    }
  };

  const handlePostClick = (post) => {
    setSelectedPost(post);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedPost(null);
  };

  const handleSubscribe = async () => {
    setSubLoading(true);
    try {
      if (subscribed) {
        await subscriptionsApi.unsubscribe(username);
        setSubscribed(false);
      } else {
        await subscriptionsApi.subscribe(username);
        setSubscribed(true);
      }
      // Обновляем профиль для получения актуальной статистики
      const res = await profilesApi.getProfile(username);
      setProfile(res.data);
    } catch (e) {
      // Можно добавить обработку ошибок
    } finally {
      setSubLoading(false);
    }
  };

  const handleOpenSubscriptions = () => {
    setSubscriptionsModalType('subscriptions');
    setSubscriptionsModalOpen(true);
  };

  const handleOpenSubscribers = () => {
    setSubscriptionsModalType('subscribers');
    setSubscribersModalOpen(true);
  };

  const handleCloseSubscriptionsModal = () => {
    setSubscriptionsModalOpen(false);
  };

  const handleCloseSubscribersModal = () => {
    setSubscribersModalOpen(false);
  };

  const handleSubscriptionChange = async () => {
    // Обновляем профиль для получения актуальной статистики
    try {
      const res = await profilesApi.getProfile(username);
      setProfile(res.data);
      setSubscribed(!!res.data.is_subscribed);
    } catch (e) {
      console.error('Ошибка обновления профиля:', e);
    }
  };

  if (loading) return <div className="flex justify-center items-center min-h-screen">Загрузка...</div>;
  if (error) return <div className="flex justify-center items-center min-h-screen text-red-500">{error}</div>;
  if (!profile) return null;

  // Функция для форматирования даты в dd-mm-yyyy
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}-${month}-${year}`;
  };

  // Статистика из профиля
  const postsCount = profile.posts_count || 0;
  const subscribersCount = profile.subscribers_count || 0;
  const subscriptionsCount = profile.subscription_count || 0;

  return (
    <div className="max-w-5xl mx-auto py-10 px-4">
      {/* Верхняя часть: аватар, имя, статистика */}
      <div className="flex flex-col items-center md:flex-row md:items-start md:gap-12 mb-8">
        <div 
          className="relative group flex-shrink-0 flex justify-center items-center w-36 h-36 rounded-full bg-gray-200 overflow-hidden border-4 border-gray-100 shadow"
          onClick={() => user?.username === username && avatarInputRef.current.click()}
        >
          {profile.avatar ? (
            <img src={`${backendUrl}${profile.avatar}`} alt="avatar" className="w-full h-full object-cover" />
          ) : (
            <span className="text-6xl text-gray-400">👤</span>
          )}
          {user?.username === username && (
            <>
              <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                <span className="text-white text-lg font-semibold">Изменить</span>
              </div>
              <input 
                type="file" 
                ref={avatarInputRef} 
                onChange={handleAvatarChange} 
                className="hidden"
                accept="image/*"
              />
            </>
          )}
        </div>
        <div className="flex-1 mt-6 md:mt-0 w-full">
          <div className="flex flex-col md:flex-row md:items-center md:gap-6 mb-4">
            <h2 className="text-3xl font-semibold text-center md:text-left">{profile.user?.username || username}</h2>
            {user && user.username === username && (
              <div className="flex justify-center md:justify-start mt-2 md:mt-0">
                <Link
                  to={`/profile/${username}/edit`}
                  className="bg-gray-200 hover:bg-gray-300 text-black font-bold py-2 px-4 rounded"
                >
                  Редактировать профиль
                </Link>
              </div>
            )}
            {/* Кнопка подписки/отписки */}
            {user && user.username !== username && (
              <>
                <button
                  onClick={handleSubscribe}
                  disabled={subLoading}
                  className={`ml-0 md:ml-4 mt-2 md:mt-0 px-4 py-2 rounded font-bold transition-colors ${subscribed ? 'bg-red-100 text-red-700 hover:bg-red-200' : 'bg-blue-500 text-white hover:bg-blue-600'}`}
                >
                  {subscribed ? 'Отписаться' : 'Подписаться'}
                </button>
                {/* Кнопки дружбы */}
                {profile.is_friend ? (
                  <span className="ml-4 mt-2 md:mt-0 px-4 py-2 rounded font-bold bg-green-100 text-green-700">Ваш друг</span>
                ) : profile.friend_request_sent ? (
                  <span className="ml-4 mt-2 md:mt-0 px-4 py-2 rounded font-bold bg-yellow-100 text-yellow-700">Ожидание принятия</span>
                ) : (
                  <button
                    onClick={async () => {
                      try {
                        await friendshipsApi.sendFriendRequest(username);
                        // Обновить профиль для отображения статуса
                        const res = await profilesApi.getProfile(username);
                        setProfile(res.data);
                      } catch (e) {
                        alert('Ошибка при отправке запроса в друзья');
                      }
                    }}
                    className="ml-4 mt-2 md:mt-0 px-4 py-2 rounded font-bold bg-blue-100 text-blue-700 hover:bg-blue-200 transition-colors"
                  >
                    Запросить дружбу
                  </button>
                )}
              </>
            )}
          </div>
          <div className="flex justify-center md:justify-start gap-8 mb-4">
            <div className="text-center"><span className="font-bold">{postsCount}</span><div className="text-xs text-gray-500">публикаций</div></div>
            <button 
              onClick={handleOpenSubscribers}
              className="text-center hover:opacity-70 transition-opacity cursor-pointer"
            >
              <span className="font-bold">{subscribersCount}</span>
              <div className="text-xs text-gray-500">подписчиков</div>
            </button>
            <button 
              onClick={handleOpenSubscriptions}
              className="text-center hover:opacity-70 transition-opacity cursor-pointer"
            >
              <span className="font-bold">{subscriptionsCount}</span>
              <div className="text-xs text-gray-500">подписок</div>
            </button>
          </div>
        </div>
      </div>
      {/* Описание профиля */}
      <div className="mb-8 text-center md:text-left">
        <div className="font-medium text-lg">{profile.first_name || ''} {profile.last_name || ''}</div>
        <div className="text-gray-700 whitespace-pre-line">{profile.bio || 'Нет описания'}</div>
        <div className="text-gray-500 text-sm mt-2">{profile.country?.name ? `Страна: ${profile.country.name}` : 'Страна не указана'}</div>
        <div className="text-gray-500 text-sm">{profile.birth_date ? `Дата рождения: ${formatDate(profile.birth_date)}` : ''}</div>
        <div className="text-gray-500 text-sm">{profile.email ? `Email: ${profile.email}` : ''}</div>
      </div>
      {/* Сетка публикаций */}
      <div>
        <div className="border-t border-gray-200 mb-4" />
        {postsLoading ? (
          <div className="flex justify-center items-center py-8">
            <div className="text-gray-500">Загрузка постов...</div>
          </div>
        ) : posts.length > 0 ? (
          <div className="grid grid-cols-3 gap-4 md:gap-6">
            {posts.map((post) => (
              <div 
                key={post.id} 
                className="aspect-square bg-gray-100 rounded-xl overflow-hidden cursor-pointer shadow-md hover:shadow-lg transition-all duration-200 hover:scale-105"
                onClick={() => handlePostClick(post)}
              >
                {post.preview ? (
                  <img 
                    src={`${backendUrl}${post.preview}`} 
                    alt={post.title || 'Post'} 
                    className="w-full h-full object-cover hover:opacity-90 transition-all duration-200 hover:scale-110"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <span className="text-6xl text-gray-300">📷</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <span className="text-4xl mb-4 block">📷</span>
            <p>Пока нет публикаций</p>
          </div>
        )}
      </div>

      {/* Модальное окно поста */}
      <PostModal
        post={selectedPost}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        backendUrl={backendUrl}
        setPosts={setPosts}
        posts={posts}
      />

      {/* Модальное окно подписок */}
      <SubscriptionsModal
        isOpen={subscriptionsModalOpen}
        onClose={handleCloseSubscriptionsModal}
        username={username}
        type="subscriptions"
        backendUrl={backendUrl}
        currentUser={user}
        onSubscriptionChange={handleSubscriptionChange}
      />

      {/* Модальное окно подписчиков */}
      <SubscriptionsModal
        isOpen={subscribersModalOpen}
        onClose={handleCloseSubscribersModal}
        username={username}
        type="subscribers"
        backendUrl={backendUrl}
        currentUser={user}
        onSubscriptionChange={handleSubscriptionChange}
      />
    </div>
  );
} 