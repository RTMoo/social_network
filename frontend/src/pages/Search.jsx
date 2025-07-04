import { useState, useEffect, useRef, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { searchProfiles } from '../api/endpoints/search';
import { AuthContext } from '../context/AuthContext';

export default function Search() {
  const { user } = useContext(AuthContext);
  const [query, setQuery] = useState('');
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const searchTimeoutRef = useRef(null);

  // Поиск с debounce
  useEffect(() => {
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    if (query.trim().length === 0) {
      setProfiles([]);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null);

    searchTimeoutRef.current = setTimeout(async () => {
      try {
        const response = await searchProfiles(query.trim());
        setProfiles(response.data);
      } catch (err) {
        setError('Ошибка при поиске профилей');
        console.error('Ошибка поиска:', err);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [query]);

  const handleProfileClick = (username) => {
    navigate(`/profile/${username}`);
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Заголовок */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Поиск</h1>
        <p className="text-gray-600">Найдите пользователей по имени или имени пользователя</p>
      </div>

      {/* Поле поиска */}
      <div className="mb-8">
        <div className="relative max-w-2xl">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Введите имя или имя пользователя..."
            className="w-full px-4 py-4 pl-12 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
            autoFocus
          />
          <span className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 text-xl">
            🔍
          </span>
          {loading && (
            <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400">
              ⏳
            </span>
          )}
        </div>
      </div>

      {/* Результаты */}
      <div className="space-y-4">
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="text-red-600 text-center">
              {error}
            </div>
          </div>
        )}
        
        {!loading && !error && query.trim().length > 0 && profiles.length === 0 && (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
            <div className="text-gray-500 text-lg mb-2">Профили не найдены</div>
            <div className="text-gray-400">Попробуйте изменить запрос</div>
          </div>
        )}

                {profiles.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
              <h2 className="text-lg font-semibold text-gray-900">
                Найдено профилей: {profiles.filter(profile => {
                  const profileUsername = profile.user?.username || profile.username;
                  return !user || user.username !== profileUsername;
                }).length}
              </h2>
            </div>
            <div className="divide-y divide-gray-200">
              {profiles
                .filter(profile => {
                  const profileUsername = profile.user?.username || profile.username;
                  return !user || user.username !== profileUsername;
                })
                .map((profile, index) => {
                  const profileUsername = profile.user?.username || profile.username;
                  
                  return (
                    <div
                      key={index}
                      onClick={() => handleProfileClick(profileUsername)}
                      className="flex items-center gap-4 p-6 hover:bg-gray-50 cursor-pointer transition-colors"
                    >
                      <div className="w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center overflow-hidden flex-shrink-0">
                        {profile.avatar ? (
                          <img 
                            src={profile.avatar} 
                            alt={profileUsername}
                            className="w-full h-full object-cover"
                          />
                        ) : (
                          <span className="text-2xl">👤</span>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-semibold text-lg text-gray-900">
                          @{profileUsername}
                        </div>
                      </div>
                      <div className="flex-shrink-0">
                        <span className="text-gray-400">→</span>
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>
        )}

        {loading && (
          <div className="bg-white border border-gray-200 rounded-lg p-8 text-center">
            <div className="text-gray-500 text-lg">Поиск...</div>
          </div>
        )}
      </div>
    </div>
  );
} 