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

  useEffect(() => {
    async function fetchProfile() {
      setLoading(true);
      setError('');
      try {
        const res = await profilesApi.getProfile(username);
        setProfile(res.data);
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
  }, [username, user, navigate]);

  if (user?.username !== username) {
    return null;
  }

  const handleSuccess = () => {
    navigate(`/profile/${username}`); // Перенаправляем на страницу профиля
  };

  if (loading) return <div className="flex justify-center items-center min-h-screen">Загрузка...</div>;
  if (error) return <div className="flex justify-center items-center min-h-screen text-red-500">{error}</div>;
  if (!profile) return null;

  return (
    <div className="max-w-xl mx-auto py-10 px-4">
      <h1 className="text-2xl font-bold mb-6">Редактировать профиль</h1>
      <EditProfileForm initial={profile} onSuccess={handleSuccess} />
    </div>
  );
} 