import { useState, useEffect, useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import EditProfileForm from '../features/profile/EditProfileForm';
import { AuthContext } from '../context/AuthContext';
import { profilesApi } from '../api';

export default function EditProfilePage() {
  const { username } = useParams();
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [avatarUrl, setAvatarUrl] = useState(null);

  const backendUrl = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace('/api/', '') : 'http://localhost:8000';

  useEffect(() => {
    async function fetchProfile() {
      setLoading(true);
      setError('');
      try {
        const res = await profilesApi.getProfile(username);
        setProfile(res.data);
        if (res.data.avatar) {
          setAvatarUrl(`${backendUrl}${res.data.avatar}`);
        }
      } catch (e) {
        setError('Ошибка загрузки профиля');
      } finally {
        setLoading(false);
      }
    }

    if (user?.username === username) {
      fetchProfile();
    } else {
      navigate(`/profile/${username}`);
    }
  }, [username, user, navigate, backendUrl]);

  if (user?.username !== username) {
    return null;
  }

  const handleSuccess = () => {
    navigate(`/profile/${username}`); // Перенаправляем на страницу профиля
  };

  const handleAvatarUpdate = (newAvatarPath) => {
    setAvatarUrl(`${backendUrl}${newAvatarPath}`);
  };

  if (loading) return <div className="flex justify-center items-center min-h-screen">Загрузка...</div>;
  if (error) return <div className="flex justify-center items-center min-h-screen text-red-500">{error}</div>;
  if (!profile) return null;

  // Преобразуем country из объекта в строку-код
  const initial = {
    ...profile,
    country: profile.country ? profile.country.code : 'null',
  };

  return (
    <div className="max-w-xl mx-auto py-10 px-4">
      <h1 className="text-2xl font-bold mb-6">Редактировать профиль</h1>
      <EditProfileForm 
        initial={initial} 
        onSuccess={handleSuccess} 
        avatarUrl={avatarUrl}
        onAvatarUpdate={handleAvatarUpdate}
      />
    </div>
  );
} 