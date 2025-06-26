import { useContext } from 'react';
import FriendsBlock from '../components/FriendsBlock';
import { AuthContext } from '../context/AuthContext';

export default function Friends() {
  const { user } = useContext(AuthContext);
  if (!user) return <div className="flex justify-center items-center min-h-screen">Необходимо войти в аккаунт</div>;
  return (
    <div className="max-w-2xl mx-auto py-10 px-4">
      <h1 className="text-3xl font-bold mb-6">Друзья</h1>
      <FriendsBlock user={user} />
    </div>
  );
} 